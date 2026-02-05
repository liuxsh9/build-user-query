## ADDED Requirements

### Requirement: Define three granularity levels
The system SHALL define three explicit granularity levels for Library tags: library-level, module-level, and component-level.

#### Scenario: Library-level tag definition
- **WHEN** a tag represents an entire framework or library used as a whole
- **THEN** it SHALL be classified as library-level (e.g., react, django, pytorch)

#### Scenario: Module-level tag definition
- **WHEN** a tag represents a major subsystem or module with distinct capabilities
- **THEN** it SHALL be classified as module-level (e.g., django-orm, pytorch-nn, pandas-dataframe)

#### Scenario: Component-level tag definition
- **WHEN** a tag represents a specific feature or API frequently used independently
- **THEN** it SHALL be classified as component-level (e.g., react-hooks, pandas-groupby)

### Requirement: Provide decision criteria for each level
The system SHALL provide clear decision criteria to determine appropriate granularity level for each tag.

#### Scenario: Library-level criteria
- **WHEN** evaluating if a tag should be library-level
- **THEN** it MUST meet criteria: library is monolithic OR commonly used as a whole

#### Scenario: Module-level criteria
- **WHEN** evaluating if a tag should be module-level
- **THEN** it MUST meet criteria: module represents distinct capability worth tracking separately

#### Scenario: Component-level criteria
- **WHEN** evaluating if a tag should be component-level
- **THEN** it MUST meet criteria: component is frequently used independently AND represents learnable skill

### Requirement: Document examples for each level
The system SHALL provide concrete examples for each granularity level across different library subcategories.

#### Scenario: Examples across subcategories
- **WHEN** guidelines are consulted
- **THEN** they MUST include examples from Web, Data, Infrastructure, Testing, and Database subcategories

#### Scenario: Edge case examples
- **WHEN** ambiguous cases exist
- **THEN** guidelines MUST document the decision rationale for edge cases

### Requirement: Add granularity metadata to tag schema
The system SHALL extend the tag schema to include a granularity field.

#### Scenario: Granularity field definition
- **WHEN** a Library tag is defined
- **THEN** it MUST include granularity field with enum values: library, module, component

#### Scenario: Granularity field validation
- **WHEN** validating taxonomy
- **THEN** system SHALL verify all Library tags have valid granularity values
