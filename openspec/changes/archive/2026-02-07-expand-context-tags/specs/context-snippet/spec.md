# context-snippet Specification

## Purpose
Define the `snippet` context tag for code fragments that are smaller than complete functions and may lack full execution context. Enable classification of documentation examples, tutorial code, and Q&A samples.

## ADDED Requirements

### Requirement: Define snippet context tag
The system SHALL provide a `snippet` context tag for code fragments smaller than complete functions.

#### Scenario: Snippet as smallest granularity
- **WHEN** classifying code by organizational granularity
- **THEN** `snippet` SHALL be the smallest unit, smaller than `single-function`

#### Scenario: Snippet lacks complete context
- **WHEN** code is a `snippet`
- **THEN** it MAY lack imports, full structure, or be incomplete/illustrative only

#### Scenario: Single-function is complete and runnable
- **WHEN** code is `single-function`
- **THEN** it SHALL have a complete function signature and be independently executable

### Requirement: Snippet identification criteria
The system SHALL define objective criteria for identifying snippets versus complete functions.

#### Scenario: Snippet missing imports
- **WHEN** code fragment uses variables/functions without defining or importing them
- **THEN** it SHALL be classified as `snippet`

#### Scenario: Snippet is illustrative example
- **WHEN** code is clearly for illustration (e.g., "Example:", "Usage:")
- **THEN** it SHALL be classified as `snippet`

#### Scenario: Snippet is incomplete block
- **WHEN** code is a partial implementation (e.g., inside a function body, missing context)
- **THEN** it SHALL be classified as `snippet`

#### Scenario: Single-function has signature and body
- **WHEN** code has a complete function definition with signature and implementation
- **AND** code can be executed or tested independently (given standard library)
- **THEN** it SHALL be classified as `single-function`

### Requirement: Snippet use cases
The system SHALL support snippet classification for common code fragment sources.

#### Scenario: Documentation examples
- **WHEN** code appears in API documentation as usage example
- **THEN** it MAY be classified as `snippet` if incomplete

#### Scenario: Tutorial code fragments
- **WHEN** code is from a tutorial showing a specific concept
- **AND** code lacks full context (e.g., "here's how to use map:")
- **THEN** it SHALL be classified as `snippet`

#### Scenario: Q&A site answers
- **WHEN** code is from StackOverflow or similar Q&A
- **AND** code is a short illustrative answer without full context
- **THEN** it SHALL be classified as `snippet`

#### Scenario: Inline code examples
- **WHEN** code is embedded in text as a brief example (< 10 lines typically)
- **AND** code demonstrates a concept without being a complete unit
- **THEN** it SHALL be classified as `snippet`

### Requirement: Snippet tag metadata
The system SHALL define metadata for the snippet context tag.

#### Scenario: Snippet tag structure
- **WHEN** defining the `snippet` tag
- **THEN** it SHALL have:
  - id: `snippet`
  - name: `Snippet`
  - category: `Context`
  - aliases: `snippet`, `code-snippet`, `fragment`, `example`
  - source: `context-expansion`

#### Scenario: Snippet description
- **WHEN** documenting the `snippet` tag
- **THEN** it SHALL describe: "Code fragment or snippet, smaller than a complete function, may lack imports or full context. Common in documentation and tutorials."

### Requirement: Granularity hierarchy
The system SHALL maintain a clear granularity hierarchy with snippet as the smallest unit.

#### Scenario: Complete granularity spectrum
- **WHEN** organizing context tags by size
- **THEN** the hierarchy SHALL be: `snippet` < `single-function` < `single-file` < `multi-file` < `module` < `repository`

#### Scenario: No overlap between snippet and function
- **WHEN** code meets single-function criteria (complete and runnable)
- **THEN** it SHALL NOT be classified as `snippet`

#### Scenario: Snippet to function boundary
- **WHEN** code is borderline (e.g., very simple one-liner function)
- **THEN** classification rule: if it has function signature and is runnable → `single-function`, otherwise → `snippet`

### Requirement: Context dimension orthogonality
The system SHALL maintain orthogonality between snippet context and other taxonomy dimensions.

#### Scenario: Snippet with task tags
- **WHEN** a snippet demonstrates testing code
- **THEN** it SHALL be tagged with both `Context(snippet)` and `Task(testing)`

#### Scenario: Snippet with concept tags
- **WHEN** a snippet illustrates async/await pattern
- **THEN** it SHALL be tagged with both `Context(snippet)` and `Concept(async-await)`

#### Scenario: Snippet with language tags
- **WHEN** a snippet is written in Python
- **THEN** it SHALL be tagged with both `Context(snippet)` and `Language(python)`

### Requirement: Classification edge cases
The system SHALL provide guidance for edge cases in snippet classification.

#### Scenario: One-line expression
- **WHEN** code is a single expression without function wrapper (e.g., `list(map(int, input().split()))`)
- **THEN** it SHALL be classified as `snippet`

#### Scenario: Lambda function
- **WHEN** code is a lambda expression (e.g., `lambda x: x * 2`)
- **THEN** it SHALL be classified as `snippet`

#### Scenario: Simple complete function
- **WHEN** code is a simple function with signature and body (e.g., `def add(a, b): return a + b`)
- **AND** it can run independently
- **THEN** it SHALL be classified as `single-function`, not `snippet`

#### Scenario: Function with missing imports
- **WHEN** code defines a function but uses undefined imports (e.g., uses `requests` without importing)
- **THEN** it SHALL be classified as `snippet`

### Requirement: Documentation and examples
The system SHALL provide clear examples distinguishing snippets from functions.

#### Scenario: Example of snippet
- **WHEN** providing snippet examples
- **THEN** examples SHALL include:
  - Expression: `x.sort(key=lambda x: x[1])`
  - Partial code: `for item in items: print(item.name)`
  - Missing context: `result = api.get_user(id)` (no api defined)

#### Scenario: Example of single-function
- **WHEN** providing single-function examples
- **THEN** examples SHALL include:
  - Complete function: `def factorial(n): return 1 if n <= 1 else n * factorial(n-1)`
  - Testable unit: `def is_prime(n): ...` (full implementation)

#### Scenario: Migration from ambiguous classification
- **WHEN** existing data was ambiguously classified
- **THEN** re-classification guidelines SHALL prioritize: "Can it execute independently?" test
