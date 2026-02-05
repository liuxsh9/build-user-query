## ADDED Requirements

### Requirement: Collect tags from programming language sources
The system SHALL collect programming language tags from authoritative sources.

#### Scenario: Collect from TIOBE index
- **WHEN** collecting Language tags
- **THEN** system SHALL extract top 50 languages from TIOBE index

#### Scenario: Collect from GitHub language stats
- **WHEN** collecting Language tags
- **THEN** system SHALL extract languages with >10k repositories from GitHub

#### Scenario: Deduplicate language names
- **WHEN** multiple sources provide the same language
- **THEN** system SHALL merge into single tag with aliases

### Requirement: Collect tags from library and framework sources
The system SHALL collect library/framework tags from curated lists and documentation.

#### Scenario: Collect from awesome-lists
- **WHEN** collecting Library tags
- **THEN** system SHALL extract libraries from awesome-python, awesome-javascript, etc.

#### Scenario: Collect from package registries
- **WHEN** collecting Library tags
- **THEN** system SHALL extract top libraries by download count from PyPI, npm, crates.io

#### Scenario: Organize by subcategory
- **WHEN** collecting Library tags
- **THEN** system SHALL assign each library to appropriate subcategory (Web, Data, Infrastructure, Testing, Database)

### Requirement: Collect tags from programming concept sources
The system SHALL collect programming concept tags from educational and reference materials.

#### Scenario: Collect from programming textbooks
- **WHEN** collecting Concept tags
- **THEN** system SHALL extract concepts from table of contents of standard CS textbooks

#### Scenario: Collect from interview question banks
- **WHEN** collecting Concept tags
- **THEN** system SHALL extract concepts from LeetCode, HackerRank topic taxonomies

#### Scenario: Assign difficulty levels
- **WHEN** collecting Concept tags
- **THEN** system SHALL assign difficulty (basic, intermediate, advanced) based on source context

### Requirement: Collect tags from existing benchmarks
The system SHALL extract capability tags from existing code generation benchmarks.

#### Scenario: Collect from HumanEval
- **WHEN** collecting tags from HumanEval
- **THEN** system SHALL extract concepts, tasks, and language tags from problem descriptions

#### Scenario: Collect from SWE-bench
- **WHEN** collecting tags from SWE-bench
- **THEN** system SHALL extract libraries, domains, and agentic capabilities from issues

### Requirement: Support LLM-assisted extraction
The system SHALL use LLM to assist in tag extraction from unstructured sources.

#### Scenario: LLM extracts tags from documentation
- **WHEN** processing library documentation
- **THEN** system SHALL use LLM to identify relevant tags and suggest metadata

#### Scenario: LLM suggests subcategory assignment
- **WHEN** collecting Library or Concept tags
- **THEN** system SHALL use LLM to suggest appropriate subcategory

#### Scenario: Human validation required
- **WHEN** LLM extracts tags
- **THEN** system SHALL mark them as requiring human validation before inclusion

### Requirement: Track tag provenance
The system SHALL record the source of each collected tag.

#### Scenario: Tag includes source metadata
- **WHEN** a tag is collected
- **THEN** it MUST include source field indicating origin (e.g., "TIOBE", "awesome-python", "HumanEval")

#### Scenario: Multiple sources increase confidence
- **WHEN** a tag appears in multiple sources
- **THEN** system SHALL record all sources in metadata
