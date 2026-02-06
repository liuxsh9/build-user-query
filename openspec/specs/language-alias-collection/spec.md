# language-alias-collection Specification

## Purpose
Enhance Language tag discoverability by collecting comprehensive aliases from real-world usage patterns, including file extensions, common abbreviations, community tags, and case variations. Ensures unambiguous mapping and maintains blocklist for conflict prevention.

## Requirements

### Requirement: Define four alias source types
The system SHALL collect aliases from four distinct source types with different extraction methods.

#### Scenario: File extension aliases
- **WHEN** collecting file extension aliases
- **THEN** system SHALL extract canonical file extensions for each language (e.g., .py, .js, .rs)

#### Scenario: Common abbreviation aliases
- **WHEN** collecting common abbreviations
- **THEN** system SHALL include standard short forms (e.g., TypeScript → ts, tsx; JavaScript → js, jsx)

#### Scenario: Stack Overflow tag aliases
- **WHEN** collecting Stack Overflow aliases
- **THEN** system SHALL extract top 3 tag variations per language from Stack Overflow tag database

#### Scenario: Case variation aliases
- **WHEN** generating case variations
- **THEN** system SHALL auto-generate lowercase, uppercase, and title-case variants

### Requirement: Extract file extension aliases
The system SHALL extract and validate file extensions as primary language identifiers.

#### Scenario: Extension format
- **WHEN** adding file extension alias
- **THEN** it SHALL be stored without leading dot (py, not .py) for consistency

#### Scenario: Multiple extensions per language
- **WHEN** a language has multiple standard extensions
- **THEN** system SHALL include all common variants (e.g., C++: cpp, cxx, cc, hpp, hxx)

#### Scenario: Extension uniqueness
- **WHEN** an extension maps to multiple languages (e.g., .h for C and C++)
- **THEN** system SHALL assign to primary language only and document ambiguity

#### Scenario: Extension priority
- **WHEN** multiple extensions exist
- **THEN** most common extension SHALL be listed first in aliases

### Requirement: Collect common abbreviation aliases
The system SHALL identify and validate common abbreviations used in developer communication.

#### Scenario: Official abbreviation collection
- **WHEN** language has official abbreviation
- **THEN** system SHALL include it (e.g., JS for JavaScript, TS for TypeScript)

#### Scenario: Framework-specific variations
- **WHEN** language has framework-specific file extensions
- **THEN** system SHALL include them (e.g., jsx, tsx for JavaScript/TypeScript + React)

#### Scenario: Abbreviation case sensitivity
- **WHEN** abbreviation has multiple case conventions
- **THEN** system SHALL include common variants (e.g., js, JS; ts, TS)

### Requirement: Extract Stack Overflow tag variations
The system SHALL analyze Stack Overflow tags to capture community-driven terminology.

#### Scenario: Tag frequency analysis
- **WHEN** analyzing Stack Overflow tags
- **THEN** system SHALL rank tags by question count for each language

#### Scenario: Top 3 tag extraction
- **WHEN** selecting tags for a language
- **THEN** system SHALL extract top 3 variations by frequency

#### Scenario: Tag normalization
- **WHEN** Stack Overflow tag contains hyphens or underscores
- **THEN** system SHALL generate normalized versions (e.g., c-sharp → csharp, c_sharp)

#### Scenario: Tag deduplication
- **WHEN** Stack Overflow tag matches existing alias
- **THEN** system SHALL skip duplicate and move to next ranked tag

### Requirement: Generate case variation aliases
The system SHALL auto-generate case variations to handle different naming conventions.

#### Scenario: Lowercase generation
- **WHEN** generating case variations
- **THEN** system SHALL create lowercase version of language name

#### Scenario: Uppercase generation
- **WHEN** generating case variations for acronym languages
- **THEN** system SHALL create uppercase version (e.g., COBOL, SQL, HTML)

#### Scenario: Title case generation
- **WHEN** language name has multiple words
- **THEN** system SHALL generate title case version (e.g., Objective-C, F-Sharp)

#### Scenario: Special character handling
- **WHEN** language name contains special characters (#, +, etc.)
- **THEN** system SHALL generate both symbolic and written-out versions (C# → c-sharp, csharp)

### Requirement: Validate alias uniqueness
The system SHALL ensure aliases unambiguously map to single languages.

#### Scenario: Uniqueness check
- **WHEN** adding a new alias
- **THEN** system SHALL verify it doesn't exist as alias or name for another language

#### Scenario: Conflict detection
- **WHEN** alias conflicts with existing language
- **THEN** system SHALL reject alias and log conflict for manual review

#### Scenario: Blocklist enforcement
- **WHEN** alias is in blocklist
- **THEN** system SHALL reject it regardless of source (e.g., "C" alone is too ambiguous)

#### Scenario: Cross-category check
- **WHEN** validating alias uniqueness
- **THEN** system SHALL check against aliases in all categories (Library, Domain, etc.) to prevent cross-category conflicts

### Requirement: Maintain alias blocklist
The system SHALL maintain and enforce a blocklist of confusing or ambiguous aliases.

#### Scenario: Blocklist initialization
- **WHEN** blocklist is created
- **THEN** it MUST include known ambiguous terms: C, v, r, d, go (conflicts with verb)

#### Scenario: Blocklist update
- **WHEN** alias conflict is manually reviewed
- **THEN** reviewer MAY add rejected alias to blocklist with reason

#### Scenario: Blocklist documentation
- **WHEN** alias is blocklisted
- **THEN** entry MUST include: alias, reason, conflicting entities

#### Scenario: Blocklist override
- **WHEN** blocklisted alias is essential for major language
- **THEN** it MAY be allowed with explicit disambiguation context (e.g., Go language has "go" despite verb conflict)

### Requirement: Generate alias report
The system SHALL generate comprehensive report showing aliases by source type.

#### Scenario: Report structure
- **WHEN** generating alias report
- **THEN** it MUST group aliases by language, then by source type

#### Scenario: Source attribution
- **WHEN** listing an alias
- **THEN** it MUST show: alias, source type, confidence/frequency, any conflicts

#### Scenario: Coverage statistics
- **WHEN** report is complete
- **THEN** it MUST show: total aliases, aliases per language (avg, min, max), source type distribution

#### Scenario: Conflict section
- **WHEN** conflicts are detected
- **THEN** report MUST include separate section listing all conflicts requiring manual resolution

### Requirement: Support human review workflow
The system SHALL flag uncertain aliases for human validation before addition.

#### Scenario: Auto-approval criteria
- **WHEN** alias is from file extension source
- **THEN** it SHALL be auto-approved (high confidence)

#### Scenario: Auto-approval for official abbreviations
- **WHEN** alias is documented in language official documentation
- **THEN** it SHALL be auto-approved

#### Scenario: Review flagging for Stack Overflow tags
- **WHEN** Stack Overflow tag frequency is <1000 questions
- **THEN** it SHALL be flagged for human review (low confidence)

#### Scenario: Review flagging for case variations
- **WHEN** case variation creates potential ambiguity
- **THEN** it SHALL be flagged for human review

#### Scenario: Batch approval
- **WHEN** reviewer approves multiple aliases
- **THEN** system SHALL support batch operations to speed review process

### Requirement: Update taxonomy files with aliases
The system SHALL update language.yaml with collected and approved aliases.

#### Scenario: Alias list update
- **WHEN** updating a language tag
- **THEN** system SHALL merge new aliases with existing, preserving order

#### Scenario: Deduplication during update
- **WHEN** new alias already exists for language
- **THEN** system SHALL skip duplicate silently

#### Scenario: Alphabetical sorting
- **WHEN** updating alias list
- **THEN** system SHALL sort aliases alphabetically within each language tag

#### Scenario: Backup before update
- **WHEN** updating language.yaml
- **THEN** system SHALL create backup of current file with timestamp

### Requirement: Enable incremental alias expansion
The system SHALL support periodic re-collection to discover new aliases as community evolves.

#### Scenario: Delta detection
- **WHEN** re-running alias collection
- **THEN** system SHALL compare against current taxonomy and report only new aliases

#### Scenario: Trend detection
- **WHEN** Stack Overflow tag frequency changes significantly
- **THEN** system SHALL flag rising aliases for consideration

#### Scenario: Deprecation detection
- **WHEN** previously common alias drops in frequency
- **THEN** system SHALL flag it for review (consider removal)
