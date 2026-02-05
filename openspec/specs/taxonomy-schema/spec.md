# taxonomy-schema Specification

## Purpose
TBD - created by archiving change build-capability-taxonomy. Update Purpose after archive.
## Requirements
### Requirement: Define category structure
The system SHALL define 8 orthogonal categories: Language, Library, Domain, Concept, Task, Constraint, Agentic, and Context.

#### Scenario: Category definition includes metadata
- **WHEN** taxonomy.yaml is loaded
- **THEN** each category MUST have name, description, and hierarchical flag

#### Scenario: Hierarchical categories support subcategories
- **WHEN** a category has hierarchical=true
- **THEN** it MUST define a subcategories list with name and description

### Requirement: Define tag structure
The system SHALL define a tag schema with required and optional fields.

#### Scenario: Tag has required fields
- **WHEN** a tag is defined
- **THEN** it MUST have id, name, and category fields

#### Scenario: Tag supports optional metadata
- **WHEN** a tag is defined
- **THEN** it MAY have description, aliases, language_scope, difficulty, examples, and related_tags fields

#### Scenario: Tag ID is unique across taxonomy
- **WHEN** multiple tags are defined
- **THEN** no two tags SHALL have the same id

### Requirement: Support mixed hierarchy
The system SHALL support both flat and two-level hierarchical categories.

#### Scenario: Library category uses subcategories
- **WHEN** Library category is defined
- **THEN** it MUST have hierarchical=true and subcategories including Web, Data, Infrastructure, Testing, Database

#### Scenario: Concept category uses subcategories
- **WHEN** Concept category is defined
- **THEN** it MUST have hierarchical=true and subcategories including Fundamentals, Advanced, Engineering

#### Scenario: Other categories are flat
- **WHEN** Language, Domain, Task, Constraint, Agentic, or Context categories are defined
- **THEN** they MUST have hierarchical=false

### Requirement: Define labeling result structure
The system SHALL define a structure for storing capability labels on data items.

#### Scenario: Labeled item has all category fields
- **WHEN** a data item is labeled
- **THEN** it MUST have a labels object with keys for all 8 categories

#### Scenario: Each category can have multiple tags
- **WHEN** a category is labeled
- **THEN** it SHALL contain an array of tag IDs (may be empty)

#### Scenario: Labeled item includes metadata
- **WHEN** a data item is labeled
- **THEN** it MUST include source, labeled_by, and labeled_at metadata

