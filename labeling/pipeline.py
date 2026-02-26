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

import httpx

sys.path.insert(0, str(Path(__file__).parent))
from prompts import (
    CALL1_SYSTEM, CALL1_FEWSHOT, CALL2_SYSTEM, CALL2_FEWSHOT,
    TAG_POOLS, SINGLE_SELECT, MULTI_SELECT
)
from preprocessing import preprocess, format_signals_for_prompt, normalize_and_slice
from config import (
    LITELLM_BASE, LITELLM_KEY, CONFIDENCE_THRESHOLD, CONSISTENCY_RULES,
    DEFAULT_INPUT, DEFAULT_OUTPUT, DATA_DIR,
    DEFAULT_MODEL, DEFAULT_CONCURRENCY, MAX_RETRIES, SAMPLE_MAX_RETRIES,
    REQUEST_TIMEOUT, SAMPLE_TIMEOUT,
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

    # Sort distributions and unmapped
    for dim in merged["tag_distributions"]:
        merged["tag_distributions"][dim] = dict(sorted(merged["tag_distributions"][dim].items(), key=lambda x: -x[1]))
    merged["unmapped_tags"] = dict(sorted(merged["unmapped_tags"].items(), key=lambda x: -x[1]))
    merged["unmapped_unique_count"] = len(merged["unmapped_tags"])

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
            if resp.status_code in (429, 502, 503):
                # Rate limited or server error — exponential backoff with jitter
                base_wait = min(2 ** attempt * 3 + 2, 60)
                wait = base_wait + random.uniform(0, base_wait * 0.5)
                last_error = f"HTTP {resp.status_code}: {resp.text[:200]}"
                if attempt < max_retries:
                    await asyncio.sleep(wait)
                    continue
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
                # Preprocess
                signals = preprocess(sample)
                signals_str = format_signals_for_prompt(signals)
                conversations_json = json.dumps(sample["conversations"], ensure_ascii=False)

                # Call 1
                msgs1 = build_call1_messages(conversations_json, signals_str)
                call1_result, _, usage1 = await async_llm_call(http_client, msgs1, model)
                monitor["llm_calls"] += 1
                monitor["total_prompt_tokens"] += usage1["prompt_tokens"]
                monitor["total_completion_tokens"] += usage1["completion_tokens"]

                if call1_result is None:
                    monitor["status"] = "call1_failed"
                    monitor["error"] = usage1.get("error", "unknown")
                    if sample_attempt < SAMPLE_MAX_RETRIES:
                        continue
                    return sample_idx, None, monitor

                call1_cleaned, call1_issues = validate_tags(call1_result, "call1")
                monitor["validation_issues"].extend(call1_issues)

                # Call 2 (depends on Call 1)
                call1_context = {d: call1_cleaned[d] for d in ["intent", "language", "domain", "task", "difficulty"] if d in call1_cleaned}
                msgs2 = build_call2_messages(conversations_json, signals_str, call1_context)
                call2_result, _, usage2 = await async_llm_call(http_client, msgs2, model)
                monitor["llm_calls"] += 1
                monitor["total_prompt_tokens"] += usage2["prompt_tokens"]
                monitor["total_completion_tokens"] += usage2["completion_tokens"]

                if call2_result is None:
                    monitor["status"] = "call2_failed"
                    monitor["error"] = usage2.get("error", "unknown")
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
            }

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
    }


async def run_one_file(input_path, output_dir, http_client, sem, model,
                       enable_arbitration=True, limit=0, shuffle=False,
                       file_prefix=None):
    """Label a single file. Writes outputs to output_dir. Returns stats dict.

    file_prefix: if set, output files are named e.g. labeled_<prefix>.json
                 instead of labeled.json (avoids name collisions in batch mode).
    """
    # Load input
    with open(input_path, "r", encoding="utf-8") as f:
        if str(input_path).endswith(".jsonl"):
            raw_samples = [json.loads(line) for line in f if line.strip()]
        else:
            raw_samples = json.load(f)

    # Normalize and slice
    samples = []
    for s in raw_samples:
        samples.extend(normalize_and_slice(s))
    for i, s in enumerate(samples):
        if not s.get("id"):
            s["id"] = f"sample-{i:04d}"

    if shuffle:
        random.shuffle(samples)
    if limit > 0:
        samples = samples[:limit]

    total = len(samples)
    n_raw = len(raw_samples)
    print(f"  ({n_raw} conversations → {total} samples)")

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
    file_start = time.time()
    for coro in asyncio.as_completed(tasks):
        try:
            sample_idx, labels, monitor = await asyncio.wait_for(coro, timeout=SAMPLE_TIMEOUT)
        except asyncio.TimeoutError:
            # Sample timed out — find which one by elimination
            done_count += 1
            print(f"  [{done_count:4d}/{total}] ???                  | TIMEOUT ({SAMPLE_TIMEOUT}s)")
            continue

        all_labels[sample_idx] = labels
        all_monitors[sample_idx] = monitor
        done_count += 1

        # Print progress
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

    with open(output_dir / labeled_json, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)

    with open(output_dir / labeled_jsonl, "w", encoding="utf-8") as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    with open(output_dir / monitor_file, "w", encoding="utf-8") as f:
        for m in all_monitors:
            if m:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

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
    print(f"  ✓ {success}/{total} success, {file_elapsed:.1f}s, {total_tokens:,} tokens")

    return stats


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
        # Filter to directory-mode files only (those with rel_path)
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

        all_file_stats = []
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
            for i, (abs_path, rel_path) in enumerate(dir_files):
                rel_str = str(rel_path)
                if rel_str in completed:
                    print(f"[File {i+1:3d}/{n}] {rel_str} — SKIPPED (completed)")
                    # Load existing stats for summary
                    file_out_dir = run_dir / rel_path.with_suffix("")
                    prefix = rel_path.stem
                    existing_stats = file_out_dir / f"stats_{prefix}.json"
                    if existing_stats.exists():
                        with open(existing_stats, "r", encoding="utf-8") as f:
                            all_file_stats.append(json.load(f))
                    continue

                file_out_dir = run_dir / rel_path.with_suffix("")
                prefix = rel_path.stem
                print(f"[File {i+1:3d}/{n}] {rel_str}")
                try:
                    stats = await run_one_file(
                        abs_path, file_out_dir, http_client, sem, model,
                        enable_arbitration=not args.no_arbitration,
                        limit=args.limit, shuffle=args.shuffle,
                        file_prefix=prefix,
                    )
                    all_file_stats.append(stats)
                    update_checkpoint(checkpoint_path, rel_str, success=True)
                except Exception as e:
                    print(f"  ✗ FAILED: {e}")
                    update_checkpoint(checkpoint_path, rel_str, success=False, error_msg=str(e)[:200])

        # Write global summary
        if all_file_stats:
            summary = merge_stats(all_file_stats)
            summary["model"] = model
            summary["concurrency"] = concurrency
            summary["total_elapsed_seconds"] = round(time.time() - batch_start, 1)
            summary["timestamp"] = datetime.now().isoformat()
            summary["input_path"] = str(input_path)
            summary["run_dir"] = str(run_dir)
            with open(run_dir / "summary_stats.json", "w", encoding="utf-8") as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            try:
                from tools.visualize_labels import generate_dashboard
                generate_dashboard(run_dir, labeled_file=None,
                                   stats_file="summary_stats.json")
            except Exception as e:
                print(f"  Global dashboard generation skipped: {e}")
            print_summary(summary, run_dir, is_batch=True)
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
        # ── Directory mode: file-serial, sample-concurrent ──
        dir_files = [(a, r) for a, r in files if r is not None]
        if not dir_files:
            print("No .json/.jsonl files found in directory")
            sys.exit(1)

        checkpoint_path = run_dir / "checkpoint.json"
        ckpt = create_checkpoint(checkpoint_path, dir_files)
        all_file_stats = []
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
            for i, (abs_path, rel_path) in enumerate(dir_files):
                rel_str = str(rel_path)
                file_out_dir = run_dir / rel_path.with_suffix("")
                prefix = rel_path.stem
                print(f"[File {i+1:3d}/{n}] {rel_str}")
                try:
                    stats = await run_one_file(
                        abs_path, file_out_dir, http_client, sem, args.model,
                        enable_arbitration=not args.no_arbitration,
                        limit=args.limit, shuffle=args.shuffle,
                        file_prefix=prefix,
                    )
                    all_file_stats.append(stats)
                    update_checkpoint(checkpoint_path, rel_str, success=True)
                except Exception as e:
                    print(f"  ✗ FAILED: {e}")
                    update_checkpoint(checkpoint_path, rel_str, success=False, error_msg=str(e)[:200])

        # Write global summary
        batch_elapsed = time.time() - batch_start
        summary = merge_stats(all_file_stats) if all_file_stats else {
            "total_samples": 0, "success": 0, "failed": 0, "success_rate": 0,
            "total_llm_calls": 0, "total_tokens": 0, "arbitrated_count": 0,
            "unmapped_unique_count": 0, "tag_distributions": {}, "unmapped_tags": {},
            "files_processed": 0,
        }
        summary["model"] = args.model
        summary["concurrency"] = concurrency
        summary["total_elapsed_seconds"] = round(batch_elapsed, 1)
        summary["timestamp"] = datetime.now().isoformat()
        summary["input_path"] = str(input_path)
        summary["run_dir"] = str(run_dir)

        with open(run_dir / "summary_stats.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        # Global dashboard — stats-only mode (no labeled.json at root)
        try:
            from tools.visualize_labels import generate_dashboard
            generate_dashboard(run_dir, labeled_file=None,
                               stats_file="summary_stats.json")
            print(f"\nGlobal dashboard generated: {run_dir / 'dashboard.html'}")
        except Exception as e:
            print(f"\nGlobal dashboard generation skipped: {e}")

        print_summary(summary, run_dir, is_batch=True)

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
            stats = await run_one_file(
                input_path, run_dir, http_client, sem, args.model,
                enable_arbitration=not args.no_arbitration,
                limit=args.limit, shuffle=args.shuffle,
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
