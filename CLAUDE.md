# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SFT Capability Taxonomy + Auto-Labeling Pipeline for code-generation training data. Two main subsystems:

1. **Taxonomy** — 9-category tag system (v3.1, 221 tags) for structured annotation
2. **Labeling Pipeline** — concurrent 2-call LLM pipeline that auto-labels conversations

## Setup

```bash
# Install dependencies
uv sync

# Required env vars for labeling pipeline
export LITELLM_BASE="http://101.47.36.53:4000/v1"
export LITELLM_KEY="sk-..."
```

## Key Commands

```bash
# Taxonomy validation & visualization
python3 scripts/validate_taxonomy.py              # Expect 0 errors, 1 warning ('make' alias)
python3 scripts/generate_tags_data.py --stats      # Regenerate visualization data → HTML embed
python3 scripts/test_iaa.py                        # 7 kappa tests, all should pass

# Labeling pipeline
python3 labeling/pipeline.py --limit 20 --shuffle                         # Label 20 random samples
python3 labeling/pipeline.py --input labeling/data/pangu_test_samples.jsonl  # Label Pangu format data
python3 labeling/pipeline.py --concurrency 50                             # Full dataset, high concurrency
python3 labeling/pipeline.py --resume labeling/data/runs/<run_dir>        # Resume interrupted run
python3 labeling/pipeline.py --model deepseek-v3.2 --no-arbitration       # Skip arbitration pass

# Labeling tools
python3 labeling/tools/export_review.py --input <run_dir>/labeled.json --monitor <run_dir>/monitor.jsonl --output review.csv
python3 labeling/tools/analyze_unmapped.py <run_dir>/labeled.json    # Unmapped tag analysis
python3 labeling/tools/visualize_labels.py <run_dir> --open          # Open dashboard in browser
python3 labeling/tools/compare_models.py                             # Multi-model comparison
python3 labeling/tools/generate_report.py                            # Labeling summary report
```

## Architecture

### Taxonomy (`taxonomy.yaml` + `taxonomy/tags/*.yaml`)

9 dimensions: Intent (single), Difficulty (single), Context (single), Language (multi), Domain (multi), Concept (multi), Task (multi), Agentic (multi), Constraint (multi).

Tag definitions live in `taxonomy/tags/<category>.yaml`. IDs are kebab-case. Concept/Agentic tags have a `subcategory` field. After modifying tags, run `validate_taxonomy.py` then `generate_tags_data.py --stats`.

### Labeling Pipeline (`labeling/`)

```
Input (ShareGPT JSON or Pangu JSONL)
  → Auto-detect format + normalize (preprocessing.py)
  → Slice true multi-turn into per-reply samples (pyramid expansion)
  → Call 1 (LLM): Intent, Language, Domain, Task, Difficulty
  → Call 2 (LLM): Concept, Agentic, Constraint, Context (receives Call 1 results)
  → Validation + optional arbitration (confidence < 0.65)
  → Output: run directory with labeled.json, labeled.jsonl, stats.json, monitor.jsonl, dashboard.html
```

Key design decisions:
- **Two input formats**: ShareGPT (`conversations: [{from, value}]`) and Pangu (`data: [{role, content}]` with `[unused*]` training tokens). Auto-detected by `preprocessing.py`.
- **Multi-turn slicing**: True multi-turn → N per-reply samples (pyramid expansion). Pseudo multi-turn preserved as-is. Each slice gets independent labels.
- **Run directories**: Output goes to `labeling/data/runs/<timestamp>_<model>/` with dashboard auto-generated.
- **Config via env vars**: `LITELLM_BASE` and `LITELLM_KEY` must be set. See `labeling/config.py` for all settings.
- **Tag pools**: Defined in `labeling/prompts.py` as `TAG_POOLS` dict. Pipeline validates all labels against these pools.

### Visualization (`visualization/`)

`tag-visualization.html` is standalone — data is embedded inline by `generate_tags_data.py` which replaces the `let tagsData = ...` block.

### Tag Manager (`tag-manager/`)

SvelteKit web UI for browsing and editing tag definitions. Run with:
```bash
cd tag-manager && npm install && npm run dev
```

## Conventions

- Tag IDs: kebab-case (`machine-learning`, `code-review-task`)
- Annotation guidelines version stays in sync with taxonomy version
- `labeling/data/runs/` is gitignored — run outputs are ephemeral
- `labeling/data/baselines/` contains frozen reference results (deepseek v4 + sonnet v4)
- Default model: `gpt-4o-mini` (8x throughput, cheapest). Alt production: `deepseek-v3.2` (0 unmapped tags). Gold set: `claude-sonnet-4-6` or stronger. Arbitration: `claude-opus-4-5-20251101-thinking`.
