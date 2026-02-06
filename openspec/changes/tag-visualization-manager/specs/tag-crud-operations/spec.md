## ADDED Requirements

### Requirement: Create new tag
The system SHALL allow users to create a new tag with all required fields for the specified category.

#### Scenario: Successfully create a tag
- **WHEN** user fills in all required fields (id, name, category, source) and submits the create form
- **THEN** system validates the tag, writes it to the appropriate YAML file, and displays the new tag in the list

#### Scenario: Create tag with duplicate ID
- **WHEN** user attempts to create a tag with an ID that already exists
- **THEN** system displays an error message "Tag with ID {id} already exists in {category}" and prevents creation

#### Scenario: Create tag with invalid fields
- **WHEN** user submits a tag with validation errors (e.g., missing required fields, invalid ID format)
- **THEN** system displays specific validation errors and prevents creation

### Requirement: Read and display tags
The system SHALL load and display all tags from YAML files, grouped by category.

#### Scenario: Load all tags on page load
- **WHEN** user opens the application
- **THEN** system reads all YAML files from taxonomy/tags/ and displays tags organized by category

#### Scenario: Refresh tags after external change
- **WHEN** user refreshes the page after YAML files have been modified externally
- **THEN** system loads the latest tag data from files

#### Scenario: Display tag with all metadata
- **WHEN** user views a tag card
- **THEN** system displays name, category, subcategory, difficulty (if applicable), language_scope (if applicable), and aliases

### Requirement: Update existing tag
The system SHALL allow users to edit any field of an existing tag while maintaining validation.

#### Scenario: Successfully update a tag
- **WHEN** user modifies tag fields and saves changes
- **THEN** system validates the updated tag, writes changes to YAML file, and displays updated tag immediately

#### Scenario: Optimistic UI update
- **WHEN** user saves tag changes
- **THEN** system immediately updates the UI with new values before server confirmation

#### Scenario: Rollback on update failure
- **WHEN** server validation fails after optimistic update
- **THEN** system reverts UI to previous tag values and displays error message

#### Scenario: Update tag ID
- **WHEN** user changes a tag's ID
- **THEN** system validates ID uniqueness and format, updates YAML file with new ID

### Requirement: Delete tag
The system SHALL allow users to delete tags with confirmation.

#### Scenario: Successfully delete a tag
- **WHEN** user confirms deletion of a tag
- **THEN** system removes the tag from YAML file and removes it from the displayed list

#### Scenario: Require deletion confirmation
- **WHEN** user clicks delete button
- **THEN** system displays a confirmation dialog with tag name before proceeding

#### Scenario: Delete tag and update UI
- **WHEN** tag is successfully deleted
- **THEN** system removes the tag from view without requiring page refresh

### Requirement: Tag editor modal
The system SHALL provide a modal interface for creating and editing tags with category-specific fields.

#### Scenario: Open editor for new tag
- **WHEN** user clicks "New Tag" button
- **THEN** system displays empty editor modal with category selector

#### Scenario: Open editor for existing tag
- **WHEN** user clicks edit button on a tag card
- **THEN** system displays editor modal pre-filled with current tag values

#### Scenario: Show category-specific fields
- **WHEN** user selects a category in the editor
- **THEN** system displays only the fields relevant to that category (e.g., difficulty for Concept, language_scope for Library)

#### Scenario: Close editor without saving
- **WHEN** user closes editor without saving
- **THEN** system discards changes and does not modify YAML files
