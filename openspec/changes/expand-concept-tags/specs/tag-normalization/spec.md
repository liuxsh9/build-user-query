## ADDED Requirements

### Requirement: Validate difficulty levels during normalization
The system SHALL validate that all Concept tags have difficulty level metadata.

#### Scenario: Missing difficulty level
- **WHEN** normalizing a Concept tag without difficulty field
- **THEN** system SHALL flag validation warning

#### Scenario: Invalid difficulty value
- **WHEN** difficulty field contains value other than basic, intermediate, or advanced
- **THEN** system SHALL flag validation error

#### Scenario: Difficulty consistency check
- **WHEN** normalizing Concept tags
- **THEN** system SHALL verify difficulty aligns with subcategory expectations

### Requirement: Validate prerequisite relationships during normalization
The system SHALL validate prerequisite field references and detect circular dependencies.

#### Scenario: Prerequisite reference validation
- **WHEN** normalizing a Concept tag with prerequisites
- **THEN** system SHALL verify all prerequisite IDs exist in taxonomy

#### Scenario: Circular dependency detection
- **WHEN** normalizing Concept tags
- **THEN** system SHALL detect and flag circular prerequisite chains

#### Scenario: Prerequisite type validation
- **WHEN** prerequisite field is present
- **THEN** system SHALL verify it is an array of strings

### Requirement: Validate language_scope during normalization
The system SHALL validate language_scope references for Concept tags.

#### Scenario: Language reference validation
- **WHEN** normalizing a Concept tag with language_scope
- **THEN** system SHALL verify all language IDs exist in Language category

#### Scenario: Language-specific concept detection
- **WHEN** concept ID contains language name but lacks language_scope
- **THEN** system SHALL flag validation warning
