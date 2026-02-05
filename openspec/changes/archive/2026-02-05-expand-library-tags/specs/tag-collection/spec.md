## MODIFIED Requirements

### Requirement: Collect tags from library and framework sources
The system SHALL collect library/framework tags from curated lists, documentation, and multiple data sources with weighted prioritization.

#### Scenario: Collect from awesome-lists
- **WHEN** collecting Library tags
- **THEN** system SHALL extract libraries from awesome-python, awesome-javascript, etc.

#### Scenario: Collect from package registries
- **WHEN** collecting Library tags
- **THEN** system SHALL extract top libraries by download count from PyPI, npm, crates.io

#### Scenario: Collect from Stack Overflow tags
- **WHEN** collecting Library tags
- **THEN** system SHALL extract libraries from Stack Overflow tags with weight 0.4

#### Scenario: Collect from GitHub Topics
- **WHEN** collecting Library tags
- **THEN** system SHALL extract libraries from GitHub Topics with weight 0.2

#### Scenario: Collect from academic papers
- **WHEN** collecting Library tags
- **THEN** system SHALL extract emerging libraries from academic paper keywords with weight 0.1

#### Scenario: Organize by subcategory
- **WHEN** collecting Library tags
- **THEN** system SHALL assign each library to appropriate subcategory (Web, Data, Infrastructure, Testing, Database)

#### Scenario: Classify granularity level
- **WHEN** collecting Library tags
- **THEN** system SHALL classify each tag as library-level, module-level, or component-level

#### Scenario: Apply weighted prioritization
- **WHEN** tag appears in multiple sources
- **THEN** system SHALL calculate weighted score and prioritize accordingly

## ADDED Requirements

### Requirement: Support granularity classification during collection
The system SHALL classify each Library tag by granularity level during collection.

#### Scenario: Library-level classification
- **WHEN** collecting a tag representing entire framework
- **THEN** system SHALL classify as library-level

#### Scenario: Module-level classification
- **WHEN** collecting a tag representing major subsystem
- **THEN** system SHALL classify as module-level

#### Scenario: Component-level classification
- **WHEN** collecting a tag representing specific feature
- **THEN** system SHALL classify as component-level

### Requirement: Record source-specific metrics
The system SHALL record source-specific metrics for each collected tag.

#### Scenario: Stack Overflow metrics
- **WHEN** collecting from Stack Overflow
- **THEN** system SHALL record question count and tag usage frequency

#### Scenario: Package registry metrics
- **WHEN** collecting from npm/PyPI
- **THEN** system SHALL record download counts and release frequency

#### Scenario: GitHub metrics
- **WHEN** collecting from GitHub Topics
- **THEN** system SHALL record repository count and star count
