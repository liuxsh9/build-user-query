"""
SFT Auto-Labeling Pipeline — Concurrent Version

Processes SFT data through the labeling pipeline with high concurrency:
  1. Preprocessing (structural signal extraction) — local, instant
  2. Call 1 — Intent, Language, Domain, Task, Difficulty — concurrent LLM
  3. Call 2 — Concept, Agentic, Constraint, Context — concurrent LLM (depends on Call 1)
  4. Validation — local, instant
  5. Optional arbitration for low-confidence labels — concurrent LLM

Supports single file or directory input. Directory mode processes files serially
(samples within each file run concurrently) with checkpoint-based resume.

Usage:
  python3 labeling/pipeline.py [--input FILE_OR_DIR] [--model MODEL] [--concurrency N]
  python3 labeling/pipeline.py --resume labeling/data/runs/<run_dir>/
"""

import json
import time
import asyncio
import argparse
import random
import sys
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field

import httpx
from rich.progress import (
    Progress, SpinnerColumn, BarColumn, TextColumn,
    TimeElapsedColumn, TimeRemainingColumn, MofNCompleteColumn,
)

sys.path.insert(0, str(Path(__file__).parent))
from prompts import (
    CALL1_SYSTEM, CALL1_FEWSHOT, CALL2_SYSTEM, CALL2_FEWSHOT,
    TAG_POOLS, SINGLE_SELECT, MULTI_SELECT
)
from preprocessing import preprocess, format_signals_for_prompt, normalize_and_slice, truncate_conversations_for_labeling
from config import (
    LITELLM_BASE, LITELLM_KEY, CONFIDENCE_THRESHOLD, CONSISTENCY_RULES,
    DEFAULT_INPUT, DEFAULT_OUTPUT, DATA_DIR,
    DEFAULT_MODEL, DEFAULT_CONCURRENCY, MAX_RETRIES, SAMPLE_MAX_RETRIES,
    REQUEST_TIMEOUT, SAMPLE_TIMEOUT,
    MAX_CONVERSATION_CHARS,
    DIR_PIPELINE_WATERMARK, DIR_PIPELINE_MAX_FILES,
)


# ─────────────────────────────────────────────────────────
# Progress bar
# ─────────────────────────────────────────────────────────

def create_progress():
    """Create a Rich progress bar display for labeling."""
    return Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(bar_width=30),
        MofNCompleteColumn(),
        TextColumn("•", style="dim"),
        TimeElapsedColumn(),
        TextColumn("•", style="dim"),
        TimeRemainingColumn(),
        TextColumn("{task.fields[info]}", style="cyan"),
    )


# ─────────────────────────────────────────────────────────
# Directory discovery & checkpoint
# ─────────────────────────────────────────────────────────

def discover_input_files(input_path):
    """Discover input files. Returns [(abs_path, rel_path_or_None)].

    - File → [(path, None)]  (single-file mode, no relative path)
    - Directory → [(abs, rel), ...] sorted by relative path
    """
    p = Path(input_path)
    if p.is_file():
        return [(p.resolve(), None)]

    files = sorted(
        f.resolve()
        for ext in ("*.json", "*.jsonl")
        for f in p.rglob(ext)
        if f.is_file()
    )
    base = p.resolve()
    return [(f, f.relative_to(base)) for f in files]


def load_checkpoint(checkpoint_path):
    """Load existing checkpoint or return None."""
    if checkpoint_path.exists():
        with open(checkpoint_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def create_checkpoint(checkpoint_path, files):
    """Create a fresh checkpoint for a batch run."""
    ckpt = {
        "status": "in_progress",
        "completed": [],
        "failed": {},
        "total_files": len(files),
    }
    _write_checkpoint(checkpoint_path, ckpt)
    return ckpt


def update_checkpoint(checkpoint_path, rel_path_str, success=True, error_msg=None):
    """Mark a file as completed or failed in the checkpoint."""
    ckpt = load_checkpoint(checkpoint_path) or {}
    if success:
        if rel_path_str not in ckpt.get("completed", []):
            ckpt.setdefault("completed", []).append(rel_path_str)
        ckpt.get("failed", {}).pop(rel_path_str, None)
    else:
        ckpt.setdefault("failed", {})[rel_path_str] = error_msg or "unknown"
    done = len(ckpt.get("completed", [])) + len(ckpt.get("failed", {}))
    if done >= ckpt.get("total_files", 0):
        ckpt["status"] = "done"
    _write_checkpoint(checkpoint_path, ckpt)
    return ckpt


def _write_checkpoint(checkpoint_path, ckpt):
    with open(checkpoint_path, "w", encoding="utf-8") as f:
        json.dump(ckpt, f, ensure_ascii=False, indent=2)


def merge_stats(all_file_stats):
    """Merge per-file stats into a global summary."""
    merged = {
        "total_samples": 0, "success": 0, "failed": 0,
        "total_llm_calls": 0, "total_prompt_tokens": 0,
        "total_completion_tokens": 0, "total_tokens": 0,
        "arbitrated_count": 0,
        "validation_issue_count": 0, "consistency_warning_count": 0,
        "unmapped_unique_count": 0,
        "total_elapsed_seconds": 0,
        "tag_distributions": {},
        "confidence_stats": {},
        "cross_matrix": {},
        "unmapped_tags": {},
        "files_processed": len(all_file_stats),
    }
    for st in all_file_stats:
        for k in ("total_samples", "success", "failed", "total_llm_calls",
                   "total_prompt_tokens", "total_completion_tokens", "total_tokens",
                   "arbitrated_count", "validation_issue_count", "consistency_warning_count"):
            merged[k] += st.get(k, 0)
        merged["total_elapsed_seconds"] += st.get("total_elapsed_seconds", 0)
        # Merge tag distributions
        for dim, dist in st.get("tag_distributions", {}).items():
            if dim not in merged["tag_distributions"]:
                merged["tag_distributions"][dim] = {}
            for tag, count in dist.items():
                merged["tag_distributions"][dim][tag] = merged["tag_distributions"][dim].get(tag, 0) + count
        # Merge unmapped
        for tag, count in st.get("unmapped_tags", {}).items():
            merged["unmapped_tags"][tag] = merged["unmapped_tags"].get(tag, 0) + count
        # Merge confidence_stats (weighted by count for proper averaging)
        for dim, cs in st.get("confidence_stats", {}).items():
            if dim not in merged["confidence_stats"]:
                merged["confidence_stats"][dim] = {"sum": 0, "count": 0, "min": cs.get("min", 1), "max": cs.get("max", 0), "below_threshold": 0}
            entry = merged["confidence_stats"][dim]
            n = cs.get("count", 0)
            if n == 0:
                continue
            entry["sum"] += cs["mean"] * n
            entry["count"] += n
            entry["min"] = min(entry["min"], cs.get("min", 1))
            entry["max"] = max(entry["max"], cs.get("max", 0))
            entry["below_threshold"] += cs.get("below_threshold", 0)
        # Merge cross_matrix (intent × difficulty)
        for key, count in st.get("cross_matrix", {}).items():
            merged["cross_matrix"][key] = merged["cross_matrix"].get(key, 0) + count

    # Sort distributions and unmapped
    for dim in merged["tag_distributions"]:
        merged["tag_distributions"][dim] = dict(sorted(merged["tag_distributions"][dim].items(), key=lambda x: -x[1]))
    merged["unmapped_tags"] = dict(sorted(merged["unmapped_tags"].items(), key=lambda x: -x[1]))
    merged["unmapped_unique_count"] = len(merged["unmapped_tags"])

    # Finalize confidence_stats: convert accumulated sum/count to mean
    for dim, entry in merged["confidence_stats"].items():
        n = entry.get("count", 0)
        if n > 0:
            merged["confidence_stats"][dim] = {
                "mean": round(entry["sum"] / n, 3),
                "min": round(entry["min"], 3),
                "max": round(entry["max"], 3),
                "below_threshold": entry["below_threshold"],
                "count": n,
            }

    total = merged["total_samples"]
    merged["success_rate"] = round(merged["success"] / max(total, 1), 4)
    merged["avg_calls_per_sample"] = round(merged["total_llm_calls"] / max(total, 1), 2)
    merged["arbitrated_rate"] = round(merged["arbitrated_count"] / max(total, 1), 4)

    return merged


def resolve_run_dir(args, input_path):
    """Determine the run output directory based on --output flag.

    Three modes:
      - None (default): sibling of input, auto-named <timestamp>_<model>/
      - "runs": legacy behavior, DATA_DIR/runs/<timestamp>_<model>/
      - explicit path: use as-is (absolute or relative to cwd)
    """
    run_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_short = args.model.replace("/", "-")
    auto_name = f"{run_ts}_{model_short}"

    if args.output is None:
        # Default: sibling of input
        parent = input_path.parent
        return parent / auto_name

    if args.output == "runs":
        # Legacy: labeling/data/runs/
        return DATA_DIR / "runs" / auto_name

    # Explicit path
    return Path(args.output).resolve()


# ─────────────────────────────────────────────────────────
# Async LLM calls
# ─────────────────────────────────────────────────────────

async def async_llm_call(http_client, messages, model, temperature=0.1, max_tokens=1000, max_retries=MAX_RETRIES):
    """Async LLM call with retry + jitter. Returns (parsed_json, raw_content, usage)."""
    url = f"{LITELLM_BASE}/chat/completions"
    headers = {"Authorization": f"Bearer {LITELLM_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            resp = await http_client.post(url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT)
            if resp.status_code in (403, 429, 502, 503, 504):
                # Rate limited or server/gateway error — exponential backoff with jitter
                base_wait = min(2 ** attempt * 3 + 2, 60)
                wait = base_wait + random.uniform(0, base_wait * 0.5)
                last_error = f"HTTP {resp.status_code}: {resp.text[:200]}"
                if attempt < max_retries:
                    await asyncio.sleep(wait)
                    continue
            if resp.status_code == 400:
                # Client error (context_length_exceeded, invalid request) — not retryable
                error_text = resp.text[:300]
                return None, f"HTTP 400: {error_text}", {"prompt_tokens": 0, "completion_tokens": 0, "error": f"HTTP 400: {error_text}", "non_retryable": True}
            resp.raise_for_status()
            data = resp.json()

            content = data["choices"][0]["message"]["content"].strip()
            usage = data.get("usage", {})
            usage_dict = {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
            }

            # Parse JSON
            json_str = content
            if json_str.startswith("```"):
                lines = json_str.split("\n")
                json_lines = []
                in_block = False
                for line in lines:
                    if line.startswith("```") and not in_block:
                        in_block = True
                        continue
                    elif line.startswith("```") and in_block:
                        break
                    elif in_block:
                        json_lines.append(line)
                json_str = "\n".join(json_lines)

            parsed = json.loads(json_str)
            return parsed, content, usage_dict

        except (json.JSONDecodeError, KeyError) as e:
            last_error = f"ParseError: {e}"
            if attempt < max_retries:
                await asyncio.sleep(2 + random.uniform(0, 2))
                continue
            return None, content if 'content' in dir() else "", {"prompt_tokens": 0, "completion_tokens": 0, "error": last_error}
        except Exception as e:
            last_error = f"{type(e).__name__}: {e}"
            if attempt < max_retries:
                base_wait = min(2 ** attempt * 3 + 2, 60)
                wait = base_wait + random.uniform(0, base_wait * 0.5)
                await asyncio.sleep(wait)
                continue
            return None, str(e), {"prompt_tokens": 0, "completion_tokens": 0, "error": last_error}

    return None, f"max retries exceeded: {last_error}", {"prompt_tokens": 0, "completion_tokens": 0, "error": last_error or "max_retries"}


# ─────────────────────────────────────────────────────────
# Prompt builders (inline to avoid cross-import issues with async)
# ─────────────────────────────────────────────────────────

def build_call1_messages(conversation_json, preprocessed_signals):
    user_content = f"""<conversation>
{conversation_json}
</conversation>

<preprocessed_signals>
{preprocessed_signals}
</preprocessed_signals>"""
    messages = [{"role": "system", "content": CALL1_SYSTEM}]
    messages.extend(CALL1_FEWSHOT)
    messages.append({"role": "user", "content": user_content})
    return messages


def build_call2_messages(conversation_json, preprocessed_signals, call1_result):
    call1_str = json.dumps(call1_result, ensure_ascii=False) if isinstance(call1_result, dict) else str(call1_result)
    user_content = f"""<conversation>
{conversation_json}
</conversation>

<call1_result>
{call1_str}
</call1_result>

<preprocessed_signals>
{preprocessed_signals}
</preprocessed_signals>"""
    messages = [{"role": "system", "content": CALL2_SYSTEM}]
    messages.extend(CALL2_FEWSHOT)
    messages.append({"role": "user", "content": user_content})
    return messages


# ─────────────────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────────────────

def validate_tags(result, call_name="call1"):
    issues = []
    unmapped = result.get("unmapped", [])
    if not isinstance(unmapped, list):
        unmapped = []
    cleaned = dict(result)

    dims = (["intent", "language", "domain", "task", "difficulty"] if call_name == "call1"
            else ["concept", "agentic", "constraint", "context"])

    for dim in dims:
        if dim not in result:
            issues.append(f"Missing: {dim}")
            cleaned[dim] = "" if dim in SINGLE_SELECT else []
            continue

        pool = TAG_POOLS.get(dim, set())
        if dim in SINGLE_SELECT:
            val = result[dim]
            if val and val not in pool:
                issues.append(f"{dim}: '{val}' not in pool")
                unmapped.append({"dimension": dim, "value": val})
                cleaned[dim] = ""
        else:
            vals = result[dim] if isinstance(result[dim], list) else [result[dim]]
            valid = []
            for v in vals:
                if v in pool:
                    valid.append(v)
                else:
                    issues.append(f"{dim}: '{v}' not in pool")
                    unmapped.append({"dimension": dim, "value": v})
            cleaned[dim] = valid

    cleaned["unmapped"] = unmapped
    return cleaned, issues


def check_consistency(labels):
    warnings = []
    ns = {
        "intent": labels.get("intent", ""),
        "difficulty": labels.get("difficulty", ""),
        "context": labels.get("context", ""),
        "language": labels.get("language", []),
        "domain": labels.get("domain", []),
        "concept": labels.get("concept", []),
        "task": labels.get("task", []),
        "agentic": labels.get("agentic", []),
        "constraint": labels.get("constraint", []),
        "len": len,
    }
    for condition, message in CONSISTENCY_RULES:
        try:
            if eval(condition, {"__builtins__": {}}, ns):
                warnings.append(message)
        except Exception:
            pass
    return warnings


def find_low_confidence_dims(labels, threshold=CONFIDENCE_THRESHOLD):
    low = []
    for dim, score in labels.get("confidence", {}).items():
        if isinstance(score, (int, float)) and score < threshold:
            low.append((dim, score))
    return low


# ─────────────────────────────────────────────────────────
# Per-sample pipeline (async)
# ─────────────────────────────────────────────────────────

async def label_one(http_client, sample, model, sample_idx, total, sem, enable_arbitration=True):
    """Label a single sample with sample-level retry on failure."""
    start = time.time()

    # Truncate oversized conversations before sending to LLM
    conversations = sample.get("conversations", [])
    truncated_convs, was_truncated = truncate_conversations_for_labeling(
        conversations, max_total_chars=MAX_CONVERSATION_CHARS)

    for sample_attempt in range(SAMPLE_MAX_RETRIES + 1):
        if sample_attempt > 0:
            # Back off before retry with jitter, outside semaphore so we don't block others
            base_wait = 2 ** sample_attempt * 2
            await asyncio.sleep(base_wait + random.uniform(0, base_wait))

        async with sem:
            monitor = {
                "sample_id": sample.get("id", f"sample-{sample_idx}"),
                "index": sample_idx,
                "llm_calls": 0,
                "total_prompt_tokens": 0,
                "total_completion_tokens": 0,
                "validation_issues": [],
                "consistency_warnings": [],
                "low_confidence_dims": [],
                "arbitrated": False,
                "sample_attempt": sample_attempt,
                "status": "success",
            }

            try:
                # Preprocess (uses original conversations for signal extraction)
                signals = preprocess(sample)
                signals_str = format_signals_for_prompt(signals)
                # Use truncated conversations for LLM prompt
                conversations_json = json.dumps(truncated_convs, ensure_ascii=False)
                if was_truncated:
                    monitor["truncated"] = True

                # Call 1
                msgs1 = build_call1_messages(conversations_json, signals_str)
                call1_result, call1_raw, usage1 = await async_llm_call(http_client, msgs1, model)
                monitor["llm_calls"] += 1
                monitor["total_prompt_tokens"] += usage1["prompt_tokens"]
                monitor["total_completion_tokens"] += usage1["completion_tokens"]

                if call1_result is None:
                    monitor["status"] = "call1_failed"
                    monitor["error"] = usage1.get("error", "unknown")
                    monitor["error_response"] = call1_raw[:500] if call1_raw else ""
                    if usage1.get("non_retryable"):
                        return sample_idx, None, monitor
                    if sample_attempt < SAMPLE_MAX_RETRIES:
                        continue
                    return sample_idx, None, monitor

                call1_cleaned, call1_issues = validate_tags(call1_result, "call1")
                monitor["validation_issues"].extend(call1_issues)

                # Call 2 (depends on Call 1)
                call1_context = {d: call1_cleaned[d] for d in ["intent", "language", "domain", "task", "difficulty"] if d in call1_cleaned}
                msgs2 = build_call2_messages(conversations_json, signals_str, call1_context)
                call2_result, call2_raw, usage2 = await async_llm_call(http_client, msgs2, model)
                monitor["llm_calls"] += 1
                monitor["total_prompt_tokens"] += usage2["prompt_tokens"]
                monitor["total_completion_tokens"] += usage2["completion_tokens"]

                if call2_result is None:
                    monitor["status"] = "call2_failed"
                    monitor["error"] = usage2.get("error", "unknown")
                    monitor["error_response"] = call2_raw[:500] if call2_raw else ""
                    if usage2.get("non_retryable"):
                        # Return partial results from Call 1
                        labels = {d: call1_cleaned.get(d) for d in ["intent", "language", "domain", "task", "difficulty"]}
                        labels["confidence"] = call1_cleaned.get("confidence", {})
                        labels["unmapped"] = call1_cleaned.get("unmapped", [])
                        return sample_idx, labels, monitor
                    if sample_attempt < SAMPLE_MAX_RETRIES:
                        continue
                    # Final attempt: return partial results from Call 1
                    labels = {d: call1_cleaned.get(d) for d in ["intent", "language", "domain", "task", "difficulty"]}
                    labels["confidence"] = call1_cleaned.get("confidence", {})
                    labels["unmapped"] = call1_cleaned.get("unmapped", [])
                    return sample_idx, labels, monitor

                call2_cleaned, call2_issues = validate_tags(call2_result, "call2")
                monitor["validation_issues"].extend(call2_issues)

                # Merge
                labels = {}
                for d in ["intent", "language", "domain", "task", "difficulty"]:
                    labels[d] = call1_cleaned.get(d, [] if d in MULTI_SELECT else "")
                for d in ["concept", "agentic", "constraint", "context"]:
                    labels[d] = call2_cleaned.get(d, [] if d in MULTI_SELECT else "")
                labels["confidence"] = {**call1_cleaned.get("confidence", {}), **call2_cleaned.get("confidence", {})}
                labels["unmapped"] = call1_cleaned.get("unmapped", []) + call2_cleaned.get("unmapped", [])

                # Consistency
                warnings = check_consistency(labels)
                monitor["consistency_warnings"] = warnings

                # Arbitration
                low_conf = find_low_confidence_dims(labels)
                monitor["low_confidence_dims"] = [{"dim": d, "conf": s} for d, s in low_conf]

                if low_conf and enable_arbitration:
                    monitor["arbitrated"] = True
                    # Re-run relevant call(s)
                    call1_dims = {"intent", "language", "domain", "task", "difficulty"}
                    call2_dims = {"concept", "agentic", "constraint", "context"}

                    if any(d in call1_dims for d, _ in low_conf):
                        re1, _, u1 = await async_llm_call(http_client, msgs1, model, temperature=0.3)
                        monitor["llm_calls"] += 1
                        monitor["total_prompt_tokens"] += u1["prompt_tokens"]
                        monitor["total_completion_tokens"] += u1["completion_tokens"]
                        if re1:
                            re1_clean, _ = validate_tags(re1, "call1")
                            for d, _ in low_conf:
                                if d in call1_dims and d in re1_clean:
                                    labels[d] = re1_clean[d]
                                    labels["confidence"][d] = re1_clean.get("confidence", {}).get(d, 0)

                    if any(d in call2_dims for d, _ in low_conf):
                        re2, _, u2 = await async_llm_call(http_client, msgs2, model, temperature=0.3)
                        monitor["llm_calls"] += 1
                        monitor["total_prompt_tokens"] += u2["prompt_tokens"]
                        monitor["total_completion_tokens"] += u2["completion_tokens"]
                        if re2:
                            re2_clean, _ = validate_tags(re2, "call2")
                            for d, _ in low_conf:
                                if d in call2_dims and d in re2_clean:
                                    labels[d] = re2_clean[d]
                                    labels["confidence"][d] = re2_clean.get("confidence", {}).get(d, 0)

            except Exception as e:
                monitor["status"] = f"error: {str(e)[:100]}"
                if sample_attempt < SAMPLE_MAX_RETRIES:
                    continue
                return sample_idx, None, monitor

            monitor["elapsed_seconds"] = round(time.time() - start, 2)
            return sample_idx, labels, monitor

        # Should not reach here, but just in case
        monitor["elapsed_seconds"] = round(time.time() - start, 2)
        return sample_idx, None, monitor


def compute_stats(all_monitors, all_labels):
    """Compute aggregate statistics."""
    total = len(all_monitors)
    success = sum(1 for m in all_monitors if m["status"] == "success")
    total_calls = sum(m["llm_calls"] for m in all_monitors)
    total_pt = sum(m["total_prompt_tokens"] for m in all_monitors)
    total_ct = sum(m["total_completion_tokens"] for m in all_monitors)
    arbitrated = sum(1 for m in all_monitors if m["arbitrated"])

    distributions = {}
    for dim in ["intent", "language", "domain", "concept", "task", "agentic", "constraint", "context", "difficulty"]:
        dist = {}
        for labels in all_labels:
            if labels is None:
                continue
            val = labels.get(dim, [])
            if isinstance(val, list):
                for v in val:
                    dist[v] = dist.get(v, 0) + 1
            elif val:
                dist[val] = dist.get(val, 0) + 1
        distributions[dim] = dict(sorted(dist.items(), key=lambda x: -x[1]))

    all_unmapped = {}
    for labels in all_labels:
        if labels is None:
            continue
        for item in labels.get("unmapped", []):
            key = f"{item.get('dimension', '?')}:{item.get('value', '?')}" if isinstance(item, dict) else str(item)
            all_unmapped[key] = all_unmapped.get(key, 0) + 1

    conf_stats = {}
    for dim in ["intent", "language", "domain", "task", "difficulty", "concept", "agentic", "constraint", "context"]:
        scores = [l["confidence"][dim] for l in all_labels if l and "confidence" in l and isinstance(l["confidence"].get(dim), (int, float))]
        if scores:
            conf_stats[dim] = {
                "mean": round(sum(scores) / len(scores), 3),
                "min": round(min(scores), 3),
                "max": round(max(scores), 3),
                "below_threshold": sum(1 for s in scores if s < CONFIDENCE_THRESHOLD),
                "count": len(scores),
            }

    # Intent × Difficulty cross matrix
    cross = {}
    for labels in all_labels:
        if labels is None:
            continue
        intent = labels.get("intent", "?")
        diff = labels.get("difficulty", "?")
        key = f"{intent}|{diff}"
        cross[key] = cross.get(key, 0) + 1

    return {
        "total_samples": total,
        "success": success,
        "failed": total - success,
        "success_rate": round(success / max(total, 1), 4),
        "total_llm_calls": total_calls,
        "avg_calls_per_sample": round(total_calls / max(total, 1), 2),
        "total_prompt_tokens": total_pt,
        "total_completion_tokens": total_ct,
        "total_tokens": total_pt + total_ct,
        "arbitrated_count": arbitrated,
        "arbitrated_rate": round(arbitrated / max(total, 1), 4),
        "validation_issue_count": sum(1 for m in all_monitors if m["validation_issues"]),
        "consistency_warning_count": sum(1 for m in all_monitors if m["consistency_warnings"]),
        "unmapped_tags": dict(sorted(all_unmapped.items(), key=lambda x: -x[1])),
        "unmapped_unique_count": len(all_unmapped),
        "confidence_stats": conf_stats,
        "low_confidence_frequency": dict(sorted(
            {d: sum(1 for m in all_monitors for lc in m.get("low_confidence_dims", []) if lc["dim"] == d)
             for d in set(lc["dim"] for m in all_monitors for lc in m.get("low_confidence_dims", []))}.items(),
            key=lambda x: -x[1])),
        "tag_distributions": distributions,
        "cross_matrix": cross,
    }


# ─────────────────────────────────────────────────────────
# Streaming I/O + cross-file helpers
# ─────────────────────────────────────────────────────────

def iter_samples_from_file(input_path, limit=0, shuffle=False):
    """Load and normalize samples from a file with minimal memory overhead.

    JSONL: line-by-line read + normalize_and_slice (memory = 1 raw line at a time).
    JSON:  json.load then del raw (can't avoid full load, but releases raw ASAP).

    Returns: (samples_list, n_raw)
    """
    input_path = Path(input_path)
    samples = []
    n_raw = 0

    if str(input_path).endswith(".jsonl"):
        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                n_raw += 1
                raw = json.loads(line)
                samples.extend(normalize_and_slice(raw))
                del raw
    else:
        with open(input_path, "r", encoding="utf-8") as f:
            raw_samples = json.load(f)
        if not isinstance(raw_samples, list):
            raw_samples = [raw_samples]
        n_raw = len(raw_samples)
        for s in raw_samples:
            samples.extend(normalize_and_slice(s))
        del raw_samples

    for i, s in enumerate(samples):
        if not s.get("id"):
            s["id"] = f"sample-{i:04d}"

    if shuffle:
        random.shuffle(samples)
    if limit > 0:
        samples = samples[:limit]

    return samples, n_raw


@dataclass
class FileCollector:
    """Track per-file labeling results for cross-file pipeline."""
    file_idx: int
    abs_path: Path
    rel_path: Path          # relative path within input dir
    output_dir: Path
    prefix: str             # file stem for output naming
    total: int
    samples: list
    done: int = 0
    ok: int = 0
    fail: int = 0
    labels: list = field(default_factory=list)
    monitors: list = field(default_factory=list)
    completed: bool = False

    def __post_init__(self):
        # Pre-allocate result slots
        self.labels = [None] * self.total
        self.monitors = [None] * self.total


def flush_file_output(collector, run_dir, checkpoint_path, pprint=print):
    """Write all outputs for a completed file and release memory.

    Writes labeled.json/jsonl, monitor.jsonl, stats.json, dashboard.
    Updates checkpoint. Deletes heavy data from collector to free memory.
    Returns the stats dict.
    """
    samples = collector.samples
    all_labels = collector.labels
    all_monitors = collector.monitors
    output_dir = collector.output_dir
    prefix = collector.prefix
    total = collector.total

    # Attach labels to samples
    for idx, sample in enumerate(samples):
        sample["labels"] = all_labels[idx]
        if all_monitors[idx]:
            sample["labeling_monitor"] = {
                "llm_calls": all_monitors[idx]["llm_calls"],
                "arbitrated": all_monitors[idx]["arbitrated"],
                "validation_issues": all_monitors[idx]["validation_issues"],
                "consistency_warnings": all_monitors[idx]["consistency_warnings"],
            }

    # Write outputs
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"_{prefix}" if prefix else ""

    labeled_json = f"labeled{suffix}.json"
    labeled_jsonl = f"labeled{suffix}.jsonl"
    monitor_file = f"monitor{suffix}.jsonl"
    stats_file = f"stats{suffix}.json"
    dashboard_file = f"dashboard{suffix}.html"
    failed_samples_file = f"failed_samples{suffix}.jsonl"

    with open(output_dir / labeled_json, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)

    with open(output_dir / labeled_jsonl, "w", encoding="utf-8") as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    with open(output_dir / monitor_file, "w", encoding="utf-8") as f:
        for m in all_monitors:
            if m:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

    # Write failed samples (original, without labels) for easy retry
    failed_indices = [i for i, l in enumerate(all_labels) if l is None]
    if failed_indices:
        with open(output_dir / failed_samples_file, "w", encoding="utf-8") as f:
            for i in failed_indices:
                s = dict(samples[i])
                s.pop("labels", None)
                s.pop("labeling_monitor", None)
                f.write(json.dumps(s, ensure_ascii=False) + "\n")

    # Append to global failure log at run_dir root
    failure_records = []
    for i in failed_indices:
        m = all_monitors[i]
        record = {
            "sample_id": samples[i].get("id", f"sample-{i}"),
            "source_file": str(collector.abs_path),
            "status": m["status"] if m else "timeout",
            "error": (m.get("error", "") if m else f"exceeded {SAMPLE_TIMEOUT}s"),
            "error_response": (m.get("error_response", "")[:200] if m else ""),
            "attempts": (m.get("sample_attempt", 0) + 1 if m else 0),
        }
        failure_records.append(record)
    if failure_records:
        with open(run_dir / "failures.jsonl", "a", encoding="utf-8") as f:
            for r in failure_records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Compute and write stats
    valid_monitors = [m for m in all_monitors if m is not None]
    stats = compute_stats(valid_monitors, all_labels)
    stats["input_file"] = str(collector.abs_path)

    with open(output_dir / stats_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    # Per-file dashboard
    try:
        from tools.visualize_labels import generate_dashboard
        generate_dashboard(output_dir, labeled_file=labeled_json,
                           stats_file=stats_file, output_file=dashboard_file)
    except Exception:
        pass

    success = stats["success"]
    total_tokens = stats["total_tokens"]
    pprint(f"  ✓ {success}/{total} success, {total_tokens:,} tokens")

    # Print failure details — batch into single print to avoid progress bar flicker
    failed_count = total - success
    if failed_count > 0:
        lines = []
        failed_monitors = [m for m in all_monitors if m and m["status"] != "success"]
        error_groups = {}
        for m in failed_monitors:
            err_type = m["status"]
            error_groups.setdefault(err_type, []).append(m)
        lines.append(f"  ✗ {failed_count} failed:")
        for err_type, monitors in sorted(error_groups.items()):
            lines.append(f"    [{err_type}] ×{len(monitors)}")
            for m in monitors[:3]:
                sid = m.get("sample_id", "?")
                err = m.get("error", "")
                resp = m.get("error_response", "")
                attempts = m.get("sample_attempt", 0) + 1
                detail = err[:120]
                if resp and resp != err:
                    detail += f" | response: {resp[:80]}"
                lines.append(f"      {sid} (attempt {attempts}): {detail}")
            if len(monitors) > 3:
                lines.append(f"      ... and {len(monitors) - 3} more")
        timeout_count = sum(1 for m in all_monitors if m is None)
        if timeout_count > 0:
            lines.append(f"    [timeout] ×{timeout_count} (exceeded {SAMPLE_TIMEOUT}s)")
        pprint("\n".join(lines))

    # Update checkpoint
    if checkpoint_path:
        rel_str = str(collector.rel_path)
        update_checkpoint(checkpoint_path, rel_str, success=True)

    # Release memory
    collector.samples = None
    collector.labels = None
    collector.monitors = None
    collector.completed = True

    return stats


async def run_one_file(input_path, output_dir, http_client, sem, model,
                       enable_arbitration=True, limit=0, shuffle=False,
                       file_prefix=None, progress=None, sample_task=None):
    """Label a single file. Writes outputs to output_dir. Returns stats dict.

    file_prefix: if set, output files are named e.g. labeled_<prefix>.json
                 instead of labeled.json (avoids name collisions in batch mode).
    """
    # Load input — streaming for JSONL
    samples, n_raw = iter_samples_from_file(input_path, limit=limit, shuffle=shuffle)

    total = len(samples)
    pprint = progress.console.print if progress else print
    pprint(f"  ({n_raw} conversations → {total} samples)")

    # Set up progress bar task — reset timer for this file
    if progress and sample_task is not None:
        progress.reset(sample_task, total=total, completed=0, visible=True, info="starting...")

    # Pre-allocate result slots
    all_labels = [None] * total
    all_monitors = [None] * total

    tasks = []
    for idx, sample in enumerate(samples):
        tasks.append(label_one(
            http_client, sample, model, idx, total, sem,
            enable_arbitration=enable_arbitration
        ))

    done_count = 0
    ok_count = 0
    fail_count = 0
    file_start = time.time()
    for coro in asyncio.as_completed(tasks):
        try:
            sample_idx, labels, monitor = await asyncio.wait_for(coro, timeout=SAMPLE_TIMEOUT)
        except asyncio.TimeoutError:
            done_count += 1
            fail_count += 1
            if progress and sample_task is not None:
                info = f"✓{ok_count}" + (f" ✗{fail_count}" if fail_count else "")
                progress.update(sample_task, advance=1, info=info)
            else:
                print(f"  [{done_count:4d}/{total}] ???                  | TIMEOUT ({SAMPLE_TIMEOUT}s)")
            continue

        all_labels[sample_idx] = labels
        all_monitors[sample_idx] = monitor
        done_count += 1

        if labels:
            ok_count += 1
        else:
            fail_count += 1

        if progress and sample_task is not None:
            info = f"✓{ok_count}" + (f" ✗{fail_count}" if fail_count else "")
            progress.update(sample_task, advance=1, info=info)
        else:
            # Fallback: per-sample print (no progress bar)
            sid = monitor["sample_id"]
            calls = monitor["llm_calls"]
            elapsed = monitor.get("elapsed_seconds", 0)
            status = monitor["status"]

            if labels:
                intent = labels.get("intent", "?")
                diff = labels.get("difficulty", "?")
                langs = ",".join(labels.get("language", [])[:3])
                n_tags = sum(
                    (len(labels[d]) if isinstance(labels.get(d), list) else (1 if labels.get(d) else 0))
                    for d in ["intent", "language", "domain", "concept", "task", "constraint", "agentic", "context", "difficulty"]
                )
                arb = " [ARB]" if monitor["arbitrated"] else ""
                print(f"  [{done_count:4d}/{total}] {sid:20s} | {calls} calls {elapsed:5.1f}s | {intent:6s} {diff:12s} | {langs:20s} | {n_tags:2d} tags{arb}")
            else:
                print(f"  [{done_count:4d}/{total}] {sid:20s} | {calls} calls {elapsed:5.1f}s | FAILED: {status}")

    file_elapsed = time.time() - file_start

    # Attach labels to samples
    for idx, sample in enumerate(samples):
        sample["labels"] = all_labels[idx]
        if all_monitors[idx]:
            sample["labeling_monitor"] = {
                "llm_calls": all_monitors[idx]["llm_calls"],
                "arbitrated": all_monitors[idx]["arbitrated"],
                "validation_issues": all_monitors[idx]["validation_issues"],
                "consistency_warnings": all_monitors[idx]["consistency_warnings"],
            }

    # Write outputs
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"_{file_prefix}" if file_prefix else ""

    labeled_json = f"labeled{suffix}.json"
    labeled_jsonl = f"labeled{suffix}.jsonl"
    monitor_file = f"monitor{suffix}.jsonl"
    stats_file = f"stats{suffix}.json"
    dashboard_file = f"dashboard{suffix}.html"
    failed_samples_file = f"failed_samples{suffix}.jsonl"

    with open(output_dir / labeled_json, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)

    with open(output_dir / labeled_jsonl, "w", encoding="utf-8") as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    with open(output_dir / monitor_file, "w", encoding="utf-8") as f:
        for m in all_monitors:
            if m:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

    # Write failed samples (original, without labels) for easy retry
    failed_indices = [i for i, l in enumerate(all_labels) if l is None]
    if failed_indices:
        with open(output_dir / failed_samples_file, "w", encoding="utf-8") as f:
            for i in failed_indices:
                s = dict(samples[i])
                s.pop("labels", None)
                s.pop("labeling_monitor", None)
                f.write(json.dumps(s, ensure_ascii=False) + "\n")

    # Write failure log
    if failed_indices:
        with open(output_dir / "failures.jsonl", "w", encoding="utf-8") as f:
            for i in failed_indices:
                m = all_monitors[i]
                record = {
                    "sample_id": samples[i].get("id", f"sample-{i}"),
                    "source_file": str(input_path),
                    "status": m["status"] if m else "timeout",
                    "error": (m.get("error", "") if m else f"exceeded {SAMPLE_TIMEOUT}s"),
                    "error_response": (m.get("error_response", "")[:200] if m else ""),
                    "attempts": (m.get("sample_attempt", 0) + 1 if m else 0),
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Compute and write stats
    valid_monitors = [m for m in all_monitors if m is not None]
    stats = compute_stats(valid_monitors, all_labels)
    stats["total_elapsed_seconds"] = round(file_elapsed, 1)
    stats["input_file"] = str(input_path)

    with open(output_dir / stats_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    # Per-file dashboard
    try:
        from tools.visualize_labels import generate_dashboard
        generate_dashboard(output_dir, labeled_file=labeled_json,
                           stats_file=stats_file, output_file=dashboard_file)
    except Exception:
        pass

    success = stats["success"]
    total_tokens = stats["total_tokens"]
    failed_count = total - success
    pprint(f"  ✓ {success}/{total} success, {file_elapsed:.1f}s, {total_tokens:,} tokens")

    # Print failure details for debugging — batch into single print to avoid progress bar flicker
    if failed_count > 0:
        lines = []
        failed_monitors = [m for m in all_monitors if m and m["status"] != "success"]
        # Group by error type
        error_groups = {}
        for m in failed_monitors:
            err_type = m["status"]
            error_groups.setdefault(err_type, []).append(m)
        lines.append(f"  ✗ {failed_count} failed:")
        for err_type, monitors in sorted(error_groups.items()):
            lines.append(f"    [{err_type}] ×{len(monitors)}")
            for m in monitors[:3]:  # show up to 3 per type
                sid = m.get("sample_id", "?")
                err = m.get("error", "")
                resp = m.get("error_response", "")
                attempts = m.get("sample_attempt", 0) + 1
                detail = err[:120]
                if resp and resp != err:
                    detail += f" | response: {resp[:80]}"
                lines.append(f"      {sid} (attempt {attempts}): {detail}")
            if len(monitors) > 3:
                lines.append(f"      ... and {len(monitors) - 3} more")
        # Count timeouts (samples with no monitor entry)
        timeout_count = sum(1 for m in all_monitors if m is None)
        if timeout_count > 0:
            lines.append(f"    [timeout] ×{timeout_count} (exceeded {SAMPLE_TIMEOUT}s)")
        pprint("\n".join(lines))

    return stats


async def run_directory_pipeline(dir_files, run_dir, args, model, concurrency,
                                 checkpoint_path, completed_set=None,
                                 progress=None, file_task=None, sample_task=None,
                                 http_client=None, sem=None, enable_arbitration=True):
    """Cross-file pipeline with watermark-based file loading.

    Instead of processing files serially, loads new files whenever in-flight
    task count drops below a watermark (concurrency * DIR_PIPELINE_WATERMARK).
    This keeps the semaphore saturated even when some files have long-tail
    samples in retry/backoff. Memory is bounded by DIR_PIPELINE_MAX_FILES.

    Returns list of per-file stats dicts.
    """
    watermark = int(concurrency * DIR_PIPELINE_WATERMARK)
    max_active = DIR_PIPELINE_MAX_FILES
    completed_set = completed_set or set()
    pprint = progress.console.print if progress else print

    # Separate already-completed files (for resume) from pending ones
    pending_files = []
    skipped_stats = []
    for i, (abs_path, rel_path) in enumerate(dir_files):
        rel_str = str(rel_path)
        if rel_str in completed_set:
            pprint(f"[File {i+1:3d}/{len(dir_files)}] {rel_str} — SKIPPED (completed)")
            # Load existing stats for summary
            file_out_dir = run_dir / rel_path.with_suffix("")
            prefix = rel_path.stem
            existing_stats = file_out_dir / f"stats_{prefix}.json"
            if existing_stats.exists():
                with open(existing_stats, "r", encoding="utf-8") as f:
                    skipped_stats.append(json.load(f))
            if progress and file_task is not None:
                progress.update(file_task, advance=1)
        else:
            pending_files.append((i, abs_path, rel_path))

    if not pending_files:
        return skipped_stats

    # --- Helper to wrap label_one with file/sample tracking + timeout ---
    async def _tagged_label(coro, file_idx, sample_idx):
        try:
            _, labels, monitor = await asyncio.wait_for(coro, timeout=SAMPLE_TIMEOUT)
            return file_idx, sample_idx, labels, monitor
        except asyncio.TimeoutError:
            return file_idx, sample_idx, None, None

    # --- Load a file into a FileCollector and submit its tasks ---
    def load_and_submit(file_entry, pending_futures):
        orig_idx, abs_path, rel_path = file_entry
        rel_str = str(rel_path)
        file_out_dir = run_dir / rel_path.with_suffix("")
        prefix = rel_path.stem

        pprint(f"[File {orig_idx+1:3d}/{len(dir_files)}] {rel_str}")
        samples, n_raw = iter_samples_from_file(
            abs_path, limit=args.limit, shuffle=args.shuffle)
        pprint(f"  ({n_raw} conversations → {len(samples)} samples)")

        collector = FileCollector(
            file_idx=orig_idx,
            abs_path=abs_path,
            rel_path=rel_path,
            output_dir=file_out_dir,
            prefix=prefix,
            total=len(samples),
            samples=samples,
        )

        # Update samples progress bar total
        if progress and sample_task is not None:
            current_total = progress.tasks[sample_task].total or 0
            progress.update(sample_task, total=current_total + len(samples), visible=True)

        # Submit all tasks
        for idx, sample in enumerate(samples):
            coro = label_one(
                http_client, sample, model, idx, len(samples), sem,
                enable_arbitration=enable_arbitration,
            )
            fut = asyncio.ensure_future(_tagged_label(coro, orig_idx, idx))
            pending_futures.add(fut)

        return collector

    # --- Try to load more files if below watermark and within memory limit ---
    def maybe_load_more(pending_futures, collectors, file_queue, next_to_load):
        active_count = sum(1 for c in collectors.values() if not c.completed)
        while (next_to_load < len(file_queue)
               and len(pending_futures) < watermark
               and active_count < max_active):
            entry = file_queue[next_to_load]
            next_to_load += 1
            new_c = load_and_submit(entry, pending_futures)
            collectors[new_c.file_idx] = new_c
            active_count += 1
        return next_to_load

    # --- Main loop: watermark-driven ---
    collectors = {}  # file_idx -> FileCollector
    pending_futures = set()
    all_file_stats = list(skipped_stats)
    file_queue = list(pending_files)
    next_to_load = 0

    if progress and sample_task is not None:
        progress.update(sample_task, total=0, completed=0, visible=True, info="starting...")

    # Initial load
    next_to_load = maybe_load_more(pending_futures, collectors, file_queue, next_to_load)

    if progress and file_task is not None:
        active_names = [str(c.rel_path) for c in collectors.values() if not c.completed]
        progress.update(file_task, info=", ".join(active_names)[:60])

    # Process results as they complete
    while pending_futures:
        done, pending_futures = await asyncio.wait(
            pending_futures, return_when=asyncio.FIRST_COMPLETED)

        for fut in done:
            file_idx, sample_idx, labels, monitor = fut.result()
            c = collectors[file_idx]

            if 0 <= sample_idx < c.total:
                c.labels[sample_idx] = labels
                c.monitors[sample_idx] = monitor

            c.done += 1
            if labels:
                c.ok += 1
            else:
                c.fail += 1

            # Update samples progress bar
            if progress and sample_task is not None:
                info = f"✓{c.ok}" + (f" ✗{c.fail}" if c.fail else "") + f" [{c.rel_path.name}]"
                progress.update(sample_task, advance=1, info=info)

            # Check if this file is fully done
            if c.done >= c.total and not c.completed:
                stats = flush_file_output(c, run_dir, checkpoint_path, pprint=pprint)
                all_file_stats.append(stats)

                if progress and file_task is not None:
                    progress.update(file_task, advance=1)

        # After processing batch of completions, check if we should load more files
        next_to_load = maybe_load_more(pending_futures, collectors, file_queue, next_to_load)

        if progress and file_task is not None:
            active_names = [str(cc.rel_path) for cc in collectors.values()
                            if not cc.completed]
            progress.update(file_task, info=", ".join(active_names)[:60] if active_names else "done")

    # Handle any files with 0 samples (edge case)
    for c in collectors.values():
        if not c.completed and c.total == 0:
            stats = flush_file_output(c, run_dir, checkpoint_path, pprint=pprint)
            all_file_stats.append(stats)
            if progress and file_task is not None:
                progress.update(file_task, advance=1)

    return all_file_stats


def print_summary(stats, run_dir, is_batch=False):
    """Print final summary to stdout."""
    print(f"\n{'='*80}")
    label = "BATCH LABELING COMPLETE" if is_batch else "LABELING COMPLETE"
    elapsed = stats.get('total_elapsed_seconds', 0)
    print(f"{label} in {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print(f"{'='*80}")
    if is_batch:
        print(f"Files:       {stats.get('files_processed', '?')}")
    print(f"Success:     {stats['success']}/{stats['total_samples']} ({stats.get('success_rate', 0)*100:.1f}%)")
    print(f"LLM calls:   {stats['total_llm_calls']} total, {stats.get('avg_calls_per_sample', 0):.1f} avg/sample")
    print(f"Tokens:      {stats['total_tokens']:,}")
    print(f"Arbitrated:  {stats['arbitrated_count']} ({stats.get('arbitrated_rate', 0)*100:.1f}%)")
    print(f"Unmapped:    {stats.get('unmapped_unique_count', 0)} unique out-of-pool tags")
    total_samples = stats.get('total_samples', 0)
    if elapsed > 0 and total_samples > 0:
        print(f"Throughput:  {total_samples / elapsed:.1f} samples/sec")

    print(f"\nConfidence (mean):")
    for dim, cs in stats.get("confidence_stats", {}).items():
        bar = "█" * int(cs["mean"] * 20)
        print(f"  {dim:15s} {cs['mean']:.3f} {bar}")

    print(f"\nTop distributions:")
    for dim in ["intent", "difficulty", "domain", "concept"]:
        dist = stats.get("tag_distributions", {}).get(dim, {})
        top5 = list(dist.items())[:5]
        top_str = ", ".join(f"{k}({v})" for k, v in top5)
        print(f"  {dim:15s} {top_str}")

    if stats.get("unmapped_tags"):
        print(f"\nUnmapped tags (top 10):")
        for tag, count in list(stats["unmapped_tags"].items())[:10]:
            print(f"  {tag}: {count}")

    print(f"\nRun dir: {run_dir}")


def _write_global_summary(all_file_stats, run_dir, input_path, model, concurrency, batch_start):
    """Write global summary stats + dashboard for a batch run."""
    batch_elapsed = time.time() - batch_start
    summary = merge_stats(all_file_stats) if all_file_stats else {
        "total_samples": 0, "success": 0, "failed": 0, "success_rate": 0,
        "total_llm_calls": 0, "total_tokens": 0, "arbitrated_count": 0,
        "unmapped_unique_count": 0, "tag_distributions": {}, "unmapped_tags": {},
        "files_processed": 0,
    }
    summary["model"] = model
    summary["concurrency"] = concurrency
    summary["total_elapsed_seconds"] = round(batch_elapsed, 1)
    summary["timestamp"] = datetime.now().isoformat()
    summary["input_path"] = str(input_path)
    summary["run_dir"] = str(run_dir)

    with open(run_dir / "summary_stats.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    input_name = input_path.name
    global_dashboard = f"dashboard_{input_name}.html"
    try:
        from tools.visualize_labels import generate_dashboard
        generate_dashboard(run_dir, labeled_file=None,
                           stats_file="summary_stats.json",
                           output_file=global_dashboard)
        print(f"\nGlobal dashboard generated: {run_dir / global_dashboard}")
    except Exception as e:
        print(f"\nGlobal dashboard generation skipped: {e}")

    print_summary(summary, run_dir, is_batch=True)


async def run_pipeline(args):
    # ── Resume mode ──────────────────────────────────────
    if args.resume:
        run_dir = Path(args.resume)
        if not run_dir.is_dir():
            print(f"Error: --resume path does not exist: {run_dir}")
            sys.exit(1)
        checkpoint_path = run_dir / "checkpoint.json"
        ckpt = load_checkpoint(checkpoint_path)
        if ckpt is None:
            print(f"Error: no checkpoint.json in {run_dir}")
            sys.exit(1)
        if ckpt.get("status") == "done":
            print(f"All files already completed in {run_dir}")
            return

        # Recover settings from summary_stats or checkpoint
        summary_path = run_dir / "summary_stats.json"
        if summary_path.exists():
            with open(summary_path, "r", encoding="utf-8") as f:
                prev_summary = json.load(f)
            input_path = Path(prev_summary.get("input_path", args.input))
            model = prev_summary.get("model", args.model)
        else:
            input_path = Path(args.input)
            model = args.model

        files = discover_input_files(input_path)
        dir_files = [(a, r) for a, r in files if r is not None]
        if not dir_files:
            print("Error: --resume only works with directory-mode runs")
            sys.exit(1)

        completed = set(ckpt.get("completed", []))
        concurrency = args.concurrency

        print(f"{'='*80}")
        print(f"SFT Auto-Labeling Pipeline — RESUME")
        print(f"{'='*80}")
        print(f"Run dir:     {run_dir}")
        print(f"Model:       {model}")
        print(f"Completed:   {len(completed)}/{len(dir_files)} files")
        print(f"Concurrency: {concurrency}")
        print(f"{'='*80}\n")

        batch_start = time.time()

        async with httpx.AsyncClient(
            proxy=None,
            timeout=REQUEST_TIMEOUT,
            limits=httpx.Limits(
                max_connections=concurrency + 10,
                max_keepalive_connections=concurrency,
            ),
        ) as http_client:
            sem = asyncio.Semaphore(concurrency)
            n = len(dir_files)
            with create_progress() as progress:
                file_task = progress.add_task("Files", total=n, info="")
                sample_task = progress.add_task("Samples", total=0, visible=False, info="starting...")
                all_file_stats = await run_directory_pipeline(
                    dir_files, run_dir, args, model, concurrency,
                    checkpoint_path, completed_set=completed,
                    progress=progress, file_task=file_task, sample_task=sample_task,
                    http_client=http_client, sem=sem,
                    enable_arbitration=not args.no_arbitration,
                )

        # Write global summary
        _write_global_summary(all_file_stats, run_dir, input_path, model, concurrency, batch_start)
        return

    # ── Normal mode ──────────────────────────────────────
    input_path = Path(args.input)
    files = discover_input_files(input_path)
    is_directory = input_path.is_dir()

    # Determine output directory
    run_dir = resolve_run_dir(args, input_path)
    run_dir.mkdir(parents=True, exist_ok=True)

    concurrency = args.concurrency

    print(f"{'='*80}")
    print(f"SFT Auto-Labeling Pipeline (Concurrent)")
    print(f"{'='*80}")
    print(f"Input:       {input_path} ({'directory, ' + str(len(files)) + ' files' if is_directory else 'single file'})")
    print(f"Model:       {args.model}")
    print(f"Run dir:     {run_dir}")
    print(f"Concurrency: {concurrency}")
    print(f"Arbitration: {'disabled' if args.no_arbitration else f'enabled (threshold={CONFIDENCE_THRESHOLD})'}")
    print(f"Started:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    if is_directory:
        # ── Directory mode: cross-file pipeline ──
        dir_files = [(a, r) for a, r in files if r is not None]
        if not dir_files:
            print("No .json/.jsonl files found in directory")
            sys.exit(1)

        checkpoint_path = run_dir / "checkpoint.json"
        create_checkpoint(checkpoint_path, dir_files)
        batch_start = time.time()

        async with httpx.AsyncClient(
            proxy=None,
            timeout=REQUEST_TIMEOUT,
            limits=httpx.Limits(
                max_connections=concurrency + 10,
                max_keepalive_connections=concurrency,
            ),
        ) as http_client:
            sem = asyncio.Semaphore(concurrency)
            n = len(dir_files)
            with create_progress() as progress:
                file_task = progress.add_task("Files", total=n, info="")
                sample_task = progress.add_task("Samples", total=0, visible=False, info="starting...")
                all_file_stats = await run_directory_pipeline(
                    dir_files, run_dir, args, args.model, concurrency,
                    checkpoint_path,
                    progress=progress, file_task=file_task, sample_task=sample_task,
                    http_client=http_client, sem=sem,
                    enable_arbitration=not args.no_arbitration,
                )

        _write_global_summary(all_file_stats, run_dir, input_path, args.model, concurrency, batch_start)

    else:
        # ── Single-file mode: backward compatible ────────
        batch_start = time.time()
        async with httpx.AsyncClient(
            proxy=None,
            timeout=REQUEST_TIMEOUT,
            limits=httpx.Limits(
                max_connections=concurrency + 10,
                max_keepalive_connections=concurrency,
            ),
        ) as http_client:
            sem = asyncio.Semaphore(concurrency)
            with create_progress() as progress:
                sample_task = progress.add_task("Labeling", total=None, info="starting...")
                stats = await run_one_file(
                    input_path, run_dir, http_client, sem, args.model,
                    enable_arbitration=not args.no_arbitration,
                    limit=args.limit, shuffle=args.shuffle,
                    progress=progress, sample_task=sample_task,
                )

        stats["model"] = args.model
        stats["concurrency"] = concurrency
        stats["timestamp"] = datetime.now().isoformat()
        stats["run_dir"] = str(run_dir)

        # Overwrite stats with enriched version
        with open(run_dir / "stats.json", "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

        print_summary(stats, run_dir)
        print(f"Output:  {run_dir / 'labeled.json'}")
        print(f"JSONL:   {run_dir / 'labeled.jsonl'}")
        print(f"Stats:   {run_dir / 'stats.json'}")
        print(f"Monitor: {run_dir / 'monitor.jsonl'}")


def main():
    parser = argparse.ArgumentParser(description="SFT Auto-Labeling Pipeline (Concurrent)")
    parser.add_argument("--input", type=str, default=str(DEFAULT_INPUT))
    parser.add_argument("--output", type=str, default=None,
                        help="Output directory: omit for sibling of input, 'runs' for labeling/data/runs/, or an explicit path")
    parser.add_argument("--resume", type=str, default=None,
                        help="Resume from an existing run directory (reads checkpoint.json)")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    parser.add_argument("--limit", type=int, default=0,
                        help="Max samples per file (0 = all). In directory mode, applies to each file independently")
    parser.add_argument("--shuffle", action="store_true", help="Randomly shuffle samples before slicing")
    parser.add_argument("--no-arbitration", action="store_true")
    args = parser.parse_args()
    asyncio.run(run_pipeline(args))


if __name__ == "__main__":
    main()
