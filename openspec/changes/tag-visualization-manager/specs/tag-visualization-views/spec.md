## ADDED Requirements

### Requirement: Adaptive view selection
The system SHALL automatically choose between grid and table views based on the number of tags in the selected category.

#### Scenario: Display grid view for small category
- **WHEN** user selects a category with fewer than 100 tags (e.g., Concept with 93 tags)
- **THEN** system displays tags in grid view with visual cards

#### Scenario: Display table view for large category
- **WHEN** user selects a category with 100 or more tags (e.g., Library with 339 tags)
- **THEN** system displays tags in table view with virtual scrolling

#### Scenario: Switch views when changing category
- **WHEN** user switches from Concept (93 tags) to Library (339 tags)
- **THEN** system automatically changes from grid view to table view

### Requirement: Grid view display
The system SHALL display tags as cards in a responsive grid layout.

#### Scenario: Display tag card with essential info
- **WHEN** user views a tag in grid mode
- **THEN** system displays card showing tag name, category badge, difficulty badge (if applicable), and first alias

#### Scenario: Grid responsive layout
- **WHEN** user resizes browser window
- **THEN** system adjusts number of columns to fit available space (e.g., 4 columns on desktop, 2 on tablet, 1 on mobile)

#### Scenario: Grid card hover interaction
- **WHEN** user hovers over a tag card
- **THEN** system displays edit and delete action buttons

#### Scenario: Color-code by difficulty
- **WHEN** user views Concept tags in grid mode
- **THEN** system shows difficulty badge with color coding (green for basic, amber for intermediate, red for advanced)

### Requirement: Table view display
The system SHALL display tags in a sortable table with columns for key attributes.

#### Scenario: Display table columns
- **WHEN** user views tags in table mode
- **THEN** system displays columns for Name, Subcategory, Language Scope, and Difficulty (if applicable)

#### Scenario: Click table row to edit
- **WHEN** user clicks a table row
- **THEN** system opens the tag editor modal for that tag

#### Scenario: Sort table by column
- **WHEN** user clicks a column header
- **THEN** system sorts table rows by that column in ascending order, clicking again sorts descending

#### Scenario: Show row actions
- **WHEN** user hovers over or focuses on a table row
- **THEN** system displays edit and delete icons in an actions column

### Requirement: Virtual scrolling for large lists
The system SHALL implement virtual scrolling for table view to handle hundreds of tags efficiently.

#### Scenario: Render only visible rows
- **WHEN** user views Library category (339 tags) in table mode
- **THEN** system renders only rows visible in viewport plus buffer, not all 339 rows

#### Scenario: Smooth scrolling performance
- **WHEN** user scrolls through large table
- **THEN** system maintains 60fps scroll performance by dynamically rendering rows

#### Scenario: Update visible rows on scroll
- **WHEN** user scrolls down in table view
- **THEN** system removes off-screen rows from DOM and renders newly visible rows

### Requirement: Group tags by subcategory
The system SHALL visually group tags by their subcategory within the selected category.

#### Scenario: Display subcategory headers in grid
- **WHEN** user views Concept category in grid mode
- **THEN** system shows section headers for "Fundamentals", "Advanced", and "Engineering" with tag counts

#### Scenario: Collapsible subcategory sections
- **WHEN** user clicks a subcategory header
- **THEN** system collapses or expands that subcategory's tags

#### Scenario: Show tag count per subcategory
- **WHEN** user views subcategory headers
- **THEN** system displays number of tags in each subcategory (e.g., "Fundamentals (28)")

### Requirement: Empty state display
The system SHALL show helpful messages when no tags match current filters.

#### Scenario: No search results
- **WHEN** user's search query returns no matches
- **THEN** system displays "No tags found matching '{query}'" with option to clear search

#### Scenario: No tags in filtered category
- **WHEN** user applies filters that result in zero tags
- **THEN** system displays message indicating no tags match the current filters with option to reset filters
