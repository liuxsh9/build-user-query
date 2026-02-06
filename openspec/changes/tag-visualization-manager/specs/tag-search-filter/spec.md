## ADDED Requirements

### Requirement: Fuzzy text search
The system SHALL provide fuzzy search across tag fields with typo tolerance.

#### Scenario: Search by tag name
- **WHEN** user enters "async" in search box
- **THEN** system displays tags with names containing or similar to "async" (e.g., "Async/Await", "asynchronous")

#### Scenario: Search by ID
- **WHEN** user enters "async-await" in search box
- **THEN** system displays tags with matching or similar IDs

#### Scenario: Search by alias
- **WHEN** user enters "fp" in search box
- **THEN** system displays "Functional Programming" tag which has "fp" as an alias

#### Scenario: Search with typo tolerance
- **WHEN** user enters "asynch" (misspelled) in search box
- **THEN** system still displays "Async/Await" tag due to fuzzy matching

#### Scenario: Weighted search results
- **WHEN** multiple tags match search query
- **THEN** system ranks results with name matches higher than description matches

#### Scenario: Clear search
- **WHEN** user clears the search box
- **THEN** system displays all tags for the selected category

### Requirement: Filter by category
The system SHALL allow users to filter tags by selecting a category from the navigation.

#### Scenario: Select category from sidebar
- **WHEN** user clicks "Concept" in category navigation
- **THEN** system displays only tags with category "Concept"

#### Scenario: Display category counts
- **WHEN** user views category navigation
- **THEN** system shows tag count next to each category name (e.g., "Concept (93)")

#### Scenario: Highlight selected category
- **WHEN** user has selected a category
- **THEN** system visually highlights the selected category in navigation

### Requirement: Filter by difficulty
The system SHALL allow users to filter tags by difficulty level for categories that have difficulty.

#### Scenario: Filter by basic difficulty
- **WHEN** user selects "Basic" difficulty filter while viewing Concept category
- **THEN** system displays only Concept tags with difficulty "basic"

#### Scenario: Difficulty filter on non-Concept category
- **WHEN** user views a category without difficulty field (e.g., Language)
- **THEN** system hides or disables the difficulty filter

#### Scenario: Clear difficulty filter
- **WHEN** user selects "All Difficulties" option
- **THEN** system displays all tags regardless of difficulty

### Requirement: Filter by language scope
The system SHALL allow users to filter tags by language scope.

#### Scenario: Filter by specific language
- **WHEN** user selects "Rust" language filter
- **THEN** system displays only tags with "rust" in their language_scope array

#### Scenario: Show tags without language scope
- **WHEN** user views tags and no language filter is applied
- **THEN** system displays tags both with and without language_scope field

#### Scenario: Language filter on Library category
- **WHEN** user selects "JavaScript" filter while viewing Library category
- **THEN** system displays only JavaScript libraries

### Requirement: Combine filters
The system SHALL allow users to apply multiple filters simultaneously.

#### Scenario: Search with category and difficulty
- **WHEN** user searches for "array" with "Basic" difficulty filter in Concept category
- **THEN** system displays only basic Concept tags matching "array"

#### Scenario: Search with language filter
- **WHEN** user searches for "async" with "Rust" language filter
- **THEN** system displays only Rust-specific tags matching "async"

#### Scenario: Display filter count
- **WHEN** user applies filters
- **THEN** system shows "Showing X of Y tags" indicating filtered count

### Requirement: Sort results
The system SHALL allow users to sort displayed tags by different criteria.

#### Scenario: Sort by name alphabetically
- **WHEN** user selects "Name" sort option
- **THEN** system sorts tags alphabetically by name field

#### Scenario: Sort by difficulty
- **WHEN** user selects "Difficulty" sort option on Concept category
- **THEN** system sorts tags with basic first, intermediate second, advanced last

#### Scenario: Sort by ID
- **WHEN** user selects "ID" sort option
- **THEN** system sorts tags alphabetically by ID field
