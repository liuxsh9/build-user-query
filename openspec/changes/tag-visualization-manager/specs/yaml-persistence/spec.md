## ADDED Requirements

### Requirement: Read YAML files
The system SHALL read and parse all YAML files from the taxonomy/tags directory on each request.

#### Scenario: Load all category files
- **WHEN** application starts or API endpoint is called
- **THEN** system reads all .yaml files from taxonomy/tags/ directory (concept.yaml, library.yaml, etc.)

#### Scenario: Parse YAML to objects
- **WHEN** system reads a YAML file
- **THEN** system parses YAML content into JavaScript objects with proper type handling

#### Scenario: Handle missing category field
- **WHEN** YAML file contains tags without explicit category field
- **THEN** system infers category from filename (e.g., "concept.yaml" → category: "Concept")

#### Scenario: Handle malformed YAML
- **WHEN** YAML file contains syntax errors
- **THEN** system logs error with file name and line number, returns error response to client

### Requirement: Write YAML files
The system SHALL write tag changes back to YAML files while preserving format and structure.

#### Scenario: Update existing tag in file
- **WHEN** system receives tag update request
- **THEN** system reads YAML file, updates the matching tag object, and writes back to file

#### Scenario: Add new tag to file
- **WHEN** system receives create tag request
- **THEN** system reads YAML file, appends new tag object, sorts by ID, and writes to file

#### Scenario: Remove tag from file
- **WHEN** system receives delete tag request
- **THEN** system reads YAML file, filters out the target tag, and writes remaining tags to file

#### Scenario: Preserve YAML formatting
- **WHEN** system writes YAML file
- **THEN** system maintains consistent indentation (2 spaces), line width unlimited, and field order

### Requirement: Maintain data integrity
The system SHALL ensure YAML files remain valid and consistent after write operations.

#### Scenario: Validate before writing
- **WHEN** system prepares to write YAML file
- **THEN** system validates all tag objects in the file against schema rules before writing

#### Scenario: Atomic file writes
- **WHEN** system writes to YAML file
- **THEN** system writes to temporary file first, then atomically renames to replace original file

#### Scenario: Sort tags by ID
- **WHEN** system writes tags to YAML file
- **THEN** system sorts tag array alphabetically by ID field for consistent ordering

#### Scenario: Preserve unmodified tags
- **WHEN** system updates one tag in a file
- **THEN** system preserves all other tags exactly as they were, including formatting and field order

### Requirement: Handle file system errors
The system SHALL gracefully handle file system errors and report them to the client.

#### Scenario: File not found
- **WHEN** system attempts to read non-existent YAML file
- **THEN** system returns empty tag array for that category and logs warning

#### Scenario: Permission denied
- **WHEN** system lacks read or write permissions for YAML files
- **THEN** system returns error response with permission details and HTTP 500 status

#### Scenario: Disk full error
- **WHEN** system attempts to write but disk is full
- **THEN** system returns error response, does not corrupt existing file, and logs error

### Requirement: Cache invalidation
The system SHALL reload YAML files on each API request to ensure fresh data.

#### Scenario: No server-side caching
- **WHEN** system receives API request for tags
- **THEN** system reads YAML files from disk, not from in-memory cache

#### Scenario: External file changes are visible
- **WHEN** user modifies YAML files externally and refreshes application
- **THEN** system displays updated tag data from modified files

### Requirement: Concurrent access handling
The system SHALL handle potential concurrent file access safely.

#### Scenario: Single writer assumption
- **WHEN** system writes to YAML file
- **THEN** system assumes it is the only writer (documented as single-user application)

#### Scenario: Detect external changes on write
- **WHEN** system writes to YAML file that was externally modified since last read
- **THEN** system completes write but logs warning about potential concurrent modification
