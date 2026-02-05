# Capability Taxonomy

A structured taxonomy for categorizing programming capabilities in code generation models. This taxonomy enables systematic coverage analysis and diverse query generation for SFT (Supervised Fine-Tuning) data.

## Overview

The taxonomy consists of **8 orthogonal categories** with **333 tags** covering the full spectrum of programming abilities:

| Category | Tags | Description |
|----------|------|-------------|
| **Language** | 50 | Programming languages (Python, Rust, JavaScript, etc.) |
| **Library** | 85 | Frameworks and libraries (React, PyTorch, Django, etc.) |
| **Domain** | 32 | Application domains (Web Backend, ML, Embedded, etc.) |
| **Concept** | 93 | Programming concepts (OOP, Concurrency, Design Patterns, etc.) |
| **Task** | 20 | Task types (Code Generation, Debugging, Refactoring, etc.) |
| **Constraint** | 25 | Non-functional requirements (Performance, Security, Compliance, etc.) |
| **Agentic** | 19 | Agent capabilities (File Operations, Tool Use, Reasoning, etc.) |
| **Context** | 9 | Context complexity (Single File, Multi-file, Repository, etc.) |

## Structure

```
.
├── taxonomy.yaml           # Category definitions and schema
├── taxonomy/
│   └── tags/              # Tag definitions by category
│       ├── language.yaml
│       ├── library.yaml
│       ├── domain.yaml
│       ├── concept.yaml
│       ├── task.yaml
│       ├── constraint.yaml
│       ├── agentic.yaml
│       └── context.yaml
└── scripts/               # Tooling
    ├── collect_tags.py    # Collect tags from sources
    ├── normalize_tags.py  # Normalize and deduplicate
    └── validate_taxonomy.py # Validate taxonomy
```

## Tag Schema

Each tag has the following structure:

```yaml
id: string                  # Unique kebab-case identifier
name: string                # Display name
category: string            # Category (Language, Library, etc.)
subcategory: string?        # Subcategory (for Library/Concept)
description: string?        # Brief description
aliases: string[]?          # Alternative names
language_scope: string[]?   # Applicable languages (for Concept tags)
difficulty: enum?           # basic | intermediate | advanced
source: string?             # Provenance information
```

## Usage

### Validating the Taxonomy

```bash
python scripts/validate_taxonomy.py
```

This checks for:
- Category orthogonality
- Tag uniqueness
- Schema compliance
- Referential integrity
- Metadata quality
- Distribution balance

### Collecting New Tags

```bash
# Collect tags for a specific category
python scripts/collect_tags.py --category Language --output collected.json

# For hierarchical categories, specify subcategory
python scripts/collect_tags.py --category Library --subcategory Web --output collected.json
```

### Normalizing Tags

```bash
python scripts/normalize_tags.py --input collected.json --output-dir taxonomy/tags
```

This performs:
- Deduplication (exact match, alias match, case-insensitive)
- ID normalization (kebab-case conversion)
- Alias conflict detection
- Granularity validation
- YAML output (sorted alphabetically)

## Design Principles

### 1. Orthogonality

Categories are designed to be orthogonal - each tag belongs to exactly one category. This ensures:
- No ambiguity in classification
- Clean separation of concerns
- Efficient querying and filtering

### 2. Mixed Hierarchy

- **Flat categories**: Language, Domain, Task, Constraint, Agentic, Context
- **Hierarchical categories**: Library (5 subcategories), Concept (3 subcategories)

This balances simplicity with organization for categories with many tags.

### 3. Medium Granularity

Tags are at module-level granularity (e.g., `pandas-groupby`) rather than:
- Too coarse: `pandas` (can't distinguish skill levels)
- Too fine: `pandas-dataframe-merge` (unmaintainable)

### 4. Language-Scoped Concepts

Language-specific concepts (e.g., Rust's Borrow Checker) are placed in the Concept category with `language_scope` metadata, maintaining orthogonality while capturing applicability.

## Statistics

- **Total tags**: 333
- **Categories**: 8
- **Hierarchical subcategories**: 8 (5 for Library, 3 for Concept)
- **Tags with aliases**: ~90%
- **Tags with difficulty levels**: ~30% (Concept tags)
- **Tags with language scope**: ~15% (language-specific concepts)

## Contributing

To add new tags:

1. Collect tags using `collect_tags.py` or manually create JSON
2. Normalize with `normalize_tags.py`
3. Validate with `validate_taxonomy.py`
4. Ensure validation passes (no errors)
5. Submit changes

## License

This taxonomy is part of the SFT data generation project.
