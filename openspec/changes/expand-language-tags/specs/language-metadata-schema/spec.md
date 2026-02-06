# language-metadata-schema Specification

## Purpose
Define structured metadata schema for Language tags to enable paradigm-based, type-system-based, and use-case-based query filtering. Extends taxonomy schema with four new fields: paradigm, typing, runtime, and use_cases.

## Requirements

### Requirement: Define paradigm metadata field
The system SHALL add a paradigm field to Language tags to represent programming paradigms.

#### Scenario: Paradigm field definition
- **WHEN** a Language tag is defined
- **THEN** it SHOULD include paradigm field as list[str] with values from controlled vocabulary

#### Scenario: Paradigm controlled vocabulary
- **WHEN** paradigm values are specified
- **THEN** they MUST be from: imperative, functional, object-oriented, declarative, logic, procedural, concurrent, event-driven

#### Scenario: Multiple paradigm support
- **WHEN** a language supports multiple paradigms (e.g., Scala is OOP + functional)
- **THEN** paradigm field SHALL accept multiple values in priority order

#### Scenario: Paradigm validation
- **WHEN** validating taxonomy
- **THEN** system SHALL verify paradigm values are from controlled vocabulary

### Requirement: Define typing metadata field
The system SHALL add a typing field to Language tags to represent type system characteristics.

#### Scenario: Typing field definition
- **WHEN** a Language tag is defined
- **THEN** it SHOULD include typing field as string with value from controlled vocabulary

#### Scenario: Typing controlled vocabulary
- **WHEN** typing value is specified
- **THEN** it MUST be one of: static, dynamic, gradual, duck, strong-static, weak-dynamic

#### Scenario: Typing examples
- **WHEN** defining typing for common languages
- **THEN** examples MUST include: Python (dynamic), Java (static), TypeScript (gradual), Go (strong-static)

#### Scenario: Typing validation
- **WHEN** validating taxonomy
- **THEN** system SHALL verify typing value is from controlled vocabulary

### Requirement: Define runtime metadata field
The system SHALL add a runtime field to Language tags to represent execution model.

#### Scenario: Runtime field definition
- **WHEN** a Language tag is defined
- **THEN** it SHOULD include runtime field as string with value from controlled vocabulary

#### Scenario: Runtime controlled vocabulary
- **WHEN** runtime value is specified
- **THEN** it MUST be one of: compiled, interpreted, jit, transpiled, hybrid

#### Scenario: Runtime examples
- **WHEN** defining runtime for common languages
- **THEN** examples MUST include: C (compiled), Python (interpreted), Java (jit), TypeScript (transpiled), JavaScript (hybrid)

#### Scenario: Runtime validation
- **WHEN** validating taxonomy
- **THEN** system SHALL verify runtime value is from controlled vocabulary

### Requirement: Define use_cases metadata field
The system SHALL add a use_cases field to Language tags to represent primary application domains.

#### Scenario: Use cases field definition
- **WHEN** a Language tag is defined
- **THEN** it SHOULD include use_cases field as list[str] with values from controlled vocabulary

#### Scenario: Use cases controlled vocabulary
- **WHEN** use_cases values are specified
- **THEN** they MUST be from: web, systems, data-science, mobile, embedded, scripting, devops, scientific, game-dev, blockchain, markup, config, build

#### Scenario: Multiple use cases support
- **WHEN** a language serves multiple domains (e.g., Python for web + data-science + scripting)
- **THEN** use_cases field SHALL accept multiple values in priority order

#### Scenario: Use cases examples
- **WHEN** defining use_cases for common languages
- **THEN** examples MUST include: JavaScript (["web", "scripting"]), Python (["data-science", "web", "scripting"]), C (["systems", "embedded"])

#### Scenario: Use cases validation
- **WHEN** validating taxonomy
- **THEN** system SHALL verify use_cases values are from controlled vocabulary

### Requirement: Update taxonomy schema definition
The system SHALL update taxonomy.yaml schema definition to include new metadata fields.

#### Scenario: Schema update for Language category
- **WHEN** taxonomy.yaml is updated
- **THEN** it MUST add optional fields: paradigm, typing, runtime, use_cases for Language tags

#### Scenario: Backward compatibility
- **WHEN** existing Language tags lack new metadata
- **THEN** validation SHALL allow missing metadata fields (optional, not required)

#### Scenario: Schema documentation
- **WHEN** schema is updated
- **THEN** it MUST include inline comments explaining each metadata field and controlled vocabulary

### Requirement: Provide metadata assignment guidelines
The system SHALL provide clear guidelines for assigning metadata values to languages.

#### Scenario: Paradigm assignment guideline
- **WHEN** assigning paradigm metadata
- **THEN** guidelines MUST specify: list paradigms in order of prominence (primary first)

#### Scenario: Typing assignment guideline
- **WHEN** assigning typing metadata for gradual typing
- **THEN** guidelines MUST specify: use "gradual" for languages with optional type annotations (TypeScript, Python 3.5+)

#### Scenario: Runtime assignment guideline
- **WHEN** assigning runtime for hybrid execution models
- **THEN** guidelines MUST specify: use "hybrid" for languages with both JIT and interpretation (JavaScript)

#### Scenario: Use cases assignment guideline
- **WHEN** assigning use_cases metadata
- **THEN** guidelines MUST specify: include all domains where language has significant adoption (>5% market share)

### Requirement: Enable metadata-based querying
The system SHALL support querying languages by metadata values.

#### Scenario: Query by single paradigm
- **WHEN** querying for functional languages
- **THEN** system SHALL return all languages with "functional" in paradigm list

#### Scenario: Query by multiple criteria
- **WHEN** querying for statically-typed compiled languages for systems programming
- **THEN** system SHALL return languages matching typing:"static" AND runtime:"compiled" AND use_cases contains "systems"

#### Scenario: Query validation
- **WHEN** query specifies metadata values
- **THEN** system SHALL validate query values against controlled vocabularies
