## ADDED Requirements

### Requirement: Support Concept-specific collection sources
The system SHALL support collecting Concept tags from educational and documentation sources.

#### Scenario: Educational platform collection
- **WHEN** collecting Concept tags
- **THEN** system SHALL support sources like MDN, W3Schools, freeCodeCamp

#### Scenario: Documentation-based collection
- **WHEN** collecting from language documentation
- **THEN** system SHALL extract concept keywords from official docs

#### Scenario: Academic curricula collection
- **WHEN** collecting from CS curricula
- **THEN** system SHALL identify core concepts taught in programming courses

### Requirement: Classify concepts by subcategory during collection
The system SHALL automatically suggest subcategory (Fundamentals, Advanced, Engineering) during collection.

#### Scenario: Foundational concept detection
- **WHEN** collecting basic programming concepts
- **THEN** system SHALL suggest Fundamentals subcategory

#### Scenario: Advanced concept detection
- **WHEN** collecting complex programming concepts
- **THEN** system SHALL suggest Advanced subcategory

#### Scenario: Engineering practice detection
- **WHEN** collecting software engineering practices
- **THEN** system SHALL suggest Engineering subcategory
