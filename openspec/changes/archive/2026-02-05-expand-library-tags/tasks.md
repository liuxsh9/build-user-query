## 1. Document Granularity Guidelines

- [x] 1.1 Create GRANULARITY_GUIDELINES.md with three-tier system definition
- [x] 1.2 Document decision criteria for library-level tags
- [x] 1.3 Document decision criteria for module-level tags
- [x] 1.4 Document decision criteria for component-level tags
- [x] 1.5 Add examples for each level across all 5 subcategories
- [x] 1.6 Document edge cases and decision rationale

## 2. Extend Tag Schema

- [ ] 2.1 Add granularity field to tag schema in taxonomy.yaml
- [ ] 2.2 Update tag schema documentation with granularity enum (library, module, component)
- [ ] 2.3 Update existing Library tags with granularity metadata
- [ ] 2.4 Update validation script to check granularity field

## 3. Build Automated Alias Expansion Tool

- [ ] 3.1 Create scripts/expand_aliases.py with CLI interface
- [ ] 3.2 Implement import statement parser for Python (extract "import X as Y" patterns)
- [ ] 3.3 Implement import statement parser for JavaScript/TypeScript
- [ ] 3.4 Implement documentation mining (extract abbreviations from docs)
- [ ] 3.5 Implement Stack Overflow terminology analyzer
- [ ] 3.6 Implement case variation generator (lowercase, uppercase, kebab-case, camelCase)
- [ ] 3.7 Implement confidence scoring algorithm
- [ ] 3.8 Implement human validation workflow (auto-approve >0.8, flag 0.5-0.8, discard <0.5)
- [ ] 3.9 Create and maintain alias blocklist file

## 4. Implement Multi-Source Collection

- [ ] 4.1 Extend scripts/collect_tags.py to support multiple sources
- [ ] 4.2 Implement Stack Overflow API integration (weight: 0.4)
- [ ] 4.3 Implement npm registry API integration (weight: 0.3)
- [ ] 4.4 Implement PyPI API integration (weight: 0.3)
- [ ] 4.5 Implement GitHub Topics API integration (weight: 0.2)
- [ ] 4.6 Implement academic database integration (arXiv, ACM, IEEE) (weight: 0.1)
- [ ] 4.7 Implement weighted score calculation
- [ ] 4.8 Implement source-specific metrics recording
- [ ] 4.9 Add granularity classification during collection

## 5. Update Normalization Script

- [ ] 5.1 Integrate alias expansion tool into normalize_tags.py
- [ ] 5.2 Add granularity validation logic
- [ ] 5.3 Update to preserve source-specific metrics
- [ ] 5.4 Add aggregate weighted score calculation
- [ ] 5.5 Update YAML output to include new metadata fields

## 6. Collect Library Tags - Web Subcategory

- [ ] 6.1 Run multi-source collection for Web libraries (target: 80 tags)
- [ ] 6.2 Review and classify granularity for collected tags
- [ ] 6.3 Run alias expansion tool
- [ ] 6.4 Validate and approve aliases
- [ ] 6.5 Run normalization with new features
- [ ] 6.6 Validate output with validate_taxonomy.py

## 7. Collect Library Tags - Data Subcategory

- [ ] 7.1 Run multi-source collection for Data libraries (target: 70 tags)
- [ ] 7.2 Review and classify granularity for collected tags
- [ ] 7.3 Run alias expansion tool
- [ ] 7.4 Validate and approve aliases
- [ ] 7.5 Run normalization with new features
- [ ] 7.6 Validate output with validate_taxonomy.py

## 8. Collect Library Tags - Infrastructure Subcategory

- [ ] 8.1 Run multi-source collection for Infrastructure libraries (target: 60 tags)
- [ ] 8.2 Review and classify granularity for collected tags
- [ ] 8.3 Run alias expansion tool
- [ ] 8.4 Validate and approve aliases
- [ ] 8.5 Run normalization with new features
- [ ] 8.6 Validate output with validate_taxonomy.py

## 9. Collect Library Tags - Testing Subcategory

- [ ] 9.1 Run multi-source collection for Testing libraries (target: 50 tags)
- [ ] 9.2 Review and classify granularity for collected tags
- [ ] 9.3 Run alias expansion tool
- [ ] 9.4 Validate and approve aliases
- [ ] 9.5 Run normalization with new features
- [ ] 9.6 Validate output with validate_taxonomy.py

## 10. Collect Library Tags - Database Subcategory

- [ ] 10.1 Run multi-source collection for Database libraries (target: 40 tags)
- [ ] 10.2 Review and classify granularity for collected tags
- [ ] 10.3 Run alias expansion tool
- [ ] 10.4 Validate and approve aliases
- [ ] 10.5 Run normalization with new features
- [ ] 10.6 Validate output with validate_taxonomy.py

## 11. Final Validation and Documentation

- [ ] 11.1 Run full taxonomy validation
- [ ] 11.2 Verify total Library tag count (~300)
- [ ] 11.3 Verify granularity distribution across levels
- [ ] 11.4 Verify alias coverage (target: >90% of tags have aliases)
- [ ] 11.5 Update README.md with new statistics
- [ ] 11.6 Document multi-source collection process
- [ ] 11.7 Document alias expansion workflow
- [ ] 11.8 Add usage examples for new tools
