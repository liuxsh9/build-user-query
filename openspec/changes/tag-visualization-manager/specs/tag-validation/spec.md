## ADDED Requirements

### Requirement: Validate required fields
The system SHALL enforce required fields based on tag category.

#### Scenario: Validate common required fields
- **WHEN** system validates any tag
- **THEN** system ensures id, name, category, and source fields are present and non-empty

#### Scenario: Validate Concept-specific fields
- **WHEN** system validates a Concept tag
- **THEN** system ensures subcategory and difficulty fields are present

#### Scenario: Validate Library-specific fields
- **WHEN** system validates a Library tag
- **THEN** system ensures subcategory, language_scope, and granularity fields are present

#### Scenario: Validate Language-specific fields
- **WHEN** system validates a Language tag
- **THEN** system ensures aliases field is present and non-empty

#### Scenario: Validate Domain-specific fields
- **WHEN** system validates a Domain tag
- **THEN** system ensures description and aliases fields are present

### Requirement: Validate field formats
The system SHALL enforce format constraints on field values.

#### Scenario: Validate ID format
- **WHEN** system validates tag ID
- **THEN** system ensures ID contains only lowercase letters, numbers, and hyphens (regex: ^[a-z0-9-]+$)

#### Scenario: Validate category enum
- **WHEN** system validates category field
- **THEN** system ensures value is one of: Concept, Library, Language, Domain, Constraint, Task, Agentic, Context

#### Scenario: Validate difficulty enum
- **WHEN** system validates difficulty field on Concept tag
- **THEN** system ensures value is one of: basic, intermediate, advanced

#### Scenario: Validate source enum
- **WHEN** system validates source field
- **THEN** system ensures value is one of: curated-list, educational-sources, TIOBE, GitHub, manual

#### Scenario: Validate weighted score range
- **WHEN** system validates weighted_score field
- **THEN** system ensures value is a number between 0 and 1 inclusive

### Requirement: Validate subcategory consistency
The system SHALL ensure subcategory values match their parent category.

#### Scenario: Validate Concept subcategories
- **WHEN** system validates Concept tag with subcategory
- **THEN** system ensures subcategory is one of: Fundamentals, Advanced, Engineering

#### Scenario: Validate Library subcategories
- **WHEN** system validates Library tag with subcategory
- **THEN** system ensures subcategory is one of: Web, Database, Data, Testing, Other

### Requirement: Validate ID uniqueness
The system SHALL ensure tag IDs are unique across all categories.

#### Scenario: Reject duplicate ID within category
- **WHEN** user creates tag with ID that exists in same category
- **THEN** system returns error "Tag with ID {id} already exists in {category}"

#### Scenario: Reject duplicate ID across categories
- **WHEN** user creates tag with ID that exists in different category
- **THEN** system returns error "Tag with ID {id} already exists in {other_category}"

#### Scenario: Allow ID updates if still unique
- **WHEN** user updates tag ID to a new unique value
- **THEN** system accepts the change

### Requirement: Validate language scope references
The system SHALL ensure language_scope values reference valid Language tags.

#### Scenario: Validate each language scope entry
- **WHEN** system validates tag with language_scope field
- **THEN** system ensures each value in language_scope array corresponds to an existing Language tag ID

#### Scenario: Reject invalid language reference
- **WHEN** user adds "invalid-lang" to language_scope
- **THEN** system returns error "Invalid language_scope: invalid-lang is not a valid Language tag"

#### Scenario: Allow empty language scope
- **WHEN** tag has no language_scope field or empty array
- **THEN** system accepts tag (language_scope is optional for most categories)

### Requirement: Validate aliases uniqueness
The system SHALL ensure aliases within a tag are unique.

#### Scenario: Reject duplicate aliases
- **WHEN** user adds duplicate values to aliases array (e.g., ["js", "js"])
- **THEN** system returns error "Aliases must be unique"

#### Scenario: Accept unique aliases
- **WHEN** user provides aliases array with all unique values
- **THEN** system accepts the tag

### Requirement: Validate relationship fields
The system SHALL validate relationship fields when present (reserved for future use).

#### Scenario: Validate prerequisite references
- **WHEN** tag has prerequisites field
- **THEN** system ensures each ID in prerequisites array corresponds to an existing tag

#### Scenario: Prevent self-reference in prerequisites
- **WHEN** tag includes its own ID in prerequisites array
- **THEN** system returns error "Tag cannot be a prerequisite of itself"

#### Scenario: Validate related references
- **WHEN** tag has related field
- **THEN** system ensures each ID in related array corresponds to an existing tag

### Requirement: Client-side validation
The system SHALL provide immediate validation feedback in the UI before submitting to server.

#### Scenario: Show field-level errors
- **WHEN** user fills in a field with invalid value
- **THEN** system displays error message below the field immediately on blur

#### Scenario: Disable submit when invalid
- **WHEN** form contains validation errors
- **THEN** system disables the save button and shows error summary

#### Scenario: Real-time ID format check
- **WHEN** user types in ID field
- **THEN** system displays format guidance and validates format as user types

### Requirement: Server-side validation
The system SHALL enforce all validation rules on the server as final authority.

#### Scenario: Validate before write
- **WHEN** server receives create or update request
- **THEN** system validates complete tag object before writing to YAML file

#### Scenario: Return structured errors
- **WHEN** server validation fails
- **THEN** system returns HTTP 400 with JSON object containing array of error messages

#### Scenario: Block invalid writes
- **WHEN** tag fails server validation
- **THEN** system does not write to YAML file and preserves existing file state
