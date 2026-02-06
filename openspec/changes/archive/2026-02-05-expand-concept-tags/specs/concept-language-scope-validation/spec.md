## ADDED Requirements

### Requirement: Validate language_scope for language-specific concepts
The system SHALL ensure language-specific Concept tags have proper language_scope metadata.

#### Scenario: Language-specific concept with scope
- **WHEN** a concept is specific to one or more languages (e.g., "borrow-checker" for Rust)
- **THEN** system SHALL verify language_scope field is populated

#### Scenario: Language-agnostic concept without scope
- **WHEN** a concept applies across all languages (e.g., "variables", "loops")
- **THEN** system SHALL allow empty or omitted language_scope

#### Scenario: Multiple language scope
- **WHEN** a concept applies to multiple specific languages (e.g., "type-inference" for Rust, TypeScript, Haskell)
- **THEN** system SHALL list all applicable languages in language_scope

### Requirement: Detect missing language_scope
The system SHALL flag concepts with language-specific names but missing language_scope.

#### Scenario: Language name in concept ID
- **WHEN** concept ID contains language name (e.g., "python-decorators", "rust-lifetimes")
- **THEN** system SHALL verify language_scope includes that language

#### Scenario: Language-specific terminology
- **WHEN** concept uses language-specific terminology
- **THEN** system SHALL flag for language_scope review if missing

### Requirement: Validate language_scope references
The system SHALL validate that language_scope values reference existing Language tags.

#### Scenario: Valid language reference
- **WHEN** language_scope contains a language ID that exists in taxonomy
- **THEN** system SHALL accept the reference

#### Scenario: Invalid language reference
- **WHEN** language_scope contains a non-existent language ID
- **THEN** system SHALL flag validation error

#### Scenario: Case-insensitive language matching
- **WHEN** validating language_scope references
- **THEN** system SHALL perform case-insensitive matching against Language tag IDs
