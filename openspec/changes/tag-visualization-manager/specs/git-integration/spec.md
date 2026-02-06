## ADDED Requirements

### Requirement: Display git status
The system SHALL show the current git status of taxonomy/tags directory.

#### Scenario: Show uncommitted changes
- **WHEN** user views the git status widget
- **THEN** system displays list of modified, added, or deleted files in taxonomy/tags/

#### Scenario: Show clean working tree
- **WHEN** no changes exist in taxonomy/tags directory
- **THEN** system displays "No uncommitted changes" message with green checkmark

#### Scenario: Highlight file status
- **WHEN** git status shows changes
- **THEN** system color-codes files by status (modified: yellow, added: green, deleted: red)

#### Scenario: Update status after tag edit
- **WHEN** user creates, updates, or deletes a tag
- **THEN** system refreshes git status display automatically to show new changes

### Requirement: Manual commit workflow
The system SHALL allow users to commit changes with a custom message through the UI.

#### Scenario: Open commit dialog
- **WHEN** user clicks "Commit" button while uncommitted changes exist
- **THEN** system displays commit dialog with message input field and file list preview

#### Scenario: Enter commit message
- **WHEN** user types in commit message field
- **THEN** system validates message is not empty and enables commit button

#### Scenario: Execute commit
- **WHEN** user submits commit with valid message
- **THEN** system executes "git add taxonomy/tags/" followed by "git commit -m '{message}'"

#### Scenario: Show commit success
- **WHEN** commit completes successfully
- **THEN** system displays success notification, clears git status, and updates recent commits list

#### Scenario: Handle commit failure
- **WHEN** git commit fails (e.g., no changes staged, merge conflict)
- **THEN** system displays error message with git output and does not clear git status

#### Scenario: Disable commit when no changes
- **WHEN** no uncommitted changes exist
- **THEN** system disables or hides the commit button

### Requirement: Display recent commits
The system SHALL show recent commit history for taxonomy/tags files.

#### Scenario: List recent commits
- **WHEN** user views git integration panel
- **THEN** system displays last 10 commits affecting taxonomy/tags/ with hash and message

#### Scenario: Show commit metadata
- **WHEN** user views commit list
- **THEN** each commit shows short hash (7 chars), commit message, and relative time

#### Scenario: Refresh commits after new commit
- **WHEN** user makes a new commit
- **THEN** system adds the new commit to top of recent commits list

### Requirement: Git status refresh
The system SHALL provide mechanisms to refresh git status.

#### Scenario: Auto-refresh after CRUD operation
- **WHEN** user creates, updates, or deletes a tag
- **THEN** system automatically refreshes git status within 1 second

#### Scenario: Manual refresh
- **WHEN** user clicks refresh button on git status widget
- **THEN** system queries current git status and updates display

#### Scenario: Refresh on page load
- **WHEN** application loads
- **THEN** system queries and displays current git status

### Requirement: Git error handling
The system SHALL handle git command failures gracefully.

#### Scenario: Git not installed
- **WHEN** git command is not available on system
- **THEN** system displays "Git not found" message and disables git integration features

#### Scenario: Not a git repository
- **WHEN** project is not initialized as a git repository
- **THEN** system displays "Not a git repository" message and suggests running "git init"

#### Scenario: Permission issues
- **WHEN** system lacks permissions to run git commands
- **THEN** system displays permission error and suggests checking file permissions

### Requirement: Commit message validation
The system SHALL validate commit messages before allowing commit.

#### Scenario: Require non-empty message
- **WHEN** user attempts to commit with empty message
- **THEN** system displays error "Commit message is required" and prevents commit

#### Scenario: Trim whitespace
- **WHEN** user enters commit message with leading/trailing whitespace
- **THEN** system trims whitespace before executing commit

#### Scenario: Escape special characters
- **WHEN** commit message contains quotes or special shell characters
- **THEN** system properly escapes message to prevent command injection

### Requirement: Visual indicator for unsaved work
The system SHALL alert users when uncommitted changes exist.

#### Scenario: Show notification badge
- **WHEN** uncommitted changes exist
- **THEN** system displays badge with change count on git status widget

#### Scenario: Warning on page unload
- **WHEN** user attempts to close browser with uncommitted changes
- **THEN** system displays browser confirmation dialog warning about unsaved work

#### Scenario: Persistent indicator
- **WHEN** user navigates within application with uncommitted changes
- **THEN** system maintains visible indicator of uncommitted changes in navigation bar
