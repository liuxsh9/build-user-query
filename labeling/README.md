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
  └─ Output: labeled JSON + stats + monitor log
```

## Configuration

All production settings are in **`config.py`**:

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

## Quick Start

```bash
# Label 20 random samples
python3 labeling/pipeline.py \
  --input labeling/data/raw_samples.json \
  --output labeling/data/labeled_output.json \
  --limit 20 --shuffle

# Full dataset (108 samples, ~15 min)
python3 labeling/pipeline.py \
  --input labeling/data/raw_samples.json \
  --output labeling/data/labeled_output.json \
  --concurrency 50

# Export review CSV for human audit
python3 labeling/export_review.py \
  --input labeling/data/labeled_output.json \
  --monitor labeling/data/monitor_output.jsonl \
  --output labeling/data/review.csv
```

## Pipeline CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--input` | `labeling/data/raw_samples.json` | Input ShareGPT JSON |
| `--output` | `labeling/data/labeled_samples.json` | Output labeled JSON |
| `--model` | `deepseek-v3.2` | Model ID (must be available via LiteLLM) |
| `--concurrency` | `30` | Max parallel LLM requests |
| `--limit` | `0` (all) | Process only first N samples |
| `--shuffle` | off | Randomly shuffle before slicing |
| `--no-arbitration` | off | Skip arbitration pass |
| `--stats` | auto | Override stats output path |
| `--monitor` | auto | Override monitor output path |

## Output Files

The pipeline produces three files per run (auto-named from `--output`):

| File | Pattern | Content |
|------|---------|---------|
| Labeled JSON | `labeled_*.json` | Full samples with `.labels` and `.labeling_monitor` |
| Stats JSON | `stats_*.json` | Aggregate metrics, distributions, confidence stats |
| Monitor JSONL | `monitor_*.jsonl` | Per-sample trace (calls, tokens, latency, issues) |

## Production Tuning

### Concurrency

- **30** (default): Safe for most LLM providers, avoids 429 rate limits
- **50**: Works well with DeepSeek v3.2 via LiteLLM proxy
- **100+**: Only if provider supports it; monitor for 429/503 errors

### Arbitration

Arbitration re-runs dimensions with confidence below `CONFIDENCE_THRESHOLD` (0.65) at temperature 0.3. In practice with deepseek-v3.2 + v4 prompts, arbitration triggers ~0% of the time (all confidence scores stay above threshold).

To disable: `--no-arbitration`

### Cost Estimate

Per sample (2 calls, no arbitration):
- ~10K prompt tokens + ~400 completion tokens
- deepseek-v3.2: ~$0.002/sample
- 108 samples full run: ~$0.22

## File Overview

| File | Description |
|------|-------------|
| `config.py` | Production settings (API, model, concurrency, thresholds) |
| `pipeline.py` | Main concurrent labeling pipeline |
| `prompts.py` | Call 1 & Call 2 prompt definitions, tag pools, few-shot examples |
| `preprocessing.py` | Structural signal extraction (languages, tool roles, code blocks) |
| `export_review.py` | Labeled JSON → review CSV for human audit |
| `compare_models.py` | Multi-model comparison report generator |
| `collect_gold_set.py` | Gold set conversation generator |
| `generate_report.py` | Labeling summary report generator |

## Data

| File | Description |
|------|-------------|
| `data/raw_samples.json` | 108 source conversations (97 single-turn + 11 multi-turn agentic) |
| `data/labeled_deepseek_v4.json` | Production baseline (deepseek-v3.2, 0 unmapped) |
| `data/labeled_sonnet_v4.json` | Gold standard reference (claude-sonnet-4.6) |
| `data/labeled_e2e_test.json` | E2E test run (20 random samples) |
| `data/review_e2e_test.csv` | Human review table from e2e test |
