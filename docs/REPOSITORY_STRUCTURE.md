# Repository Structure

## Overview

This repository contains a comprehensive capability taxonomy for code generation models, designed for systematic coverage analysis and diverse query generation for SFT (Supervised Fine-Tuning) data.

## Directory Structure

```
.
├── taxonomy.yaml                    # Category definitions and schema
├── taxonomy/
│   └── tags/                        # Tag definitions by category
│       ├── language.yaml            # 50 programming languages
│       ├── library.yaml             # 339 frameworks and libraries
│       ├── domain.yaml              # 57 application domains
│       ├── concept.yaml             # 107 programming concepts
│       ├── task.yaml                # 20 task types
│       ├── constraint.yaml          # 25 non-functional requirements
│       ├── agentic.yaml             # 19 agent capabilities
│       └── context.yaml             # 9 context complexity levels
├── scripts/                         # Tooling and utilities
│   ├── validate_taxonomy.py         # Taxonomy validation
│   ├── collect_tags.py              # Tag collection from sources
│   ├── collect_tags_multisource.py  # Multi-source collection
│   ├── normalize_tags.py            # Basic normalization
│   ├── normalize_tags_enhanced.py   # Enhanced normalization with merging
│   ├── expand_aliases.py            # Automated alias expansion
│   └── alias_blocklist.txt          # Alias expansion blocklist
├── openspec/                        # OpenSpec workflow artifacts
│   ├── changes/                     # Active changes
│   └── archive/                     # Archived changes
│       ├── 2026-02-05-build-capability-taxonomy/
│       ├── 2026-02-05-expand-library-tags/
│       ├── 2026-02-05-expand-domain-tags/
│       └── 2026-02-05-expand-concept-tags/
├── collected_*.json                 # Collection artifacts
├── GRANULARITY_GUIDELINES.md        # Library tag granularity guidelines
├── FIXES_SUMMARY.md                 # Quality fixes documentation
└── README.md                        # Main documentation
```

## Core Files

### Taxonomy Definition
- **taxonomy.yaml**: Defines the 8 orthogonal categories and their schemas
- **taxonomy/tags/*.yaml**: Tag definitions for each category

### Scripts
- **validate_taxonomy.py**: Validates orthogonality, uniqueness, schema compliance
- **normalize_tags_enhanced.py**: Normalizes and merges tags with intelligent conflict resolution
- **collect_tags_multisource.py**: Collects tags from multiple sources with weighted scoring

### Documentation
- **README.md**: Main documentation with statistics and usage
- **GRANULARITY_GUIDELINES.md**: 3-tier granularity system for Library tags
- **FIXES_SUMMARY.md**: Record of quality improvements and fixes

## Workflow

### 1. Tag Collection
```bash
# Manual collection
vim collected_new_tags.json

# Or multi-source collection (for Library tags)
python scripts/collect_tags_multisource.py --subcategory Web --output collected_web.json
```

### 2. Normalization
```bash
python scripts/normalize_tags_enhanced.py \
  --input collected_new_tags.json \
  --output-dir taxonomy/tags \
  --category Library \
  --merge
```

### 3. Validation
```bash
python scripts/validate_taxonomy.py
```

### 4. Commit
```bash
git add taxonomy/tags/*.yaml
git commit -m "Add new tags to [category]"
```

## OpenSpec Workflow

This repository uses OpenSpec for structured change management:

1. **Create change**: `openspec new change <name>`
2. **Fast-forward artifacts**: `/opsx:ff <name>`
3. **Implement**: `/opsx:apply <name>`
4. **Archive**: `openspec archive <name>`

Archived changes are stored in `openspec/changes/archive/` with full documentation.

## Data Quality

### Validation Checks
- ✅ Category orthogonality
- ✅ Tag uniqueness (IDs and names)
- ✅ Schema compliance
- ✅ Referential integrity
- ✅ Metadata quality
- ✅ Distribution balance

### Quality Metrics
- **Total tags**: 626
- **Validation**: 0 errors
- **Alias coverage**: 99.7% (Library), 100% (Domain, Language, Task, Constraint, Agentic, Context)
- **Metadata completeness**: High across all categories

## Expansion History

| Category | Before | After | Change | Status |
|----------|--------|-------|--------|--------|
| Library | 86 | 339 | +294% | ✅ Complete |
| Domain | 32 | 57 | +78% | ✅ Complete |
| Concept | 93 | 107 | +15% | ✅ Complete |
| Language | 50 | 50 | - | ✅ Complete |
| Task | 20 | 20 | - | ✅ Complete |
| Constraint | 25 | 25 | - | ✅ Complete |
| Agentic | 19 | 19 | - | ✅ Complete |
| Context | 9 | 9 | - | ✅ Complete |

## Design Principles

### 1. Orthogonality
Categories are designed to be orthogonal - each tag belongs to exactly one category.

### 2. Mixed Hierarchy
- **Flat categories**: Language, Domain, Task, Constraint, Agentic, Context
- **Hierarchical categories**: Library (5 subcategories), Concept (3 subcategories)

### 3. Medium Granularity
Tags are at module-level granularity, balancing specificity with maintainability.

### 4. Quality Over Quantity
Expansion focused on filling gaps and improving coverage, not hitting arbitrary numbers.

## Contributing

See README.md for contribution guidelines.
