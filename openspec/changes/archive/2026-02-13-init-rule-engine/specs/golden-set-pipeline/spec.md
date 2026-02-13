## ADDED Requirements

### Requirement: Per-category LLM annotation for golden set records
The system SHALL annotate golden set records by splitting annotation into independent per-category LLM calls.

#### Scenario: Annotate Language category
- **WHEN** a golden set record is submitted for Language annotation
- **THEN** the LLM SHALL be prompted with the full conversation content and the list of 75 Language tag IDs/names, returning all applicable Language tags

#### Scenario: Annotate Library category with subcategory splitting
- **WHEN** a golden set record is submitted for Library annotation
- **THEN** the system SHALL split the 339 Library tags by subcategory (Web, Data, Testing, Infrastructure, Database) and make separate LLM calls per subcategory, merging results

#### Scenario: Annotate Concept category with subcategory splitting
- **WHEN** a golden set record is submitted for Concept annotation
- **THEN** the system SHALL split the 106 Concept tags by subcategory (Fundamentals, Advanced, Engineering) and make separate LLM calls per subcategory, merging results

#### Scenario: Annotate small categories in single calls
- **WHEN** a golden set record is submitted for Task (21), Constraint (24), Agentic (40), Domain (57), or Context (10) annotation
- **THEN** each category SHALL be annotated in a single LLM call with all tags listed

#### Scenario: Context annotation returns exactly one tag
- **WHEN** the Context category is annotated
- **THEN** the LLM SHALL return exactly one Context tag ID (single-select)

### Requirement: Multi-model verification for golden set
The system SHALL use multiple LLM models to verify golden set annotations.

#### Scenario: Dual-model annotation
- **WHEN** a golden set record is annotated
- **THEN** the system SHALL run the full per-category annotation pipeline with two different LLM models independently

#### Scenario: Agreement produces final label
- **WHEN** two models agree on a tag (both include or both exclude it)
- **THEN** that agreement SHALL be the final label for that tag

#### Scenario: Disagreement triggers arbitration
- **WHEN** two models disagree on a tag (one includes, one excludes)
- **THEN** a third LLM model SHALL be prompted with the record, the specific tag in question, and both models' reasoning, producing a final decision

### Requirement: Golden set sampling strategy
The system SHALL sample records for the golden set to ensure coverage across files and data types.

#### Scenario: Proportional sampling from each file
- **WHEN** the golden set is constructed from ~50 source files
- **THEN** the system SHALL sample at least 15-20 records from each file, producing ~750-1000 total records

#### Scenario: Diversity within file samples
- **WHEN** records are sampled from a file
- **THEN** the system SHALL select records with maximum diversity (e.g., different conversation lengths, different tool usage patterns) rather than random sampling

### Requirement: Golden set output format
The system SHALL store golden set results in a structured, reusable format.

#### Scenario: Store golden set as JSONL
- **WHEN** golden set annotation is complete
- **THEN** the system SHALL store results in `annotation/golden_set/golden_set.jsonl` where each line contains record_id, source_file, labels (8-category object), and annotation_metadata (models used, agreement scores, arbitration details)

#### Scenario: Generate quality report
- **WHEN** golden set annotation is complete
- **THEN** the system SHALL produce a quality report showing inter-model agreement rate per category, number of arbitrations, and tag distribution statistics
