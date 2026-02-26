# SFT Auto-Labeling Pipeline

Automated labeling pipeline for SFT code-generation training data, using a structured 9-category taxonomy (v3.1, 221 tags).

## Architecture

```
Input (ShareGPT JSON / Pangu JSONL)
  │
  ├─ Format detection: auto-detect ShareGPT vs Pangu (preprocessing.py)
  │
  ├─ Normalization: strip training tokens, unify to ShareGPT internal format
  │
  ├─ Multi-turn slicing: true multi-turn → N per-reply samples (pyramid expansion)
  │     • Pseudo multi-turn: preserved as-is (already one training sample)
  │     • True multi-turn: each assistant reply → one sample with full preceding context
  │
  ├─ Call 1 (LLM): Intent, Language, Domain, Task, Difficulty
  │
  ├─ Call 2 (LLM): Concept, Agentic, Constraint, Context  (receives Call 1 results)
  │
  ├─ Validation: tag pool check, cross-dimension consistency
  │
  ├─ Arbitration (optional): re-run low-confidence dimensions at higher temperature
  │
  └─ Output: run directory with labeled JSON/JSONL + stats + monitor + dashboard
```

## Directory Structure

```
labeling/
  config.py              # Production settings (env vars, model, concurrency, thresholds)
  pipeline.py            # Main concurrent labeling pipeline
  prompts.py             # Call 1 & Call 2 prompts, tag pools, few-shot examples
  preprocessing.py       # Format detection, normalization, multi-turn slicing
  tools/
    visualize_labels.py  # Standalone HTML dashboard from labeled results
    export_review.py     # Labeled JSON → review CSV for human audit
    analyze_unmapped.py  # Unmapped tag frequency analysis for pool iteration
    compare_models.py    # Multi-model comparison report
    generate_report.py   # Labeling summary report
    collect_gold_set.py  # Gold set conversation generator
  data/
    raw_samples.json     # 108 ShareGPT source conversations (97 single-turn + 11 agentic)
    pangu_test_samples.jsonl  # 12 Pangu format test samples (all variants)
    baselines/           # Frozen v4 baselines (deepseek + sonnet)
    reports/             # Analysis documents
    runs/                # Per-run output (auto-created, gitignored)
  README.md
```

## Configuration

Settings in `config.py`, API credentials via environment variables:

```bash
export LITELLM_BASE="http://your-litellm-proxy:4000/v1"
export LITELLM_KEY="sk-your-key"
```

| Setting | Default | Description |
|---------|---------|-------------|
| `LITELLM_BASE` | env `LITELLM_BASE` | LiteLLM proxy endpoint |
| `LITELLM_KEY` | env `LITELLM_KEY` | API key |
| `DEFAULT_MODEL` | `deepseek-v3.2` | Production labeling model |
| `DEFAULT_CONCURRENCY` | `30` | Concurrent LLM requests |
| `CONFIDENCE_THRESHOLD` | `0.65` | Below this triggers arbitration |
| `MAX_RETRIES` | `3` | LLM call retry count |
| `REQUEST_TIMEOUT` | `180` | Per-request timeout (seconds) |
| `DIR_PIPELINE_WATERMARK` | `2.0` | Load next file when in-flight tasks < concurrency × watermark |
| `DIR_PIPELINE_MAX_FILES` | `5` | Max files loaded in memory simultaneously |

### Model Tiers

| Tier | Models | Use Case |
|------|--------|----------|
| Strong | claude-opus-4.5-thinking, gpt-5, gemini-2.5-pro-thinking | Gold set annotation |
| Mid | claude-sonnet-4.6, deepseek-v3.2, qwen3-235b | Production labeling |
| Light | gpt-4o-mini, deepseek-v3.1 | Cost-sensitive batches |

## Input Formats

Pipeline auto-detects format from input file structure. Supports JSON arrays and JSONL.

### ShareGPT Format

```json
[
  {
    "id": "gen-0000",
    "conversations": [
      { "from": "human", "value": "Python 列表推导式和生成器表达式的区别？" },
      { "from": "gpt", "value": "列表推导式和生成器表达式都是..." }
    ],
    "metadata": { "source": "generated", "has_code": true }
  }
]
```

### Pangu Format

Pangu 是内部 SFT 训练数据格式，包含特殊训练标记。Pipeline 自动剥离这些标记后进行标注。

```jsonl
{"meta_prompt":["你是一个有用的助手"],"data":[{"role":"user","content":"解释快速排序"},{"role":"assistant","content":"[unused16]思考过程...[unused17]快速排序是..."}]}
```

支持的 Pangu 变体：

| 变体 | 说明 | 标注处理 |
|------|------|----------|
| 单轮快思考 | `/no_think` + `[unused16][unused17]` 空标记 | 剥离标记，标注 1 条 |
| 单轮慢思考 | `[unused16]{思考}[unused17]` | 剥离标记，标注 1 条 |
| 伪多轮 | `[unused10][unused9]` 分隔历史轮次 | 保持原样，标注 1 条 |
| 真多轮 | `data` 数组含多组 user/assistant | 切片为 N 条（金字塔展开），每条独立标注 |
| 工具调用 | `[unused11-16]` 嵌入式 / `role: tool` 独立节点 | 剥离标记，保留语义 |
| 无标记 | 纯 role/content，无特殊标记 | 直接标注 |

详细格式规范见 `docs/pangu_data_format.md`。

### Multi-turn Slicing

真多轮数据在训练时按轮次展开（金字塔形状），每个 assistant 回复对应一条训练样本。Pipeline 自动执行相同的切片：

```
原始 3 轮对话 → 3 条标注样本：
  sample_t1: [user₁, assistant₁]
  sample_t2: [user₁, assistant₁, user₂, assistant₂]
  sample_t3: [user₁, assistant₁, user₂, assistant₂, user₃, assistant₃]
```

每条切片独立标注，标签随轮次递进（如 t1=bug-fixing, t2=+code-explanation, t3=+performance-analysis），支持按标签筛选高价值训练轮次。

## Quick Start

```bash
# Label 20 random ShareGPT samples (single file)
python3 labeling/pipeline.py --limit 20 --shuffle

# Label Pangu format data
python3 labeling/pipeline.py --input labeling/data/pangu_test_samples.jsonl

# Full dataset, high concurrency
python3 labeling/pipeline.py --concurrency 50

# Label an entire directory (recursive, all json/jsonl)
python3 labeling/pipeline.py --input /data/train/ --limit 5

# Resume after interruption (reads checkpoint, skips completed files)
python3 labeling/pipeline.py --resume labeling/data/runs/<run_dir>/

# View dashboard (auto-generated in run dir)
open labeling/data/runs/<run_dir>/dashboard.html

# Export review CSV
python3 labeling/tools/export_review.py \
  --input labeling/data/runs/<run_dir>/labeled.json \
  --monitor labeling/data/runs/<run_dir>/monitor.jsonl \
  --output review.csv

# Analyze unmapped tags
python3 labeling/tools/analyze_unmapped.py labeling/data/runs/<run_dir>/labeled.json

# Regenerate dashboard from existing run
python3 labeling/tools/visualize_labels.py labeling/data/runs/<run_dir> --open
```

## Pipeline CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--input` | `labeling/data/raw_samples.json` | Input file or directory (JSON/JSONL, recursive for dirs) |
| `--resume` | — | Resume from existing run directory (reads checkpoint.json) |
| `--model` | `deepseek-v3.2` | Model ID (must be available via LiteLLM) |
| `--concurrency` | `30` | Max parallel LLM requests |
| `--limit` | `0` (all) | Process only first N samples per file |
| `--shuffle` | off | Randomly shuffle before slicing |
| `--no-arbitration` | off | Skip arbitration pass |

## Output

### Single-file mode

Each run creates a timestamped directory under `data/runs/`:

```
data/runs/20260225_155440_deepseek-v3.2/
  labeled.json      # Full samples with .labels and .labeling_monitor
  labeled.jsonl     # One sample per line (streaming-friendly)
  stats.json        # Aggregate metrics, distributions, confidence stats
  monitor.jsonl     # Per-sample trace (calls, tokens, latency, issues)
  dashboard.html    # Interactive statistics dashboard (auto-generated)
```

### Directory mode

When `--input` is a directory, output mirrors the input structure. Each input file gets its own subdirectory with a full set of outputs, plus global summary files at the root:

```
Input:
  /data/train/
    math/algebra.jsonl
    math/geometry.jsonl
    code/python.json

Output:
  data/runs/20260225_200000_deepseek-v3.2/
    checkpoint.json        # File-level progress (for --resume)
    summary_stats.json     # Merged stats across all files
    dashboard.html         # Global dashboard
    math/
      algebra/             # One subdirectory per input file
        labeled.json
        labeled.jsonl
        stats.json
        monitor.jsonl
        dashboard.html
      geometry/
        ...
    code/
      python/
        ...
```

Files are processed via a cross-file pipeline: multiple files' samples compete for the shared concurrency semaphore simultaneously. New files are loaded when in-flight tasks drop below a watermark (`concurrency × DIR_PIPELINE_WATERMARK`), bounded by `DIR_PIPELINE_MAX_FILES` to limit memory. Completed files are flushed and released immediately. The `checkpoint.json` tracks completed/failed files so `--resume` can skip already-finished work.

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
