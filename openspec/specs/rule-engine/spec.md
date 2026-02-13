# rule-engine Specification

## Purpose
Core framework for executing tag detection rules against ShareGPT conversation data. Preprocesses conversations into structured feature vectors, then applies category-specific rules to match tags across all 8 taxonomy categories.

## Requirements

### Requirement: Preprocess ShareGPT records into feature vectors
The system SHALL extract structured features from ShareGPT-format conversation records into a feature vector for downstream rule matching.

#### Scenario: Extract code blocks from conversation
- **WHEN** a ShareGPT record contains markdown fenced code blocks (``` delimited) in any role's content
- **THEN** the system SHALL extract each code block as {language_hint, content} where language_hint is the language identifier after the opening fence (may be empty)

#### Scenario: Extract import statements from code blocks
- **WHEN** code blocks are extracted from a record
- **THEN** the system SHALL identify and extract import/require/using/include statements from all code blocks, normalized to {module_name, language}

#### Scenario: Extract tool calls from assistant messages
- **WHEN** an assistant message contains tool_calls fields
- **THEN** the system SHALL extract each tool call as {name, args} preserving the original structure

#### Scenario: Extract file references from conversation
- **WHEN** any message in the conversation references file paths (e.g., `src/main.py`, `Cargo.toml`)
- **THEN** the system SHALL extract all file path references as a deduplicated list

#### Scenario: Extract user intent verbs
- **WHEN** a user message contains action-oriented instructions
- **THEN** the system SHALL extract key intent verbs (fix, implement, refactor, optimize, test, review, deploy, migrate, explain, etc.) from user messages

#### Scenario: Produce raw text for keyword matching
- **WHEN** a ShareGPT record is preprocessed
- **THEN** the system SHALL produce a concatenated raw_text field combining all roles' content for downstream keyword matching

#### Scenario: Handle missing or malformed fields gracefully
- **WHEN** a ShareGPT record has missing conversations, empty messages, or unexpected structure
- **THEN** the system SHALL produce a valid feature vector with empty lists/strings for missing features, without raising errors

### Requirement: Execute category-specific rules against feature vectors
The system SHALL apply detection rules to feature vectors and return matched tag IDs per category.

#### Scenario: PatternRule matches import statements for Library/Language
- **WHEN** a PatternRule is executed against a feature vector
- **THEN** the system SHALL match import_statements and code_blocks against regex patterns and return all matched tag IDs

#### Scenario: MappingRule maps tool_calls to Agentic tags
- **WHEN** a MappingRule is executed against a feature vector
- **THEN** the system SHALL map tool_call names to Agentic tag IDs via a direct lookup table

#### Scenario: KeywordRule matches Concept/Constraint tags
- **WHEN** a KeywordRule is executed with strong_signals and weak_signals
- **THEN** the system SHALL match strong signals (immediate hit) and accumulate weak signals (hit only when multiple co-occur above threshold), returning matched tag IDs with confidence scores

#### Scenario: IntentRule classifies Task tags
- **WHEN** an IntentRule is executed against a feature vector
- **THEN** the system SHALL match user_intent_verbs and conversation structure patterns to determine Task tag IDs

#### Scenario: StructuralRule classifies Context tag
- **WHEN** a StructuralRule is executed against a feature vector
- **THEN** the system SHALL analyze code_block count, file_references count, and conversation structure to select exactly one Context tag ID according to the defined priority hierarchy

#### Scenario: InferenceRule derives Domain tags
- **WHEN** an InferenceRule is executed with previously matched Library tag IDs
- **THEN** the system SHALL lookup the Library→Domain mapping table to derive Domain tag IDs

### Requirement: Common rule interface
All rule types SHALL implement a common interface for uniform invocation.

#### Scenario: All rules return consistent output format
- **WHEN** any rule type is executed against a feature vector
- **THEN** it SHALL return a list of {tag_id, confidence} pairs where confidence is a float between 0.0 and 1.0

#### Scenario: Rules are loadable from pattern files
- **WHEN** the rule engine initializes
- **THEN** it SHALL load detection patterns from `annotation/patterns/<category>.json` and instantiate the appropriate rule type for each category

### Requirement: Batch processing with parallel execution
The system SHALL support batch processing of multiple records efficiently.

#### Scenario: Process records in batches
- **WHEN** a list of ShareGPT records is submitted for annotation
- **THEN** the system SHALL preprocess and run rules in configurable batch sizes with optional parallel execution

#### Scenario: Output annotation results as JSONL
- **WHEN** batch processing completes
- **THEN** the system SHALL output results as JSONL where each line contains the record ID and a labels object with all 8 category results
