## 1. Setup Project Structure

- [x] 1.1 Create directory structure: taxonomy/, taxonomy/tags/, scripts/
- [x] 1.2 Create taxonomy.yaml with 8 category definitions
- [x] 1.3 Create empty YAML files for each category in tags/ directory
- [x] 1.4 Add Python dependencies (pyyaml, anthropic/openai SDK) to requirements.txt

## 2. Implement Taxonomy Schema

- [x] 2.1 Define taxonomy.yaml with all 8 categories (Language, Library, Domain, Concept, Task, Constraint, Agentic, Context)
- [x] 2.2 Add hierarchical subcategories for Library (Web, Data, Infrastructure, Testing, Database)
- [x] 2.3 Add hierarchical subcategories for Concept (Fundamentals, Advanced, Engineering)
- [x] 2.4 Document tag schema structure in taxonomy.yaml comments

## 3. Build Tag Collection Script

- [x] 3.1 Create scripts/collect_tags.py with CLI interface
- [x] 3.2 Implement Language tag collection from TIOBE/GitHub stats
- [x] 3.3 Implement Library tag collection from awesome-lists and package registries
- [x] 3.4 Implement Concept tag collection from educational sources
- [x] 3.5 Implement Domain, Task, Constraint, Agentic, Context tag collection
- [x] 3.6 Add LLM-assisted extraction function for unstructured sources
- [x] 3.7 Add provenance tracking (source field) for all collected tags
- [x] 3.8 Output collected tags to intermediate JSON format for review

## 4. Build Tag Normalization Script

- [x] 4.1 Create scripts/normalize_tags.py with CLI interface
- [x] 4.2 Implement deduplication logic (exact match, alias match, case-insensitive)
- [x] 4.3 Implement tag ID normalization (kebab-case conversion)
- [x] 4.4 Implement alias conflict detection and resolution
- [x] 4.5 Add metadata enrichment (descriptions, language_scope, related_tags)
- [x] 4.6 Add granularity validation (flag too specific/broad tags)
- [x] 4.7 Implement category and subcategory assignment
- [x] 4.8 Output normalized tags to tags/*.yaml files (sorted alphabetically)

## 5. Build Taxonomy Validation Script

- [x] 5.1 Create scripts/validate_taxonomy.py with CLI interface
- [x] 5.2 Implement category orthogonality validation
- [x] 5.3 Implement tag uniqueness validation (IDs, aliases, names)
- [x] 5.4 Implement schema compliance validation (required fields, valid enums)
- [x] 5.5 Implement referential integrity validation (category, subcategory, related_tags, language_scope)
- [x] 5.6 Implement metadata quality checks (description length, alias format)
- [x] 5.7 Implement distribution checks (empty categories, imbalanced subcategories)
- [x] 5.8 Generate validation report with errors, warnings, and statistics
- [x] 5.9 Set appropriate exit codes (0 for valid, non-zero for errors)

## 6. Populate Initial Tag Set

- [x] 6.1 Run collect_tags.py for Language category (target: 50-100 tags)
- [x] 6.2 Run collect_tags.py for Library category (target: 100-200 initial tags)
- [x] 6.3 Run collect_tags.py for Concept category (target: 50-100 tags)
- [x] 6.4 Run collect_tags.py for remaining categories (target: 20-50 each)
- [x] 6.5 Review and validate collected tags manually
- [x] 6.6 Run normalize_tags.py to deduplicate and enrich metadata
- [x] 6.7 Run validate_taxonomy.py and fix any errors
- [x] 6.8 Commit initial taxonomy to repository

## 7. Documentation

- [x] 7.1 Create README.md explaining taxonomy structure and usage
- [x] 7.2 Document tag collection process and sources
- [x] 7.3 Document tag normalization guidelines (granularity, naming conventions)
- [x] 7.4 Add examples of well-formed tags for each category
- [x] 7.5 Document validation rules and how to fix common errors
- [x] 7.6 Add usage examples for scripts (collect, normalize, validate)
