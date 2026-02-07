# task-expansion Specification

## Purpose
Expand Task taxonomy with 6 fundamental programming tasks and add descriptions to all tags. Clarify the boundary between Task (user goals) and Agentic (agent capabilities) dimensions.

## ADDED Requirements

### Requirement: Add bug-fixing task
The system SHALL provide a `bug-fixing` task tag for identifying and fixing bugs in code.

#### Scenario: Bug-fixing task definition
- **WHEN** defining the `bug-fixing` task tag
- **THEN** it SHALL represent the goal of fixing bugs and errors in existing code

#### Scenario: Bug-fixing vs debugging distinction
- **WHEN** comparing `bug-fixing` (Task) to `debugging` (Agentic)
- **THEN** `bug-fixing` SHALL represent the user's goal (fix this bug)
- **AND** `debugging` SHALL represent the agent's capability (ability to debug)

#### Scenario: Bug-fixing data characteristics
- **WHEN** classifying bug-fixing training data
- **THEN** it SHALL include: broken/incorrect code as input, corrected code as output, and error description

### Requirement: Add feature-implementation task
The system SHALL provide a `feature-implementation` task tag for implementing new functionality.

#### Scenario: Feature-implementation definition
- **WHEN** defining the `feature-implementation` task tag
- **THEN** it SHALL represent implementing new features or functionality

#### Scenario: Feature vs bug-fixing distinction
- **WHEN** comparing feature-implementation to bug-fixing
- **THEN** feature-implementation SHALL be for adding NEW functionality
- **AND** bug-fixing SHALL be for correcting EXISTING code

#### Scenario: Feature-implementation metadata
- **WHEN** defining feature-implementation tag metadata
- **THEN** it SHALL include aliases: `feature-development`, `implementation`, `feature`

### Requirement: Add testing task
The system SHALL provide a `testing` task tag distinct from test-generation capability.

#### Scenario: Testing task definition
- **WHEN** defining the `testing` task tag
- **THEN** it SHALL represent the user's goal of writing tests

#### Scenario: Testing vs test-generation distinction
- **WHEN** comparing `testing` (Task) to `test-generation` (Agentic)
- **THEN** `testing` SHALL represent "I want to write tests" (user goal)
- **AND** `test-generation` SHALL represent agent's ability to generate test code

#### Scenario: Testing task types
- **WHEN** using the testing task tag
- **THEN** it SHALL cover unit tests, integration tests, and end-to-end tests

#### Scenario: Testing and test-generation coexistence
- **WHEN** a code sample demonstrates writing tests
- **THEN** it MAY be tagged with both Task(testing) and Agentic(test-generation)

### Requirement: Add error-handling task
The system SHALL provide an `error-handling` task tag for adding error handling and validation.

#### Scenario: Error-handling definition
- **WHEN** defining the `error-handling` task tag
- **THEN** it SHALL represent adding error handling, validation, and graceful degradation

#### Scenario: Error-handling vs bug-fixing distinction
- **WHEN** comparing error-handling to bug-fixing
- **THEN** error-handling SHALL be for ADDING error handling to prevent errors
- **AND** bug-fixing SHALL be for FIXING existing errors

#### Scenario: Error-handling examples
- **WHEN** applying the error-handling tag
- **THEN** it SHALL include: adding try-catch blocks, adding input validation, adding error messages, implementing graceful degradation

### Requirement: Add logging task
The system SHALL provide a `logging` task tag for adding log statements and instrumentation.

#### Scenario: Logging task definition
- **WHEN** defining the `logging` task tag
- **THEN** it SHALL represent adding logging statements and instrumentation to code

#### Scenario: Logging vs monitoring distinction
- **WHEN** comparing logging to monitoring
- **THEN** `logging` SHALL be for adding log statements to code
- **AND** `monitoring` SHALL be for setting up monitoring infrastructure

#### Scenario: Logging vs observable constraint
- **WHEN** comparing logging (Task) to observable (Constraint)
- **THEN** `logging` SHALL represent the task of adding logging
- **AND** `observable` SHALL represent that code HAS logging/metrics/tracing

### Requirement: Add code-review-task
The system SHALL provide a `code-review-task` tag distinct from code-review capability.

#### Scenario: Code-review-task definition
- **WHEN** defining the `code-review-task` tag
- **THEN** it SHALL represent the goal of reviewing code and providing feedback

#### Scenario: Code-review-task vs code-review capability
- **WHEN** comparing `code-review-task` (Task) to `code-review` (Agentic)
- **THEN** `code-review-task` SHALL represent "review this code" (user goal)
- **AND** `code-review` SHALL represent agent's code review capability

#### Scenario: Code-review-task naming
- **WHEN** naming the code-review task tag
- **THEN** it SHALL use `-task` suffix to avoid ID conflict with Agentic dimension

#### Scenario: Code-review-task coexistence
- **WHEN** a code sample demonstrates code review
- **THEN** it MAY be tagged with both Task(code-review-task) and Agentic(code-review)

### Requirement: Add descriptions to all task tags
The system SHALL require descriptions for all Task taxonomy tags.

#### Scenario: Description format
- **WHEN** adding descriptions to task tags
- **THEN** descriptions SHALL be 1-2 sentences
- **AND** SHALL start with what the task accomplishes
- **AND** SHALL focus on objective, not method

#### Scenario: Existing tags get descriptions
- **WHEN** implementing this change
- **THEN** all 15 existing task tags SHALL receive descriptions
- **AND** all 6 new task tags SHALL include descriptions

#### Scenario: Description consistency
- **WHEN** writing descriptions
- **THEN** they SHALL follow consistent format across all task tags

### Requirement: Maintain Task vs Agentic orthogonality
The system SHALL maintain clear distinction between Task and Agentic dimensions.

#### Scenario: Task describes user goals
- **WHEN** defining Task tags
- **THEN** they SHALL describe what the user wants to accomplish (goals/objectives)

#### Scenario: Agentic describes agent capabilities
- **WHEN** comparing to Agentic dimension
- **THEN** Agentic tags SHALL describe what capabilities the agent uses (methods/abilities)

#### Scenario: Task and Agentic coexistence
- **WHEN** annotating training data
- **THEN** the same sample MAY have both Task and Agentic tags
- **AND** Task SHALL represent what user asked for
- **AND** Agentic SHALL represent what capability agent demonstrated

#### Scenario: Example combinations
- **WHEN** a sample shows bug fixing
- **THEN** it MAY be tagged Task(bug-fixing) + Agentic(debugging) + Agentic(code-analysis)

### Requirement: Task tag metadata structure
The system SHALL define complete metadata for all task tags.

#### Scenario: Required fields for new tasks
- **WHEN** adding new task tags
- **THEN** each SHALL include: id, name, category (Task), aliases, description, source

#### Scenario: Bug-fixing tag structure
- **WHEN** defining bug-fixing tag
- **THEN** it SHALL have:
  - id: `bug-fixing`
  - name: `Bug Fixing`
  - aliases: `bug-fix`, `fix-bug`, `debugging-task`
  - description: "Fix bugs and errors in existing code. Identify root cause and correct faulty logic or implementation."

#### Scenario: Feature-implementation tag structure
- **WHEN** defining feature-implementation tag
- **THEN** it SHALL have:
  - id: `feature-implementation`
  - aliases: `feature-development`, `implementation`, `feature`
  - description: "Implement new features or functionality. Add new capabilities to existing codebase."

#### Scenario: Testing tag structure
- **WHEN** defining testing tag
- **THEN** it SHALL have:
  - id: `testing`
  - aliases: `test`, `write-tests`, `test-development`
  - description: "Write tests for code. Create unit tests, integration tests, or end-to-end tests."

#### Scenario: Error-handling tag structure
- **WHEN** defining error-handling tag
- **THEN** it SHALL have:
  - id: `error-handling`
  - aliases: `error-handling`, `exception-handling`, `validation`
  - description: "Add error handling and validation to code. Implement try-catch blocks, input validation, and graceful degradation."

#### Scenario: Logging tag structure
- **WHEN** defining logging tag
- **THEN** it SHALL have:
  - id: `logging`
  - aliases: `logging`, `add-logs`, `instrumentation`
  - description: "Add logging statements and instrumentation to code. Insert log messages for debugging and monitoring."

#### Scenario: Code-review-task tag structure
- **WHEN** defining code-review-task tag
- **THEN** it SHALL have:
  - id: `code-review-task`
  - aliases: `code-review-task`, `review`, `peer-review`
  - description: "Review code and provide feedback. Identify issues, suggest improvements, and ensure quality standards."

### Requirement: Final taxonomy size
The system SHALL expand Task taxonomy from 15 to 21 tags.

#### Scenario: Tag count verification
- **WHEN** completing this expansion
- **THEN** Task taxonomy SHALL contain exactly 21 tags
- **AND** SHALL include 15 existing + 6 new tags

#### Scenario: All tags have complete metadata
- **WHEN** completing this expansion
- **THEN** all 21 tags SHALL have: id, name, category, aliases, description, source
