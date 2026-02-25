# CLAUDE.md

## Project Overview

SFT (Supervised Fine-Tuning) Capability Taxonomy — a structured tag system for labeling code-generation training data. Enables coverage analysis, data filtering, and annotation quality control.

**Current version: v3.1 — 9 categories, 221 tags, evaluation score 8.3/10**

## Project Structure

```
taxonomy.yaml                  # Category schema (9 categories, select modes, descriptions)
taxonomy/tags/*.yaml           # Tag definitions (one file per category)
scripts/
  validate_taxonomy.py         # Validate tag schema, uniqueness, orthogonality
  generate_tags_data.py        # Generate visualization data from YAML → JSON + HTML embed
  compute_iaa.py               # Inter-Annotator Agreement (Fleiss' κ) computation
  test_iaa.py                  # Tests for kappa implementation
  extract_libraries.py         # Library auto-extraction from import statements
labeling/                      # Auto-labeling pipeline (see labeling/README.md)
  config.py                    # Production settings (API, model, concurrency, thresholds)
  pipeline.py                  # 2-call concurrent labeling pipeline
  prompts.py                   # Call 1 & Call 2 prompt definitions + tag pools
  preprocessing.py             # Structural signal extraction
  export_review.py             # Labeled JSON → review CSV
  compare_models.py            # Multi-model comparison
  collect_gold_set.py          # Gold set conversation generator
  data/                        # Gold set & labeling outputs
data/iaa/                      # IAA pilot test materials (50 samples, templates, examples)
docs/
  annotation_guidelines.md     # Annotation rules, boundary cases (v1.1)
  iaa_evaluation_plan.md       # IAA evaluation methodology
  taxonomy_evaluation_report_v3.md  # Comprehensive v3 evaluation
visualization/
  tag-visualization.html       # Standalone interactive browser (data embedded)
  tags_data.json               # JSON export of all tags
tag-manager/                   # SvelteKit web app for tag CRUD (not actively used)
```

## Taxonomy Categories

| Category | Tags | Select | Key |
|----------|------|--------|-----|
| Language | 75 | multi | Programming languages + markup/config |
| Domain | 38 | multi | Application domains (web, ML, devops...) |
| Concept | 25 | multi | Umbrella programming concepts with alias sub-concepts |
| Task | 21 | multi | Work types (bug-fixing, feature-implementation...) |
| Constraint | 20 | multi | Non-functional requirements (thread-safe, scalable...) |
| Agentic | 23 | multi | Tool Actions (12) + Behavioral Patterns (11) |
| Context | 10 | single | Code scope (snippet → repository) |
| Difficulty | 4 | single | beginner / intermediate / advanced / expert |
| Intent | 5 | single | learn / build / debug / review / decide |

## Key Commands

```bash
# Taxonomy
python3 scripts/validate_taxonomy.py          # Validate (expect 0 errors, 1 warning for 'make' alias)
python3 scripts/generate_tags_data.py --stats  # Regenerate visualization data
python3 scripts/test_iaa.py                    # Run kappa tests (7 tests, all should pass)
python3 scripts/compute_iaa.py A1.yaml A2.yaml A3.yaml --report-dir out/  # Compute IAA

# Labeling pipeline
python3 labeling/pipeline.py --limit 20 --shuffle   # Label 20 random samples
python3 labeling/export_review.py --input labeling/data/labeled_output.json --output labeling/data/review.csv
```

## Development Conventions

- Tag files: `taxonomy/tags/<category>.yaml` — each tag has `id`, `name`, `category`, `description`, `aliases`
- Tag IDs: kebab-case (`machine-learning`, `code-review-task`)
- Concept/Agentic tags have `subcategory` field for grouping
- After modifying tags, run `validate_taxonomy.py` then `generate_tags_data.py --stats` to update visualization
- The HTML visualization embeds data inline — `generate_tags_data.py` replaces the `let tagsData = ...` block automatically
- Annotation guidelines version should stay in sync with taxonomy version

## Version History

| Version | Tags | Score | Key Changes |
|---------|------|-------|-------------|
| v1 | 198 | 7.2 | Initial 7-category design |
| v2 | 252 | 7.3 | +Library, expanded Concept/Domain |
| v3 | 224 | 8.3 | -Library, Concept 106→25, +Difficulty/Intent, annotation guidelines |
| v3.1 | 221 | 8.3 | Domain 41→38 (merge mlops/observability/SRE), Language eval (no change) |

## Current Status & Next Steps

**Completed:**
- [x] 9-category orthogonal taxonomy design
- [x] 221 tag definitions with aliases
- [x] Annotation guidelines (100+ boundary cases)
- [x] IAA tooling (Fleiss' κ) + 50 sample queries
- [x] Validation framework (0 errors)
- [x] Interactive visualization (responsive HTML)
- [x] v3 evaluation report
- [x] Domain long-tail cleanup
- [x] Language long-tail evaluation (no changes needed)
- [x] Output Format dimension evaluation (decided not to add — redundant with Intent × Task)

**Next steps:**
- [ ] IAA pilot test execution (3 annotators, 50 samples) — tooling ready, needs human annotators
- [ ] Library auto-extraction integration into labeling pipeline
- [ ] Production annotation pipeline scaling (full dataset beyond gold set)
