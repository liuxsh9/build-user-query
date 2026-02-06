# agentic-search-capabilities Specification

## Purpose
Define search capabilities for agentic systems, distinguishing between file metadata search (paths, names) and content search (code, text). Enables agents to discover files and code patterns across codebases.

## Requirements

### Requirement: Define file-search capability
The system SHALL provide file-search capability for discovering files by metadata.

#### Scenario: File path pattern matching
- **WHEN** agent needs to find files by path pattern
- **THEN** it SHALL use file-search with glob patterns (e.g., "**/*.ts", "src/**/*.test.js")

#### Scenario: File name search
- **WHEN** agent needs to find files by name
- **THEN** it SHALL use file-search with name patterns (e.g., "*.config.js", "Dockerfile")

#### Scenario: File extension filtering
- **WHEN** agent needs to find all files of specific type
- **THEN** it SHALL use file-search with extension patterns (e.g., "*.py", "*.md")

#### Scenario: Recursive directory search
- **WHEN** agent needs to search nested directories
- **THEN** it SHALL support recursive glob patterns (e.g., "**/test/**/*.js")

#### Scenario: File-search output format
- **WHEN** file-search completes
- **THEN** it SHALL return list of matching file paths sorted by relevance/modification time

### Requirement: Define code-search capability
The system SHALL provide code-search capability for discovering content within files.

#### Scenario: Regex pattern matching
- **WHEN** agent needs to find code matching regex
- **THEN** it SHALL use code-search with regex patterns (e.g., "function\\s+\\w+", "class\\s+\\w+")

#### Scenario: Literal string search
- **WHEN** agent needs to find exact code strings
- **THEN** it SHALL use code-search with literal strings (e.g., "import React", "TODO:")

#### Scenario: Context around matches
- **WHEN** code-search finds matches
- **THEN** it SHALL return surrounding context (e.g., N lines before/after)

#### Scenario: File type filtering
- **WHEN** code-search should only search specific file types
- **THEN** it SHALL support file type filters (e.g., --type js, --glob "*.py")

#### Scenario: Case sensitivity
- **WHEN** code-search is invoked
- **THEN** it SHALL support case-sensitive and case-insensitive modes

#### Scenario: Code-search output format
- **WHEN** code-search completes
- **THEN** it SHALL return matching lines with file paths, line numbers, and content snippets

### Requirement: Maintain orthogonality between search types
The system SHALL ensure file-search and code-search serve distinct purposes.

#### Scenario: file-search vs file-navigation distinction
- **WHEN** comparing file-search to existing file-navigation
- **THEN** file-search SHALL be pattern-based search, file-navigation SHALL be tree-based browsing

#### Scenario: code-search vs file-read distinction
- **WHEN** comparing code-search to existing file-read
- **THEN** code-search SHALL find unknown files containing patterns, file-read SHALL read known files

#### Scenario: file-search vs code-search use case separation
- **WHEN** agent needs to find files by properties
- **THEN** it SHALL use file-search (metadata search)
- **WHEN** agent needs to find files by content
- **THEN** it SHALL use code-search (content search)

### Requirement: Support common tool mappings
The system SHALL map search capabilities to common tools.

#### Scenario: File-search tool mapping
- **WHEN** implementing file-search
- **THEN** it MAY use tools: Glob (Node.js), find (Unix), ripgrep --files, fd

#### Scenario: Code-search tool mapping
- **WHEN** implementing code-search
- **THEN** it MAY use tools: Grep (Unix), ripgrep, ag (Silver Searcher), ack

### Requirement: Enable combined search workflows
The system SHALL support combining file-search and code-search.

#### Scenario: Two-stage search
- **WHEN** agent needs to search specific files for content
- **THEN** it SHALL first use file-search to find files, then code-search within those files

#### Scenario: Independent searches
- **WHEN** searches are unrelated
- **THEN** file-search and code-search SHALL work independently without dependencies
