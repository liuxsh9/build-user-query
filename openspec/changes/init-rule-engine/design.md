## Context

The project has built a 672-tag capability taxonomy across 8 categories (Language 75, Library 339, Concept 106, Domain 57, Agentic 40, Constraint 24, Task 21, Context 10). The next goal is to annotate ~3M SFT training records (ShareGPT format, organized in ~50 files) with these tags.

Direct LLM annotation over 672 tags at 3M scale is infeasible. The exploration phase established a multi-layer approach: deterministic rules handle most categories, with models only used for residual cases against a narrowed candidate set.

This change (Phase 0) builds the foundation: rule engine framework, LLM-generated detection patterns, mapping tables, and golden set pipeline. All subsequent annotation phases depend on this.

The training data is in ShareGPT format with multi-turn conversations including user messages, assistant responses, tool_calls, and tool outputs. Each record provides rich signals across all roles.

## Goals / Non-Goals

**Goals:**
- Build a rule engine framework that processes ShareGPT conversations and matches against tag detection rules
- Generate high-quality detection patterns for all 672 tags via LLM (~1500 calls)
- Build cross-category mapping tables (Library→Domain, Language+Library+Domain→Concept candidates)
- Verify and complete aliases for all 672 tags
- Establish golden set construction pipeline using per-category LLM annotation
- All outputs must be serializable, inspectable, and incrementally updatable

**Non-Goals:**
- File-level profiling (Phase 1)
- Record-level annotation pipeline (Phase 2)
- Intra-file clustering (Phase 2)
- Post-processing and validation (Phase 3)
- Training any models

## Decisions

### Decision 1: Rule engine operates on preprocessed feature vectors, not raw text

**Choice**: Preprocessing step extracts structured features from each ShareGPT record first, then rules match against features.

**Rationale**: Many rules need the same extracted features (code blocks, import statements, tool_calls). Extracting once and caching avoids redundant parsing. It also makes rule authoring simpler — rules operate on clean structured data.

**Preprocessed features**:
- `code_blocks`: list of {language_hint, content} extracted from markdown fenced blocks
- `import_statements`: list of import/require/using statements extracted from code blocks
- `tool_calls`: list of {name, args} from assistant tool_call fields
- `file_references`: list of file paths mentioned in conversation
- `user_intent_verbs`: extracted action verbs from user messages (fix, implement, refactor, etc.)
- `raw_text`: concatenated conversation text for keyword matching

**Alternative**: Run rules directly on raw conversation JSON. Rejected because rules would each need to implement their own text extraction logic, leading to duplication and inconsistency.

### Decision 2: Detection patterns stored as JSON alongside YAML taxonomy, not embedded in YAML

**Choice**: Generated detection patterns stored in `annotation/patterns/<category>.json`, separate from taxonomy YAML.

**Rationale**:
- Taxonomy YAML files are the source of truth for tag definitions; detection patterns are derived artifacts
- Patterns are LLM-generated and may need regeneration; keeping them separate avoids polluting curated taxonomy data
- Patterns can be version-controlled independently
- Pattern files can include metadata (generation model, timestamp, confidence) without cluttering tag schema

**Alternative**: Embed patterns directly in each tag's YAML entry. Rejected because it mixes curated and generated data, and makes pattern regeneration risky for taxonomy integrity.

### Decision 3: Category-specific rule types with a common interface

**Choice**: Each category has its own rule type optimized for its detection characteristics, but all expose a common `match(features) → list[tag_id]` interface.

Rule types:
- **PatternRule** (Language, Library): regex matching against import_statements and code_blocks
- **MappingRule** (Agentic): direct lookup from tool_calls.name → tag_id
- **KeywordRule** (Concept, Constraint): weighted keyword matching with strong/weak signals and threshold
- **IntentRule** (Task): pattern matching on user_intent_verbs + conversation structure
- **StructuralRule** (Context): heuristics on code_block count, file_references, conversation structure
- **InferenceRule** (Domain): derived from other categories' results via Library→Domain mapping

**Alternative**: Uniform rule type for all categories. Rejected because categories have fundamentally different detection characteristics; a one-size-fits-all approach would be either too simple for some or unnecessarily complex for others.

### Decision 4: LLM pattern generation uses structured output with validation

**Choice**: Each LLM call for pattern generation uses a category-specific prompt template with JSON structured output. Generated patterns are validated against the taxonomy (tag IDs must exist, language_scope must be consistent) before storage.

**Rationale**: Structured output ensures parseable results. Validation catches hallucinated tag IDs or inconsistent patterns before they enter the rule engine.

### Decision 5: Concept candidate reduction uses a two-level mapping

**Choice**:
- Level 1 (static): Precomputed mapping from common (Language, Domain) pairs → candidate Concept set. Built via LLM (~200 calls covering frequent combinations).
- Level 2 (dynamic): At runtime, keyword pre-screening further narrows candidates based on actual content.

The union of both levels forms the final candidate set for model-based annotation in later phases.

**Rationale**: Static mapping alone misses edge cases. Keyword screening alone has false negatives. Combining both provides high recall with manageable candidate set sizes (typically 15-30 out of 106).

### Decision 6: Golden set uses per-category independent annotation with multi-model verification

**Choice**: For each golden record, annotate each category independently via separate LLM calls. Use two different models per record, with a third model arbitrating disagreements.

**Rationale**:
- Per-category annotation keeps each call's label space small (max 106 for Concept, but typically split into subcategories of ~40)
- Multi-model verification catches individual model biases
- Independent category annotation avoids cross-category interference
- Cost: ~1000 records × 8-12 calls × 2-3 models = ~20K-30K calls, acceptable

## Risks / Trade-offs

**[Risk] LLM-generated patterns may have low recall for rare/niche tags**
→ Mitigation: Validation against golden set will expose low-recall tags; patterns can be iteratively refined. Aliases from Phase 0.2 help expand coverage.

**[Risk] Keyword-based Concept detection may produce false positives**
→ Mitigation: Strong/weak signal separation with configurable thresholds. Weak signals only contribute when multiple co-occur. Model fallback in Phase 2 handles ambiguous cases.

**[Risk] Library→Domain mapping may be incomplete for multi-domain libraries**
→ Mitigation: Allow many-to-many mapping (one library → multiple domains). LLM generates the mapping with validation against existing Domain tags.

**[Risk] Context detection heuristics may be brittle for edge cases**
→ Mitigation: Context is single-select with only 10 options; define a clear priority hierarchy. Golden set validation will calibrate thresholds.

**[Trade-off] Separate pattern files vs. embedded in taxonomy**
→ Accepted: Extra file management complexity in exchange for clean separation of curated vs. generated data.

**[Trade-off] ~1500 LLM calls for initialization**
→ Accepted: One-time cost that dramatically reduces per-record annotation cost. Patterns are reusable and incrementally updatable.
