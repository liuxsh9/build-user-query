## MODIFIED Requirements

### Requirement: Validate tag granularity
The system SHALL ensure Library tags conform to three-tier granularity system (library, module, component).

#### Scenario: Validate library-level tags
- **WHEN** validating a library-level tag
- **THEN** system SHALL verify it represents entire framework used as a whole

#### Scenario: Validate module-level tags
- **WHEN** validating a module-level tag
- **THEN** system SHALL verify it represents major subsystem with distinct capabilities

#### Scenario: Validate component-level tags
- **WHEN** validating a component-level tag
- **THEN** system SHALL verify it represents specific feature used independently

#### Scenario: Flag incorrect granularity
- **WHEN** tag granularity doesn't match guidelines
- **THEN** system SHALL flag for review and suggest correct level

### Requirement: Enrich tag metadata
The system SHALL add missing metadata fields to collected tags, including automated alias expansion.

#### Scenario: Add language scope to concepts
- **WHEN** a Concept tag is language-specific
- **THEN** system SHALL populate language_scope field

#### Scenario: Generate descriptions
- **WHEN** a tag lacks description
- **THEN** system SHALL use LLM to generate concise description for human review

#### Scenario: Identify related tags
- **WHEN** processing tags
- **THEN** system SHALL suggest related_tags based on co-occurrence in sources

#### Scenario: Expand aliases automatically
- **WHEN** processing Library tags
- **THEN** system SHALL run automated alias expansion tool to generate candidate aliases

#### Scenario: Validate expanded aliases
- **WHEN** aliases are auto-generated
- **THEN** system SHALL apply confidence scoring and human validation workflow

## ADDED Requirements

### Requirement: Validate granularity metadata field
The system SHALL validate that all Library tags include granularity metadata.

#### Scenario: Granularity field presence
- **WHEN** normalizing Library tags
- **THEN** system SHALL verify each tag has granularity field

#### Scenario: Granularity enum validation
- **WHEN** validating granularity field
- **THEN** system SHALL verify value is one of: library, module, component

### Requirement: Apply alias expansion during normalization
The system SHALL integrate automated alias expansion into normalization workflow.

#### Scenario: Trigger alias expansion
- **WHEN** normalizing Library tags
- **THEN** system SHALL automatically run alias expansion tool

#### Scenario: Merge expanded aliases
- **WHEN** alias expansion completes
- **THEN** system SHALL merge high-confidence aliases into tag definition

#### Scenario: Flag medium-confidence aliases
- **WHEN** alias expansion produces medium-confidence results
- **THEN** system SHALL flag for human review before merging

### Requirement: Preserve source-specific metrics
The system SHALL preserve source-specific metrics during normalization.

#### Scenario: Retain collection metrics
- **WHEN** normalizing tags from multiple sources
- **THEN** system SHALL preserve all source-specific metrics in metadata

#### Scenario: Calculate aggregate scores
- **WHEN** tag appears in multiple sources
- **THEN** system SHALL calculate and store aggregate weighted score
