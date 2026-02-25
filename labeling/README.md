# SFT Auto-Labeling Pipeline

Automated labeling pipeline for SFT code-generation training data, using a structured 9-category taxonomy (v3.1, 221 tags).

## Architecture

Two-call pipeline with optional arbitration:

```
Input (ShareGPT JSON)
  │
  ├─ Preprocessing: extract structural signals (languages, tool roles, code blocks)
  │
  ├─ Call 1 (LLM): Intent, Language, Domain, Task, Difficulty
  │
  ├─ Call 2 (LLM): Concept, Agentic, Constraint, Context  (receives Call 1 results)
  │
  ├─ Validation: tag pool check, cross-dimension consistency
  │
  ├─ Arbitration (optional): re-run low-confidence dimensions at higher temperature
  │
  └─ Output: labeled JSON/JSONL + stats + monitor log
```

## Directory Structure

```
labeling/
  config.py              # Production settings (API, model, concurrency, thresholds)
  pipeline.py            # Main concurrent labeling pipeline
  prompts.py             # Call 1 & Call 2 prompts, tag pools, few-shot examples
  preprocessing.py       # Structural signal extraction
  tools/
    export_review.py     # Labeled JSON → review CSV for human audit
    analyze_unmapped.py  # Unmapped tag frequency analysis for pool iteration
    compare_models.py    # Multi-model comparison report
    generate_report.py   # Labeling summary report
    collect_gold_set.py  # Gold set conversation generator
  data/
    raw_samples.json     # 108 source conversations (97 single-turn + 11 agentic)
    baselines/           # Frozen v4 baselines (deepseek + sonnet)
    reports/             # Analysis documents
    runs/                # Per-run output (auto-created by pipeline)
  README.md
```

## Configuration

All production settings are in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `LITELLM_BASE` | `http://101.47.36.53:4000/v1` | LiteLLM proxy endpoint |
| `LITELLM_KEY` | `sk-...` | API key |
| `DEFAULT_MODEL` | `deepseek-v3.2` | Production labeling model |
| `DEFAULT_CONCURRENCY` | `30` | Concurrent LLM requests |
| `CONFIDENCE_THRESHOLD` | `0.65` | Below this triggers arbitration |
| `MAX_RETRIES` | `3` | LLM call retry count |
| `REQUEST_TIMEOUT` | `180` | Per-request timeout (seconds) |

### Model Tiers

| Tier | Models | Use Case |
|------|--------|----------|
| Strong | claude-opus-4.5-thinking, gpt-5, gemini-2.5-pro-thinking | Gold set annotation |
| Mid | claude-sonnet-4.6, deepseek-v3.2, qwen3-235b | Production labeling |
| Light | gpt-4o-mini, deepseek-v3.1 | Cost-sensitive batches |

## Input Format

Pipeline accepts a JSON array of ShareGPT-format conversations:

```json
[
  {
    "id": "gen-0000",
    "conversations": [
      { "from": "human", "value": "Python 列表推导式和生成器表达式的区别？" },
      { "from": "gpt", "value": "列表推导式和生成器表达式都是..." }
    ],
    "metadata": {                    // optional, used by preprocessing
      "source": "generated",
      "est_tokens": 687,
      "num_turns": 2,
      "is_multi_turn": false,
      "has_tool_calls": false,
      "has_code": true
    }
  }
]
```

| Field | Required | Description |
|-------|----------|-------------|
| `id` | yes | Unique sample identifier |
| `conversations` | yes | Array of `{from, value}` turns. `from` is `"human"` or `"gpt"` |
| `metadata` | no | Preprocessing hints (auto-detected if absent) |

Conversations can be single-turn (1 human + 1 gpt) or multi-turn. The pipeline extracts structural signals (languages, code blocks, tool calls) from all turns during preprocessing.

## Quick Start

```bash
# Label 20 random samples
python3 labeling/pipeline.py --limit 20 --shuffle

# Full dataset (108 samples, ~15 min)
python3 labeling/pipeline.py --concurrency 50

# Export review CSV from a run
python3 labeling/tools/export_review.py \
  --input labeling/data/runs/<run_dir>/labeled.json \
  --monitor labeling/data/runs/<run_dir>/monitor.jsonl \
  --output labeling/data/runs/<run_dir>/review.csv

# Analyze unmapped tags for pool iteration
python3 labeling/tools/analyze_unmapped.py labeling/data/runs/<run_dir>/labeled.json
```

## Pipeline CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--input` | `labeling/data/raw_samples.json` | Input ShareGPT JSON |
| `--model` | `deepseek-v3.2` | Model ID (must be available via LiteLLM) |
| `--concurrency` | `30` | Max parallel LLM requests |
| `--limit` | `0` (all) | Process only first N samples |
| `--shuffle` | off | Randomly shuffle before slicing |
| `--no-arbitration` | off | Skip arbitration pass |

## Output

Each run creates a timestamped directory under `data/runs/`:

```
data/runs/20260225_155440_deepseek-v3.2/
  labeled.json      # Full samples with .labels and .labeling_monitor
  labeled.jsonl     # One sample per line (same data, streaming-friendly)
  stats.json        # Aggregate metrics, distributions, confidence stats
  monitor.jsonl     # Per-sample trace (calls, tokens, latency, issues)
```

## Production Tuning

### Concurrency

- **30** (default): Safe for most LLM providers, avoids 429 rate limits
- **50**: Works well with DeepSeek v3.2 via LiteLLM proxy
- **100+**: Only if provider supports it; monitor for 429/503 errors

### Arbitration

Arbitration re-runs dimensions with confidence below `CONFIDENCE_THRESHOLD` (0.65) at temperature 0.3. In practice with deepseek-v3.2 + v4 prompts, arbitration triggers ~0% of the time.

To disable: `--no-arbitration`

### Cost Estimate

Per sample (2 calls, no arbitration):
- ~10K prompt tokens + ~400 completion tokens
- deepseek-v3.2: ~$0.002/sample
- 108 samples full run: ~$0.22

## Baselines

| File | Description |
|------|-------------|
| `baselines/labeled_deepseek_v4.json` | Production baseline (deepseek-v3.2, 0 unmapped) |
| `baselines/stats_deepseek_v4.json` | Stats for deepseek baseline |
| `baselines/labeled_sonnet_v4.json` | Gold standard reference (claude-sonnet-4.6) |
| `baselines/stats_sonnet_v4.json` | Stats for sonnet baseline |
