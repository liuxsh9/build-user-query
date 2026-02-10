## ADDED Requirements

### Requirement: Generate Library import detection patterns
The system SHALL generate regex-based import detection patterns for all 339 Library tags via LLM.

#### Scenario: Generate patterns for a single library tag
- **WHEN** a Library tag with id, name, aliases, and language_scope is submitted to the generation pipeline
- **THEN** the LLM SHALL produce a JSON object containing import_patterns (list of regex strings for import/require/using statements), usage_patterns (list of regex strings for common API usage), config_patterns (list of strings for package manager files like requirements.txt, package.json), and negative_patterns (list of patterns that should NOT trigger a match)

#### Scenario: Patterns respect language_scope
- **WHEN** a Library tag has language_scope defined (e.g., ["python"])
- **THEN** the generated import_patterns SHALL use language-appropriate import syntax (e.g., `from X import` for Python, `require('X')` for JavaScript)

#### Scenario: Store generated patterns
- **WHEN** patterns are generated for all Library tags
- **THEN** the system SHALL store them in `annotation/patterns/library.json` with metadata including generation_model, generation_timestamp, and tag_count

### Requirement: Generate Language syntax fingerprint patterns
The system SHALL generate syntax detection patterns for all 75 Language tags via LLM.

#### Scenario: Generate patterns for a single language tag
- **WHEN** a Language tag with id, name, aliases, paradigm, and runtime is submitted
- **THEN** the LLM SHALL produce syntax_fingerprints (list of distinctive syntax patterns), file_extensions (list of associated extensions), code_fence_hints (list of markdown fence identifiers like "python", "py"), and keyword_patterns (list of language-unique keywords)

#### Scenario: Store generated patterns
- **WHEN** patterns are generated for all Language tags
- **THEN** the system SHALL store them in `annotation/patterns/language.json`

### Requirement: Generate Concept keyword dictionaries
The system SHALL generate keyword detection dictionaries for all 106 Concept tags via LLM.

#### Scenario: Generate keywords for a single concept tag
- **WHEN** a Concept tag with id, name, subcategory, difficulty, and optional language_scope is submitted
- **THEN** the LLM SHALL produce strong_signals (list of highly distinctive keywords/patterns that definitively indicate this concept), weak_signals (list of keywords that suggest but don't confirm this concept), code_patterns (list of regex patterns for code structure detection), and negative_patterns (list of patterns that should exclude a match)

#### Scenario: Language-scoped concepts produce scoped patterns
- **WHEN** a Concept tag has language_scope (e.g., borrow-checker with ["rust"])
- **THEN** the generated patterns SHALL be specific to those languages and include language-specific syntax

#### Scenario: Store generated dictionaries
- **WHEN** dictionaries are generated for all Concept tags
- **THEN** the system SHALL store them in `annotation/patterns/concept.json`

### Requirement: Generate Constraint detection rules
The system SHALL generate static-analysis-style detection rules for all 24 Constraint tags via LLM.

#### Scenario: Generate rules for a single constraint tag
- **WHEN** a Constraint tag with id, name, aliases, and optional description is submitted
- **THEN** the LLM SHALL produce detection_signals (list of code/conversation patterns indicating this constraint), absence_signals (list of patterns whose absence indicates this constraint, e.g., no-recursion = no recursive calls), and context_keywords (list of natural language keywords in conversation suggesting this constraint)

#### Scenario: Store generated rules
- **WHEN** rules are generated for all Constraint tags
- **THEN** the system SHALL store them in `annotation/patterns/constraint.json`

### Requirement: Generate Task conversation pattern rules
The system SHALL generate conversation pattern detection rules for all 21 Task tags via LLM.

#### Scenario: Generate patterns for a single task tag
- **WHEN** a Task tag with id, name, aliases, and description is submitted
- **THEN** the LLM SHALL produce user_intent_patterns (list of regex patterns for user request classification), assistant_action_patterns (list of patterns for what the assistant does in response), structural_signals (list of conversation structure features like "contains diff", "asks follow-up question")

#### Scenario: Store generated patterns
- **WHEN** patterns are generated for all Task tags
- **THEN** the system SHALL store them in `annotation/patterns/task.json`

### Requirement: Generate Agentic tool_calls mapping rules
The system SHALL generate mapping rules from tool_call names to Agentic tag IDs.

#### Scenario: Build tool_calls mapping table
- **WHEN** all 40 Agentic tags with their aliases are provided
- **THEN** the system SHALL produce a mapping table from common tool_call function names (read_file, write_file, search, bash, etc.) to corresponding Agentic tag IDs, supporting many-to-one mapping (multiple tool names → one tag)

#### Scenario: Store mapping rules
- **WHEN** mapping rules are generated
- **THEN** the system SHALL store them in `annotation/patterns/agentic.json`

### Requirement: Generate Context structural detection rules
The system SHALL generate structural feature detection rules for all 10 Context tags.

#### Scenario: Define context detection heuristics
- **WHEN** all 10 Context tags are provided
- **THEN** the system SHALL produce a priority-ordered list of detection rules, each with structural_conditions (e.g., "code_blocks.count == 1 AND code_blocks[0].lines < 10") and the target Context tag ID

#### Scenario: Context rules are mutually exclusive by priority
- **WHEN** multiple Context rules match a feature vector
- **THEN** the highest-priority matching rule SHALL determine the single Context tag

#### Scenario: Store detection rules
- **WHEN** rules are generated
- **THEN** the system SHALL store them in `annotation/patterns/context.json`

### Requirement: Validate generated patterns against taxonomy
The system SHALL validate all generated patterns for consistency with the taxonomy.

#### Scenario: All tag IDs in patterns exist in taxonomy
- **WHEN** pattern files are validated
- **THEN** every tag_id referenced in patterns SHALL exist in the corresponding taxonomy YAML file

#### Scenario: Language scope consistency
- **WHEN** a pattern references a language-scoped tag
- **THEN** the pattern's language-specific syntax SHALL be consistent with the tag's language_scope field

### Requirement: Complete and verify aliases for all tags
The system SHALL use LLM to review and complete aliases for all 672 tags.

#### Scenario: Generate alias suggestions for a tag
- **WHEN** a tag with id, name, and existing aliases is submitted for alias review
- **THEN** the LLM SHALL suggest additional aliases (common abbreviations, alternative spellings, community names) and flag any potentially conflicting aliases that overlap with other tags

#### Scenario: Cross-check aliases across categories
- **WHEN** alias completion is done for all tags
- **THEN** the system SHALL report any alias that maps to tags in different categories as a potential conflict requiring manual review
