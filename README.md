# SFT Capability Taxonomy

A structured capability taxonomy for labeling SFT (Supervised Fine-Tuning) training data. Enables systematic coverage analysis, data filtering, and quality control for code generation models.

## Overview

**9 orthogonal categories, 221 tags** covering the full spectrum of programming abilities:

| Category | Tags | Select | Description |
|----------|------|--------|-------------|
| **Language** | 75 | multi | Programming languages and markup/config formats |
| **Domain** | 38 | multi | Application domains and industry scenarios |
| **Concept** | 25 | multi | Programming concepts (umbrella labels with sub-concept aliases) |
| **Task** | 21 | multi | Types of work being performed |
| **Constraint** | 20 | multi | Non-functional requirements |
| **Agentic** | 23 | multi | Agent capabilities: Tool Actions + Behavioral Patterns |
| **Context** | 10 | single | Code scope / project context |
| **Difficulty** | 4 | single | Coding ability level required (beginner → expert) |
| **Intent** | 5 | single | User's primary goal (learn / build / debug / review / decide) |

## Core Use Cases

```
Use Case 1: Data Labeling
  Input:  user query + agent trajectory
  Output: multi-dimensional tag set
  Goal:   fast, consistent, actionable annotations

Use Case 2: Coverage Analysis
  Input:  labeled dataset
  Output: capability gaps and distribution insights
  Goal:   identify blind spots at meaningful granularity

Use Case 3: Data Filtering
  Input:  requirement (e.g. "Rust concurrency advanced debug")
  Output: matching data subset
  Goal:   9-dimension orthogonal queries, composable filters
```

## Structure

```
.
├── taxonomy.yaml              # Category schema and definitions
├── taxonomy/tags/             # Tag definitions by category
│   ├── language.yaml          # 75 tags
│   ├── domain.yaml            # 38 tags
│   ├── concept.yaml           # 25 tags (Fundamentals / Advanced / Engineering)
│   ├── task.yaml              # 21 tags
│   ├── constraint.yaml        # 20 tags
│   ├── agentic.yaml           # 23 tags (Tool Actions / Behavioral Patterns)
│   ├── context.yaml           # 10 tags
│   ├── difficulty.yaml        # 4 tags
│   └── intent.yaml            # 5 tags
├── scripts/
│   ├── validate_taxonomy.py   # Validate taxonomy integrity
│   ├── compute_iaa.py         # Inter-Annotator Agreement (Fleiss' κ)
│   └── test_iaa.py            # Tests for IAA computation
├── data/iaa/                  # IAA pilot test materials
│   ├── samples.yaml           # 50 sample queries for IAA testing
│   ├── annotation_template.yaml
│   └── example_*.yaml         # Example annotations
├── docs/
│   ├── annotation_guidelines.md  # Annotation rules and boundary cases
│   ├── iaa_evaluation_plan.md    # IAA evaluation methodology
│   └── taxonomy_evaluation_report_v3.md  # Latest evaluation (8.3/10)
└── tag-manager/               # Web-based tag management UI
```

## Tag Schema

```yaml
id: string                  # Unique identifier (kebab-case)
name: string                # Display name
category: string            # One of the 9 categories
subcategory: string?        # For Concept (Fundamentals/Advanced/Engineering)
                            # and Agentic (Tool Actions/Behavioral Patterns)
description: string         # Brief description
aliases: string[]?          # Alternative names for matching
language_scope: string[]?   # Applicable languages (e.g. ownership → rust)
examples: string[]?         # Example queries (for Difficulty/Intent)
```

## Usage

### Validate the Taxonomy

```bash
python3 scripts/validate_taxonomy.py
```

Checks: category orthogonality, tag uniqueness, schema compliance, distribution balance.

### Compute Inter-Annotator Agreement

```bash
python3 scripts/compute_iaa.py data/iaa/A1.yaml data/iaa/A2.yaml data/iaa/A3.yaml \
  --report-dir output/
```

Produces Fleiss' κ per category, confusion matrices, and disagreement analysis.

## Design Principles

1. **Orthogonality**: Each category answers a different question. No semantic overlap between categories.
2. **Umbrella granularity**: Concept tags are broad labels (e.g. `concurrency`) with sub-concepts as aliases (e.g. `mutex`, `deadlock`, `async-await`). This maximizes annotation consistency.
3. **Evidence-based tagging**: Only tag what has direct textual evidence. When unsure, don't tag.
4. **Signal density over coverage**: 221 well-defined tags > 600+ noisy tags. Every tag should be a meaningful signal.

## Version History

| Version | Categories | Tags | Score | Key Changes |
|---------|-----------|------|-------|-------------|
| v1 | 7 | 198 | 7.2 | Initial design |
| v2 | 9 | 252 | 7.3 | +Library, expanded Concept/Domain |
| v3 | 9 | 221 | **8.3** | -Library, Concept 106→25, +Difficulty, +Intent, annotation guidelines |

## Production Readiness

| Dimension | Status |
|-----------|--------|
| Category design | Done |
| Tag definitions | Done (221 tags, 0 validation errors) |
| Annotation guidelines | Done (100+ boundary cases) |
| IAA evaluation | Designed, awaiting execution |
| Validation tooling | Done |
