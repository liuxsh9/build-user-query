"""
SFT Auto-Labeling Pipeline — Concurrent Version

Processes SFT data through the labeling pipeline with high concurrency:
  1. Preprocessing (structural signal extraction) — local, instant
  2. Call 1 — Intent, Language, Domain, Task, Difficulty — concurrent LLM
  3. Call 2 — Concept, Agentic, Constraint, Context — concurrent LLM (depends on Call 1)
  4. Validation — local, instant
  5. Optional arbitration for low-confidence labels — concurrent LLM

Usage:
  python3 labeling/pipeline.py [--input FILE] [--output FILE] [--model MODEL] [--concurrency N]
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
    DEFAULT_MODEL, DEFAULT_CONCURRENCY, MAX_RETRIES, SAMPLE_MAX_RETRIES, REQUEST_TIMEOUT,
)


# ─────────────────────────────────────────────────────────
# Async LLM calls
# ─────────────────────────────────────────────────────────

async def async_llm_call(http_client, messages, model, temperature=0.1, max_tokens=1000, max_retries=MAX_RETRIES):
    """Async LLM call with retry. Returns (parsed_json, raw_content, usage)."""
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
                # Rate limited or server error — back off
                wait = min(2 ** attempt * 3 + 2, 60)
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
                await asyncio.sleep(1)
                continue
            return None, content if 'content' in dir() else "", {"prompt_tokens": 0, "completion_tokens": 0, "error": last_error}
        except Exception as e:
            last_error = f"{type(e).__name__}: {e}"
            if attempt < max_retries:
                wait = min(2 ** attempt * 3 + 2, 60)
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
            # Back off before retry, outside semaphore so we don't block others
            await asyncio.sleep(2 ** sample_attempt * 2)

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


async def run_pipeline(args):
    input_path = Path(args.input)

    # Create run directory: labeling/data/runs/<timestamp>_<model>/
    run_ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_short = args.model.replace("/", "-")
    run_dir = DATA_DIR / "runs" / f"{run_ts}_{model_short}"
    run_dir.mkdir(parents=True, exist_ok=True)

    output_path = run_dir / "labeled.json"
    jsonl_path = run_dir / "labeled.jsonl"
    stats_path = run_dir / "stats.json"
    monitor_path = run_dir / "monitor.jsonl"

    # Load input (JSON array or JSONL)
    with open(input_path, "r", encoding="utf-8") as f:
        if input_path.suffix == ".jsonl":
            samples = [json.loads(line) for line in f if line.strip()]
        else:
            samples = json.load(f)

    # Normalize and slice multi-turn into training-aligned samples
    raw_samples = samples
    samples = []
    for s in raw_samples:
        samples.extend(normalize_and_slice(s))
    # Assign IDs if missing
    for i, s in enumerate(samples):
        if not s.get("id"):
            s["id"] = f"sample-{i:04d}"

    if args.shuffle:
        random.shuffle(samples)

    if args.limit > 0:
        samples = samples[:args.limit]

    total = len(samples)
    concurrency = args.concurrency

    print(f"{'='*80}")
    print(f"SFT Auto-Labeling Pipeline (Concurrent)")
    print(f"{'='*80}")
    n_raw = len(raw_samples)
    print(f"Input:       {input_path} ({n_raw} conversations → {total} samples)")
    print(f"Model:       {args.model}")
    print(f"Run dir:     {run_dir}")
    print(f"Concurrency: {concurrency}")
    print(f"Arbitration: {'disabled' if args.no_arbitration else f'enabled (threshold={CONFIDENCE_THRESHOLD})'}")
    print(f"Started:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    sem = asyncio.Semaphore(concurrency)
    start_time = time.time()

    # Pre-allocate result slots
    all_labels = [None] * total
    all_monitors = [None] * total

    async with httpx.AsyncClient(
        proxy=None,
        timeout=REQUEST_TIMEOUT,
        limits=httpx.Limits(
            max_connections=concurrency + 10,
            max_keepalive_connections=concurrency,
        ),
    ) as http_client:
        tasks = []
        for idx, sample in enumerate(samples):
            tasks.append(label_one(
                http_client, sample, args.model, idx, total, sem,
                enable_arbitration=not args.no_arbitration
            ))

        done_count = 0
        for coro in asyncio.as_completed(tasks):
            sample_idx, labels, monitor = await coro
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
                print(f"[{done_count:4d}/{total}] {sid:20s} | {calls} calls {elapsed:5.1f}s | {intent:6s} {diff:12s} | {langs:20s} | {n_tags:2d} tags{arb}")
            else:
                print(f"[{done_count:4d}/{total}] {sid:20s} | {calls} calls {elapsed:5.1f}s | FAILED: {status}")

    total_elapsed = time.time() - start_time

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

    # Save labeled JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)

    # Save labeled JSONL (one sample per line, original structure + labels)
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")

    # Save monitor log
    with open(monitor_path, "w", encoding="utf-8") as f:
        for m in all_monitors:
            if m:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

    # Stats
    valid_monitors = [m for m in all_monitors if m is not None]
    stats = compute_stats(valid_monitors, all_labels)
    stats["model"] = args.model
    stats["concurrency"] = concurrency
    stats["total_elapsed_seconds"] = round(total_elapsed, 1)
    stats["timestamp"] = datetime.now().isoformat()
    stats["input_file"] = str(input_path)
    stats["run_dir"] = str(run_dir)

    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    # Print summary
    print(f"\n{'='*80}")
    print(f"LABELING COMPLETE in {total_elapsed:.1f}s ({total_elapsed/60:.1f} min)")
    print(f"{'='*80}")
    print(f"Success:     {stats['success']}/{stats['total_samples']} ({stats['success_rate']*100:.1f}%)")
    print(f"LLM calls:   {stats['total_llm_calls']} total, {stats['avg_calls_per_sample']:.1f} avg/sample")
    print(f"Tokens:      {stats['total_tokens']:,}")
    print(f"Arbitrated:  {stats['arbitrated_count']} ({stats['arbitrated_rate']*100:.1f}%)")
    print(f"Unmapped:    {stats['unmapped_unique_count']} unique out-of-pool tags")
    print(f"Throughput:  {total / total_elapsed:.1f} samples/sec")

    print(f"\nConfidence (mean):")
    for dim, cs in stats.get("confidence_stats", {}).items():
        bar = "█" * int(cs["mean"] * 20)
        print(f"  {dim:15s} {cs['mean']:.3f} {bar}")

    print(f"\nTop distributions:")
    for dim in ["intent", "difficulty", "domain", "concept"]:
        dist = stats["tag_distributions"].get(dim, {})
        top5 = list(dist.items())[:5]
        top_str = ", ".join(f"{k}({v})" for k, v in top5)
        print(f"  {dim:15s} {top_str}")

    if stats.get("unmapped_tags"):
        print(f"\nUnmapped tags (top 10):")
        for tag, count in list(stats["unmapped_tags"].items())[:10]:
            print(f"  {tag}: {count}")

    # Generate dashboard
    try:
        from tools.visualize_labels import generate_dashboard
        dashboard_path = generate_dashboard(run_dir)
        print(f"\nDashboard generated: {dashboard_path}")
    except Exception as e:
        print(f"\nDashboard generation skipped: {e}")

    print(f"\nRun dir: {run_dir}")
    print(f"Output:  {output_path}")
    print(f"JSONL:   {jsonl_path}")
    print(f"Stats:   {stats_path}")
    print(f"Monitor: {monitor_path}")


def main():
    parser = argparse.ArgumentParser(description="SFT Auto-Labeling Pipeline (Concurrent)")
    parser.add_argument("--input", type=str, default=str(DEFAULT_INPUT))
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--shuffle", action="store_true", help="Randomly shuffle samples before slicing")
    parser.add_argument("--no-arbitration", action="store_true")
    args = parser.parse_args()
    asyncio.run(run_pipeline(args))


if __name__ == "__main__":
    main()
