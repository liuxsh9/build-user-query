## Why

Current SFT data generation lacks a systematic way to ensure comprehensive coverage of model capabilities. Without a structured capability taxonomy, we cannot identify gaps in training data, measure coverage, or systematically generate diverse queries that exercise the full spectrum of programming abilities needed for code generation models.

## What Changes

- Create a multi-dimensional capability taxonomy with 8 orthogonal categories (Language, Library, Domain, Concept, Task, Constraint, Agentic, Context)
- Define a hierarchical tag system where categories are stable and tags are extensible
- Build semi-automated tooling to collect, normalize, and validate tags from multiple sources
- Establish data structures (YAML schemas) for taxonomy definition and tag metadata
- Enable future data labeling by providing a complete capability graph

## Capabilities

### New Capabilities
- `taxonomy-schema`: Define the structure of categories, subcategories, and tags with metadata
- `tag-collection`: Semi-automated collection of tags from various sources (language lists, library docs, benchmarks)
- `tag-normalization`: Deduplication, alias resolution, and metadata enrichment for collected tags
- `taxonomy-validation`: Validation rules to ensure orthogonality, completeness, and consistency

### Modified Capabilities
<!-- No existing capabilities are being modified -->

## Impact

- Creates foundation for all downstream SFT query generation work
- Enables systematic coverage analysis of training data
- Provides structured vocabulary for capability-driven data generation
- No impact on existing code (greenfield development)
