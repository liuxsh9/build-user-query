# constraint-optimization Specification

## Purpose
Define principles and requirements for objective, verifiable constraint tags in the taxonomy. Establish judgment criteria for all constraints and optimize existing tags for data annotation and gap detection.

## ADDED Requirements

### Requirement: Every constraint SHALL have objective judgment criteria
The system SHALL require explicit, objective judgment criteria for every constraint tag.

#### Scenario: Constraint with static analysis criteria
- **WHEN** a constraint can be verified through code structure analysis
- **THEN** the judgment criteria SHALL specify detectable patterns (e.g., "no malloc calls", "uses async/await syntax")

#### Scenario: Constraint with behavioral testing criteria
- **WHEN** a constraint requires runtime verification
- **THEN** the judgment criteria SHALL specify testable behaviors (e.g., "same input produces same output", "concurrent execution has no data races")

#### Scenario: Constraint with tool-based measurement criteria
- **WHEN** a constraint requires quantitative measurement
- **THEN** the judgment criteria SHALL specify measurement tools and thresholds (e.g., "has benchmark tests", "uses profiling tools")

#### Scenario: Constraint with compliance checklist criteria
- **WHEN** a constraint represents regulatory compliance
- **THEN** the judgment criteria SHALL reference official standards (e.g., "passes GDPR compliance checklist", "follows MISRA C rules")

#### Scenario: Rejection of subjective constraints
- **WHEN** a proposed constraint lacks objective judgment criteria
- **THEN** the system SHALL reject it or require reformulation with objective criteria

### Requirement: Remove subjective constraint tags
The system SHALL remove constraint tags that cannot be objectively evaluated.

#### Scenario: Remove readable constraint
- **WHEN** evaluating the `readable` constraint
- **THEN** it SHALL be removed because readability is highly subjective and developer-dependent

#### Scenario: Remove maintainable constraint
- **WHEN** evaluating the `maintainable` constraint
- **THEN** it SHALL be removed because maintainability is a composite of many factors without objective metrics

#### Scenario: Remove testable constraint
- **WHEN** evaluating the `testable` constraint
- **THEN** it SHALL be removed because it is ambiguous (has tests vs. easy to test) and overlaps with Concept dimension

### Requirement: Merge redundant performance constraints
The system SHALL consolidate performance-related constraints into unified tags with multi-dimensional criteria.

#### Scenario: Merge performance tags
- **WHEN** processing `high-performance`, `low-latency`, and `memory-efficient` constraints
- **THEN** they SHALL be merged into `performance-optimized` with judgment criteria covering time, space, and latency optimization

#### Scenario: Preserve performance tag aliases
- **WHEN** merging performance tags
- **THEN** original tag names SHALL be preserved as aliases for backward compatibility

#### Scenario: Performance optimization judgment criteria
- **WHEN** determining if code is `performance-optimized`
- **THEN** criteria SHALL include: uses profiling/benchmarking tools, applies algorithmic optimizations, uses efficient data structures, or has documented performance characteristics

### Requirement: Remove overly broad constraints
The system SHALL remove constraints that are too vague to enable useful classification.

#### Scenario: Remove secure constraint
- **WHEN** evaluating the `secure` constraint
- **THEN** it SHALL be removed because "secure" is too broad and cannot be objectively verified as a whole

#### Scenario: Specific security properties belong in Concept
- **WHEN** code demonstrates specific security patterns
- **THEN** it SHALL use Concept tags (security, authentication, encryption) rather than a broad Constraint tag

### Requirement: Add state management constraints
The system SHALL provide constraints for state management patterns.

#### Scenario: Stateless constraint
- **WHEN** code has the `stateless` constraint
- **THEN** judgment criteria SHALL verify: no global variables, no persistent state between function calls
- **AND** detection method SHALL be static analysis of variable scope

#### Scenario: Immutable constraint
- **WHEN** code has the `immutable` constraint
- **THEN** judgment criteria SHALL verify: no mutation operations, uses immutable data structures
- **AND** detection method SHALL be static analysis of assignment/mutation operations

### Requirement: Add concurrency model constraints
The system SHALL provide constraints for concurrency patterns.

#### Scenario: Lock-free constraint
- **WHEN** code has the `lock-free` constraint
- **THEN** judgment criteria SHALL verify: no mutex, lock, or semaphore primitives used
- **AND** detection method SHALL be static analysis for synchronization primitives

#### Scenario: Async constraint
- **WHEN** code has the `async` constraint
- **THEN** judgment criteria SHALL verify: uses async/await, Promises, coroutines, or async frameworks
- **AND** detection method SHALL be static analysis for async keywords and patterns

#### Scenario: Async constraint vs async-await concept distinction
- **WHEN** comparing `async` (Constraint) to `async-await` (Concept)
- **THEN** `async` SHALL mean "code IS asynchronous" (property)
- **AND** `async-await` SHALL mean "code DEMONSTRATES async/await pattern" (knowledge domain)

### Requirement: Add observability constraint
The system SHALL provide a constraint for observable systems.

#### Scenario: Observable constraint
- **WHEN** code has the `observable` constraint
- **THEN** judgment criteria SHALL verify: uses logging frameworks, implements metrics/monitoring, has distributed tracing, or uses structured logging with correlation IDs
- **AND** detection method SHALL be static analysis for logging, metrics, and tracing libraries

#### Scenario: Observable as alias for instrumented
- **WHEN** searching for observable code
- **THEN** both `observable` and `instrumented` SHALL identify the same constraint

### Requirement: Maintain coarse granularity
The system SHALL keep constraint tags at a coarse level of abstraction.

#### Scenario: Single performance tag not multiple dimensions
- **WHEN** representing performance optimization
- **THEN** system SHALL use one `performance-optimized` tag, not separate tags for time/space/latency

#### Scenario: Single observability tag not multiple aspects
- **WHEN** representing observability
- **THEN** system SHALL use one `observable` tag, not separate tags for logging/metrics/tracing

#### Scenario: Preserve domain-specific fine-grained constraints
- **WHEN** a constraint is highly specific to a domain
- **THEN** it MAY remain fine-grained (e.g., `gas-optimized` for Solidity, `misra-c-compliant` for embedded)

### Requirement: Ensure orthogonality with other dimensions
The system SHALL maintain clear boundaries between Constraint and other taxonomy dimensions.

#### Scenario: Constraint vs Concept distinction
- **WHEN** comparing Constraint to Concept tags
- **THEN** Constraint SHALL represent properties/requirements of code
- **AND** Concept SHALL represent knowledge domains or patterns

#### Scenario: Constraint vs Agentic distinction
- **WHEN** comparing Constraint to Agentic tags
- **THEN** Constraint SHALL represent quality attributes
- **AND** Agentic SHALL represent agent capabilities or tools

#### Scenario: Constraint vs Task distinction
- **WHEN** comparing Constraint to Task tags
- **THEN** Constraint SHALL represent non-functional requirements
- **AND** Task SHALL represent work types or objectives

### Requirement: Document judgment criteria for all constraints
The system SHALL maintain explicit judgment rules for every constraint tag.

#### Scenario: Judgment criteria in tag metadata
- **WHEN** defining a constraint tag
- **THEN** it SHALL include judgment criteria explaining how to determine if code has this property

#### Scenario: Detection method specification
- **WHEN** documenting judgment criteria
- **THEN** it SHALL specify detection method: static analysis, dynamic testing, tool measurement, or checklist validation

#### Scenario: Examples of positive and negative cases
- **WHEN** documenting a constraint
- **THEN** it SHOULD include examples of code that does and does not satisfy the constraint

### Requirement: Validate constraint objectivity
The system SHALL enforce objectivity requirements during validation.

#### Scenario: Reject constraints without judgment criteria
- **WHEN** validating taxonomy
- **THEN** constraints without explicit judgment criteria SHALL fail validation

#### Scenario: Flag potentially subjective constraints
- **WHEN** validating taxonomy
- **THEN** system SHOULD warn about constraints that may be subjective (e.g., using words like "clean", "elegant", "simple")

### Requirement: Maintain approximately 25 constraint tags
The system SHALL keep total constraint count around 25 tags, prioritizing quality over quantity.

#### Scenario: Net change from optimization
- **WHEN** applying constraint optimization
- **THEN** tag count SHALL change from 25 to approximately 23-25 tags
- **AND** reduction SHALL come from removing subjective and redundant tags
- **AND** additions SHALL only include high-value objective constraints
