## ADDED Requirements

### Requirement: Library to Domain mapping table
The system SHALL maintain a mapping table from Library tag IDs to Domain tag IDs.

#### Scenario: Generate mapping via LLM
- **WHEN** all 339 Library tags and 57 Domain tags are provided
- **THEN** the LLM SHALL assign one or more Domain tag IDs to each Library tag, producing a many-to-many mapping

#### Scenario: Store mapping table
- **WHEN** the mapping is generated
- **THEN** the system SHALL store it in `annotation/mappings/library_to_domain.json` as a dict of library_id → list[domain_id]

#### Scenario: Mapping covers all libraries
- **WHEN** the mapping table is validated
- **THEN** every Library tag ID SHALL have at least one Domain mapping (use a "general" or "unclassified" fallback if needed)

#### Scenario: Mapping uses only valid Domain IDs
- **WHEN** the mapping table is validated
- **THEN** every Domain ID in the mapping SHALL exist in the Domain taxonomy YAML

### Requirement: Concept candidate reduction mapping
The system SHALL maintain a mapping from (Language, Domain) pairs to a reduced set of candidate Concept tag IDs.

#### Scenario: Generate candidate mapping via LLM
- **WHEN** common (Language, Domain) pairs are identified (e.g., (python, machine-learning), (javascript, web-frontend), (rust, systems-programming))
- **THEN** the LLM SHALL produce a candidate Concept set (typically 15-30 IDs) for each pair, covering concepts likely to appear in that context

#### Scenario: Cover frequent combinations
- **WHEN** the candidate mapping is generated
- **THEN** it SHALL cover at least 200 (Language, Domain) combinations representing the most common pairings

#### Scenario: Store candidate mapping
- **WHEN** the mapping is generated
- **THEN** the system SHALL store it in `annotation/mappings/concept_candidates.json` as a dict of "language_id:domain_id" → list[concept_id]

#### Scenario: Fallback for unmapped combinations
- **WHEN** a (Language, Domain) pair is not found in the mapping
- **THEN** the system SHALL fall back to the union of all Concept candidates for that Language (any domain) and that Domain (any language)

### Requirement: Domain inference from Library combinations
The system SHALL infer Domain tags from combinations of matched Library tags when direct Domain detection is insufficient.

#### Scenario: Single library maps to domains
- **WHEN** a record has matched Library tags
- **THEN** the system SHALL lookup each library's domains from the Library→Domain mapping and return the union

#### Scenario: Library combination reinforces domain confidence
- **WHEN** multiple matched Library tags map to the same Domain
- **THEN** that Domain SHALL receive a higher confidence score than a Domain mapped by only one library
