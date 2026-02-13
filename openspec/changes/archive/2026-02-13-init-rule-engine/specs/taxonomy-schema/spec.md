## MODIFIED Requirements

### Requirement: Define tag structure
The system SHALL define a tag schema with required and optional fields.

#### Scenario: Tag has required fields
- **WHEN** a tag is defined
- **THEN** it MUST have id, name, and category fields

#### Scenario: Tag supports optional metadata
- **WHEN** a tag is defined
- **THEN** it MAY have description, aliases, language_scope, difficulty, examples, related_tags, subcategory, granularity, weighted_score, paradigm, typing, runtime, use_cases, and source fields

#### Scenario: Tag ID is unique across taxonomy
- **WHEN** multiple tags are defined
- **THEN** no two tags SHALL have the same id

## ADDED Requirements

### Requirement: Define category selection mode
The system SHALL define whether each category uses single-select or multi-select labeling.

#### Scenario: Context category is single-select
- **WHEN** the Context category is used for labeling
- **THEN** exactly one tag SHALL be assigned per record

#### Scenario: All other categories are multi-select
- **WHEN** Language, Library, Domain, Concept, Task, Constraint, or Agentic categories are used for labeling
- **THEN** zero or more tags MAY be assigned per record
