## ADDED Requirements

### Requirement: Validate category orthogonality
The system SHALL ensure categories remain orthogonal with no overlapping tags.

#### Scenario: No tag appears in multiple categories
- **WHEN** validating taxonomy
- **THEN** system SHALL verify each tag ID appears in exactly one category

#### Scenario: Category boundaries are clear
- **WHEN** validating taxonomy
- **THEN** system SHALL check that no tag could reasonably belong to multiple categories

### Requirement: Validate tag uniqueness
The system SHALL ensure tag IDs and aliases are unique across the taxonomy.

#### Scenario: Tag IDs are globally unique
- **WHEN** validating taxonomy
- **THEN** system SHALL verify no duplicate tag IDs exist

#### Scenario: Aliases don't conflict across tags
- **WHEN** validating taxonomy
- **THEN** system SHALL verify no alias appears in multiple tags

#### Scenario: Tag names are unique within category
- **WHEN** validating taxonomy
- **THEN** system SHALL verify no duplicate tag names within same category

### Requirement: Validate schema compliance
The system SHALL verify all taxonomy files conform to defined schemas.

#### Scenario: Taxonomy file matches schema
- **WHEN** validating taxonomy.yaml
- **THEN** system SHALL verify it contains all required fields and valid category definitions

#### Scenario: Tag files match schema
- **WHEN** validating tags/*.yaml
- **THEN** system SHALL verify each tag has required fields (id, name, category)

#### Scenario: Hierarchical categories have subcategories
- **WHEN** validating hierarchical category tags
- **THEN** system SHALL verify each tag has valid subcategory field

### Requirement: Validate referential integrity
The system SHALL ensure all references between taxonomy elements are valid.

#### Scenario: Tag category exists
- **WHEN** validating a tag
- **THEN** system SHALL verify its category field matches a defined category in taxonomy.yaml

#### Scenario: Tag subcategory exists
- **WHEN** validating a hierarchical tag
- **THEN** system SHALL verify its subcategory exists in the category definition

#### Scenario: Related tags exist
- **WHEN** validating related_tags field
- **THEN** system SHALL verify all referenced tag IDs exist in taxonomy

#### Scenario: Language scope is valid
- **WHEN** validating language_scope field
- **THEN** system SHALL verify all referenced languages exist as Language tags

### Requirement: Validate tag metadata quality
The system SHALL check that tag metadata meets quality standards.

#### Scenario: Descriptions are concise
- **WHEN** validating tag descriptions
- **THEN** system SHALL flag descriptions longer than 200 characters

#### Scenario: Difficulty levels are valid
- **WHEN** validating difficulty field
- **THEN** system SHALL verify value is one of: basic, intermediate, advanced

#### Scenario: Aliases are lowercase
- **WHEN** validating aliases
- **THEN** system SHALL verify all aliases are lowercase

### Requirement: Validate tag distribution
The system SHALL check that tags are reasonably distributed across categories.

#### Scenario: No category is empty
- **WHEN** validating taxonomy
- **THEN** system SHALL verify each category has at least one tag

#### Scenario: Flag imbalanced subcategories
- **WHEN** validating hierarchical categories
- **THEN** system SHALL flag if one subcategory has >80% of tags

### Requirement: Generate validation report
The system SHALL produce a comprehensive validation report.

#### Scenario: Report includes all errors
- **WHEN** validation completes
- **THEN** system SHALL list all schema violations, uniqueness conflicts, and referential integrity errors

#### Scenario: Report includes warnings
- **WHEN** validation completes
- **THEN** system SHALL list quality issues like missing descriptions or imbalanced distributions

#### Scenario: Report includes statistics
- **WHEN** validation completes
- **THEN** system SHALL include tag counts per category, coverage metrics, and metadata completeness

#### Scenario: Exit code reflects validation status
- **WHEN** validation script completes
- **THEN** system SHALL exit with code 0 if valid, non-zero if errors found
