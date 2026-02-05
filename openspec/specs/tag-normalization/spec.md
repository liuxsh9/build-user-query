# tag-normalization Specification

## Purpose
TBD - created by archiving change build-capability-taxonomy. Update Purpose after archive.
## Requirements
### Requirement: Deduplicate tags across sources
The system SHALL identify and merge duplicate tags from different sources.

#### Scenario: Exact name match
- **WHEN** two tags have identical names
- **THEN** system SHALL merge them into single tag with combined metadata

#### Scenario: Alias match
- **WHEN** a tag name matches another tag's alias
- **THEN** system SHALL merge them and preserve all aliases

#### Scenario: Case-insensitive matching
- **WHEN** comparing tag names
- **THEN** system SHALL use case-insensitive comparison (e.g., "Python" == "python")

### Requirement: Normalize tag identifiers
The system SHALL convert tag names to standardized kebab-case identifiers.

#### Scenario: Convert to kebab-case
- **WHEN** creating tag ID from name
- **THEN** system SHALL convert to lowercase and replace spaces/special chars with hyphens

#### Scenario: Handle version numbers
- **WHEN** tag name includes version (e.g., "Python 3")
- **THEN** system SHALL strip version from ID but preserve in name/aliases

#### Scenario: Preserve original name
- **WHEN** normalizing tag ID
- **THEN** system SHALL keep original name in the name field

### Requirement: Resolve alias conflicts
The system SHALL detect and resolve conflicting aliases across tags.

#### Scenario: Alias collision detected
- **WHEN** two different tags claim the same alias
- **THEN** system SHALL flag conflict for human resolution

#### Scenario: Prefer canonical names
- **WHEN** resolving alias conflicts
- **THEN** system SHALL suggest keeping alias with more authoritative source

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

### Requirement: Assign tags to categories
The system SHALL correctly categorize each normalized tag.

#### Scenario: Assign to primary category
- **WHEN** normalizing a tag
- **THEN** system SHALL assign it to exactly one category

#### Scenario: Assign subcategory for hierarchical categories
- **WHEN** tag belongs to Library or Concept category
- **THEN** system SHALL assign appropriate subcategory

#### Scenario: Validate category assignment
- **WHEN** assigning category
- **THEN** system SHALL verify tag fits category definition and doesn't overlap with other categories

### Requirement: Output normalized tags in YAML format
The system SHALL write normalized tags to category-specific YAML files.

#### Scenario: One file per category
- **WHEN** outputting normalized tags
- **THEN** system SHALL create tags/<category>.yaml for each category

#### Scenario: Preserve metadata structure
- **WHEN** writing YAML
- **THEN** system SHALL include all tag fields defined in schema

#### Scenario: Sort tags alphabetically
- **WHEN** writing YAML
- **THEN** system SHALL sort tags by ID for readability

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

