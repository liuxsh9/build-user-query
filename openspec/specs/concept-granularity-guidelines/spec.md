# concept-granularity-guidelines Specification

## Purpose
TBD - created by archiving change expand-concept-tags. Update Purpose after archive.
## Requirements
### Requirement: Define Fundamentals subcategory granularity
The system SHALL define granularity guidelines for Fundamentals subcategory concepts.

#### Scenario: Foundational concepts classification
- **WHEN** classifying a basic programming concept (variables, loops, conditionals)
- **THEN** system SHALL categorize it as Fundamentals level

#### Scenario: Language-agnostic fundamentals
- **WHEN** a fundamental concept applies across multiple languages
- **THEN** system SHALL document it without language_scope

#### Scenario: Language-specific fundamentals
- **WHEN** a fundamental concept is language-specific (e.g., Python list comprehensions)
- **THEN** system SHALL include language_scope metadata

### Requirement: Define Advanced subcategory granularity
The system SHALL define granularity guidelines for Advanced subcategory concepts.

#### Scenario: Complex concepts classification
- **WHEN** classifying advanced programming concepts (metaprogramming, concurrency, design patterns)
- **THEN** system SHALL categorize it as Advanced level

#### Scenario: Prerequisites for advanced concepts
- **WHEN** an advanced concept requires foundational knowledge
- **THEN** system SHALL document prerequisite relationships

### Requirement: Define Engineering subcategory granularity
The system SHALL define granularity guidelines for Engineering subcategory concepts.

#### Scenario: Practice and methodology classification
- **WHEN** classifying software engineering practices (testing, CI/CD, code review)
- **THEN** system SHALL categorize it as Engineering level

#### Scenario: Process-oriented concepts
- **WHEN** a concept describes a development process or methodology
- **THEN** system SHALL place it in Engineering subcategory

### Requirement: Document granularity decision criteria
The system SHALL provide clear criteria for assigning concepts to subcategories.

#### Scenario: Ambiguous concept classification
- **WHEN** a concept could fit multiple subcategories
- **THEN** system SHALL provide decision criteria with examples

#### Scenario: Edge case documentation
- **WHEN** edge cases arise in classification
- **THEN** system SHALL document rationale and precedent

