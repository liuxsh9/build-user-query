# Capability Taxonomy

A structured taxonomy for categorizing programming capabilities in code generation models. This taxonomy enables systematic coverage analysis and diverse query generation for SFT (Supervised Fine-Tuning) data.

## Overview

The taxonomy consists of **8 orthogonal categories** with **626 tags** covering the full spectrum of programming abilities:

| Category | Tags | Description |
|----------|------|-------------|
| **Language** | 50 | Programming languages (Python, Rust, JavaScript, etc.) |
| **Library** | 339 | Frameworks and libraries (React, PyTorch, Django, etc.) |
| **Domain** | 57 | Application domains (Web Backend, ML, Embedded, etc.) |
| **Concept** | 107 | Programming concepts (OOP, Concurrency, Design Patterns, etc.) |
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
├── scripts/               # Tooling
│   ├── collect_tags.py    # Collect tags from curated sources
│   ├── collect_tags_multisource.py  # Multi-source collection with weighted scoring
│   ├── normalize_tags.py  # Basic normalization
│   ├── normalize_tags_enhanced.py   # Enhanced normalization with alias expansion
│   ├── expand_aliases.py  # Automated alias expansion tool
│   ├── validate_taxonomy.py # Validate taxonomy
│   └── alias_blocklist.txt # Blocklist for alias expansion
└── GRANULARITY_GUIDELINES.md  # Library tag granularity guidelines
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
granularity: enum?          # library | module | component (for Library tags)
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
# Basic collection from curated sources
python scripts/collect_tags.py --category Language --output collected.json

# For hierarchical categories, specify subcategory
python scripts/collect_tags.py --category Library --subcategory Web --output collected.json

# Multi-source collection with weighted prioritization (Library tags)
python scripts/collect_tags_multisource.py --subcategory Web --output collected_web.json --min-score 0.1
```

### Expanding Aliases

```bash
# Run automated alias expansion on all Library tags
python scripts/expand_aliases.py --tags-dir taxonomy/tags --output alias_candidates.json

# Expand aliases for a specific tag
python scripts/expand_aliases.py --tag-id react --output react_aliases.json

# Show only auto-approve candidates (confidence > 0.8)
python scripts/expand_aliases.py --auto-approve
```

### Normalizing Tags

```bash
# Basic normalization
python scripts/normalize_tags.py --input collected.json --output-dir taxonomy/tags

# Enhanced normalization with alias expansion and merge
python scripts/normalize_tags_enhanced.py \
  --input collected_web.json \
  --output-dir taxonomy/tags \
  --category Library \
  --expand-aliases \
  --merge
```

This performs:
- Deduplication (exact match, alias match, case-insensitive)
- ID normalization (kebab-case conversion)
- Automated alias expansion (optional)
- Alias conflict detection
- Granularity classification (for Library tags)
- Multi-source metadata preservation
- Weighted score calculation
- Intelligent merging with existing tags
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

- **Total tags**: 626
- **Categories**: 8
- **Hierarchical subcategories**: 8 (5 for Library, 3 for Concept)
- **Library tags with granularity metadata**: 339/339 (100%)
- **Domain tags**: 57 (expanded from 32)
- **Concept tags**: 107 (expanded from 93)
- **Tags with aliases**: 99.7% (Library category), 100% (Domain category)
- **Tags with multi-source metrics**: 273/339 Library tags (80.5%)
- **Tags with difficulty levels**: ~100% (Concept tags)
- **Tags with language scope**: 18 languages (Library tags)

### Library Tag Enhancements

The Library category has been expanded from 86 to 339 tags with:
- **3-tier granularity system**: library, module, component levels (100% coverage)
- **Comprehensive alias coverage**: 99.7% of tags have aliases
- **Multi-source metrics**: 80.5% of tags have weighted scores from multiple sources
- **Extensive language coverage**: 18 programming languages covered
- **Quality assurance**: All duplicate tags resolved, validation passing with 0 errors

### Library Subcategory Distribution

- **Web**: 93 tags (frameworks, bundlers, state management, UI libraries)
- **Data**: 70 tags (ML/AI, data processing, visualization, NLP)
- **Testing**: 70 tags (unit testing, E2E testing, load testing, mocking)
- **Infrastructure**: 60 tags (containers, orchestration, CI/CD, monitoring)
- **Database**: 46 tags (ORMs, drivers, query builders, clients)

### Library Language Coverage

- **JavaScript**: 104 tags (30.7%)
- **Python**: 97 tags (28.6%)
- **TypeScript**: 80 tags (23.6%)
- **Go**: 39 tags (11.5%)
- **Java**: 25 tags (7.4%)
- **C#**: 12 tags (3.5%)
- **Ruby**: 9 tags (2.7%)
- **PHP**: 9 tags (2.7%)
- **Rust**: 8 tags (2.4%)
- **C++**: 7 tags (2.1%)
- **18 languages total** with comprehensive ecosystem coverage

### Domain Tag Enhancements

The Domain category has been expanded from 32 to 57 tags with:
- **Emerging technology domains**: MLOps, DataOps, Edge Computing, Serverless, Platform Engineering, SRE, FinOps, Low-Code
- **Specialized subfields**: Bioinformatics, Geospatial, Audio/Video Processing, Quantum Computing, AR/VR, Computer Graphics, Simulation, Data Engineering
- **Cross-cutting domains**: Accessibility, Internationalization, Real-time Systems, Observability, Performance Engineering, Compliance, Search Engineering
- **100% alias coverage**: All domain tags have relevant aliases
- **Quality validation**: All tags pass scope, granularity, distinctiveness, and ecosystem tests

### Domain Category Distribution

**Emerging Technology (8 tags):**
- MLOps, DataOps, Edge Computing, Serverless Computing
- Platform Engineering, Site Reliability Engineering, FinOps, Low-Code Development

**Specialized Subfields (10 tags):**
- Bioinformatics, Geospatial, Audio Processing, Video Processing
- Quantum Computing, Augmented Reality, Virtual Reality
- Computer Graphics, Simulation, Data Engineering

**Cross-Cutting Domains (7 tags):**
- Accessibility, Internationalization, Real-time Systems
- Observability, Performance Engineering, Compliance, Search Engineering

**Traditional Domains (32 tags):**
- Web Frontend/Backend, Mobile, Desktop, Game Development
- Machine Learning, Deep Learning, Data Science, Computer Vision, NLP
- Cloud Computing, DevOps, IoT, Embedded Systems, Cybersecurity
- And more...

### Concept Tag Enhancements

The Concept category has been expanded from 93 to 107 tags with:
- **Gap filling approach**: Added missing fundamental concepts rather than over-expansion
- **Data structures**: Hash Tables, Trees, Queues, Stacks, Linked Lists
- **Algorithms**: Sorting, Searching, Dynamic Programming, Greedy Algorithms
- **Concurrency primitives**: Mutex, Semaphores, Deadlock, Race Conditions, Thread Pools
- **100% difficulty coverage**: All concept tags have difficulty levels (basic, intermediate, advanced)
- **Quality focus**: Targeted additions to fill specific gaps in coverage

### Concept Subcategory Distribution

**Fundamentals (27 tags):**
- Basic data structures, control flow, functions, data types
- Added: Hash Tables, Trees, Queues, Stacks, Linked Lists

**Advanced (39 tags):**
- Complex patterns, concurrency, memory management
- Added: Sorting, Searching, Dynamic Programming, Greedy Algorithms
- Added: Mutex, Semaphores, Deadlock, Race Conditions, Thread Pools

**Engineering (41 tags):**
- Software engineering practices, architecture patterns, security
- Comprehensive coverage of modern engineering concepts

## Data Construction Approach

The taxonomy was built using a systematic, quality-focused methodology:

### 1. Initial Design Phase
- Defined 8 orthogonal categories based on first principles analysis
- Established mixed hierarchy (flat vs hierarchical) based on category size
- Created comprehensive schema with validation rules
- Built automated validation framework

### 2. Iterative Expansion Phase
- **Library Category** (86 → 339 tags, +294%):
  - Multi-source collection from curated lists (Awesome lists, State of JS, PyPI)
  - Weighted scoring system prioritizing quality signals
  - 3-tier granularity classification (library/module/component)
  - Automated alias expansion with confidence scoring
  - Intelligent merging with conflict resolution
- **Domain Category** (32 → 57 tags, +78%):
  - Gap analysis identifying emerging technologies, specialized subfields, cross-cutting domains
  - Quality-first approach: added only domains with clear scope and ecosystem
  - Comprehensive alias coverage for discoverability
- **Concept Category** (93 → 107 tags, +15%):
  - Pragmatic gap-filling: identified missing fundamentals (data structures, algorithms, concurrency)
  - Avoided over-engineering: added only essential concepts, not arbitrary targets
  - Maintained difficulty classification across all tags

### 3. Quality Assurance Phase
- Continuous validation after each expansion
- Orthogonality checks (alias conflicts, name overlaps)
- Metadata completeness verification
- Distribution balance analysis

### 4. Guiding Principles
- **Quality over quantity**: Expansion focused on filling real gaps, not hitting numbers
- **Orthogonality first**: Each tag belongs to exactly one category
- **Medium granularity**: Module-level specificity for practical usability
- **High metadata quality**: Comprehensive aliases, descriptions, difficulty levels

## Completeness Analysis

Comprehensive review of all 8 categories confirms **production-ready completeness**:

### Category-by-Category Assessment

| Category | Status | Coverage Analysis |
|----------|--------|-------------------|
| **Language** | ✅ COMPLETE | 50 tags cover all major programming languages including mainstream (Python, JavaScript, Java), systems (Rust, C++, Go), functional (Haskell, Elixir), and emerging languages |
| **Library** | ✅ EXCELLENT | 339 tags with comprehensive coverage across 5 subcategories (Web, Data, Testing, Infrastructure, Database) and 18 programming languages. 3-tier granularity system enables precise capability targeting |
| **Domain** | ✅ EXCELLENT | 57 tags covering traditional domains (Web, Mobile, ML), emerging technologies (MLOps, Edge Computing, Serverless), specialized subfields (Bioinformatics, Quantum), and cross-cutting concerns (Accessibility, Observability) |
| **Concept** | ✅ COMPLETE | 107 tags with full coverage of fundamentals (data structures, algorithms), advanced concepts (concurrency, memory management), and engineering practices (design patterns, testing, security) |
| **Task** | ✅ COMPLETE | 20 tags cover all major task types for code generation including creation, modification, analysis, and optimization tasks |
| **Constraint** | ✅ COMPLETE | 25 tags cover all major non-functional requirements including performance, security, scalability, maintainability, and compliance |
| **Agentic** | ✅ COMPLETE | 19 tags cover all major agent capabilities including file operations, tool use, reasoning, planning, and multi-step workflows |
| **Context** | ✅ COMPLETE | 9 tags cover all context complexity levels from single-file to multi-repository scenarios |

### Metadata Quality Metrics

- **Alias Coverage**: 99.7% (Library), 100% (Domain, Language, Task, Constraint, Agentic, Context)
- **Description Coverage**: 100% across all categories
- **Difficulty Classification**: 100% (Concept tags)
- **Granularity Classification**: 100% (Library tags)
- **Language Scope**: 18 languages covered (Library tags)
- **Multi-source Metrics**: 80.5% (Library tags)

### Gap Analysis Results

After systematic review, **no significant gaps remain**:
- Language: All major and emerging languages covered
- Library: Comprehensive ecosystem coverage across 18 languages
- Domain: Traditional, emerging, specialized, and cross-cutting domains complete
- Concept: Fundamentals, advanced concepts, and engineering practices complete
- Task/Constraint/Agentic/Context: All categories at optimal size with full coverage

## Orthogonality Analysis

Validation confirms **strong orthogonality** with minimal conflicts:

### Cross-Category Checks

✅ **Name Uniqueness**: No duplicate tag names across categories
- All 626 tags have unique names
- Case-insensitive checks pass

✅ **Alias Conflicts**: Minimal and intentional
- Analyzed all aliases across categories
- Conflicts are semantic (e.g., "ml" could mean Machine Learning domain or ML library)
- These conflicts are acceptable as context disambiguates

✅ **Category Boundaries**: Clear separation of concerns
- **Language** vs **Library**: Language = programming language itself; Library = framework/tool in that language
- **Domain** vs **Task**: Domain = application area; Task = type of work performed
- **Concept** vs **Library**: Concept = abstract programming idea; Library = concrete implementation
- **Constraint** vs **Task**: Constraint = non-functional requirement; Task = functional activity

### Validation Results

```
Total tags: 626
Categories: 8
Validation errors: 0
Orthogonality: PASS
Schema compliance: PASS
Referential integrity: PASS
```

### Design Decisions Supporting Orthogonality

1. **Language-scoped concepts**: Language-specific concepts (e.g., Rust's Borrow Checker) placed in Concept category with `language_scope` metadata, maintaining orthogonality while capturing applicability

2. **Mixed hierarchy**: Hierarchical subcategories (Library, Concept) prevent category explosion while maintaining flat structure for simpler categories

3. **Clear definitions**: Each category has explicit inclusion/exclusion criteria documented in taxonomy.yaml

## Production Readiness

The taxonomy is **ready for production use** in SFT data generation:

✅ **Comprehensive Coverage**: 626 tags across 8 categories cover the full spectrum of programming capabilities
✅ **High Quality**: 99.7%+ alias coverage, 100% description coverage, 0 validation errors
✅ **Orthogonal Design**: Clear category boundaries, minimal conflicts, strong separation of concerns
✅ **Well Documented**: Complete schema, usage guidelines, granularity guidelines, and repository structure docs
✅ **Validated**: Automated validation framework ensures ongoing quality
✅ **Maintainable**: Clear contribution workflow, normalization tools, and quality checks

## Contributing

To add new tags:

1. Collect tags using `collect_tags.py` or manually create JSON
2. Normalize with `normalize_tags.py`
3. Validate with `validate_taxonomy.py`
4. Ensure validation passes (no errors)
5. Submit changes

## License

This taxonomy is part of the SFT data generation project.
