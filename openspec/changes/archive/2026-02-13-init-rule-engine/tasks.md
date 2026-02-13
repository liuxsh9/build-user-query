## 1. Project Structure & Data Models

- [ ] 1.1 Create `annotation/` directory structure: `annotation/{patterns/, mappings/, golden_set/, engine/}`
- [ ] 1.2 Define ShareGPT record data model (TypedDict/dataclass for conversation format with roles, content, tool_calls)
- [ ] 1.3 Define FeatureVector data model (code_blocks, import_statements, tool_calls, file_references, user_intent_verbs, raw_text)
- [ ] 1.4 Define AnnotationResult data model (record_id, labels dict with 8 categories, each containing list of {tag_id, confidence})

## 2. Preprocessing Pipeline

- [ ] 2.1 Implement code block extractor (parse markdown fenced blocks → list of {language_hint, content})
- [ ] 2.2 Implement import statement extractor (regex-based extraction for Python/JS/TS/Rust/Go/Java/C#/Ruby/PHP/etc.)
- [ ] 2.3 Implement tool_calls extractor (parse tool_calls from assistant messages)
- [ ] 2.4 Implement file reference extractor (regex-based path detection in conversation text)
- [ ] 2.5 Implement user intent verb extractor (action verb detection from user messages)
- [ ] 2.6 Implement raw text concatenator (combine all roles' content)
- [ ] 2.7 Integrate all extractors into a `preprocess(record) → FeatureVector` function with graceful error handling

## 3. Rule Engine Framework

- [ ] 3.1 Define abstract Rule interface: `match(features: FeatureVector) → list[{tag_id, confidence}]`
- [ ] 3.2 Implement PatternRule (regex matching against import_statements and code_blocks for Language/Library)
- [ ] 3.3 Implement MappingRule (direct lookup from tool_calls.name → tag_id for Agentic)
- [ ] 3.4 Implement KeywordRule (strong/weak signal weighted matching with threshold for Concept/Constraint)
- [ ] 3.5 Implement IntentRule (user_intent_verbs + conversation structure pattern matching for Task)
- [ ] 3.6 Implement StructuralRule (code_block count, file_references, structure heuristics for Context, returns single tag)
- [ ] 3.7 Implement InferenceRule (Library→Domain mapping lookup, confidence aggregation for Domain)
- [ ] 3.8 Implement RuleEngine class: loads pattern files, instantiates rules per category, runs all rules on a FeatureVector, returns AnnotationResult
- [ ] 3.9 Implement batch processing: process records in configurable batch sizes with optional multiprocessing
- [ ] 3.10 Implement JSONL output writer for annotation results

## 4. Detection Pattern Generation (LLM Pipeline)

- [ ] 4.1 Create LLM call utility with retry logic, structured JSON output parsing, and configurable model selection
- [ ] 4.2 Create prompt template for Library import pattern generation (input: tag metadata → output: import_patterns, usage_patterns, config_patterns, negative_patterns)
- [ ] 4.3 Generate Library detection patterns for all 339 tags, store in `annotation/patterns/library.json`
- [ ] 4.4 Create prompt template for Language syntax fingerprint generation (input: tag metadata → output: syntax_fingerprints, file_extensions, code_fence_hints, keyword_patterns)
- [ ] 4.5 Generate Language detection patterns for all 75 tags, store in `annotation/patterns/language.json`
- [ ] 4.6 Create prompt template for Concept keyword dictionary generation (input: tag metadata → output: strong_signals, weak_signals, code_patterns, negative_patterns)
- [ ] 4.7 Generate Concept keyword dictionaries for all 106 tags, store in `annotation/patterns/concept.json`
- [ ] 4.8 Create prompt template for Constraint detection rule generation (input: tag metadata → output: detection_signals, absence_signals, context_keywords)
- [ ] 4.9 Generate Constraint detection rules for all 24 tags, store in `annotation/patterns/constraint.json`
- [ ] 4.10 Create prompt template for Task conversation pattern generation (input: tag metadata → output: user_intent_patterns, assistant_action_patterns, structural_signals)
- [ ] 4.11 Generate Task detection patterns for all 21 tags, store in `annotation/patterns/task.json`
- [ ] 4.12 Build Agentic tool_calls mapping table from tag aliases + LLM augmentation, store in `annotation/patterns/agentic.json`
- [ ] 4.13 Build Context structural detection rules with priority ordering, store in `annotation/patterns/context.json`
- [ ] 4.14 Validate all generated patterns: tag IDs exist in taxonomy, language_scope consistency, no duplicate patterns

## 5. Alias Completion & Verification

- [ ] 5.1 Create prompt template for alias review (input: tag with existing aliases → output: suggested additions, conflict flags)
- [ ] 5.2 Run alias completion for all 672 tags via LLM
- [ ] 5.3 Cross-check aliases across categories, report conflicts
- [ ] 5.4 Apply verified alias additions to taxonomy YAML files (with human review gate)

## 6. Mapping Tables

- [ ] 6.1 Create prompt template for Library→Domain mapping (input: library tag → output: list of domain IDs)
- [ ] 6.2 Generate Library→Domain mapping for all 339 libraries, store in `annotation/mappings/library_to_domain.json`
- [ ] 6.3 Validate mapping: all library IDs and domain IDs exist in taxonomy
- [ ] 6.4 Create prompt template for Concept candidate reduction (input: language+domain pair → output: list of relevant concept IDs)
- [ ] 6.5 Generate Concept candidate mapping for ~200 common (Language, Domain) pairs, store in `annotation/mappings/concept_candidates.json`
- [ ] 6.6 Implement candidate lookup with fallback logic for unmapped combinations

## 7. Golden Set Pipeline

- [ ] 7.1 Implement file-stratified sampling: select 15-20 diverse records per source file
- [ ] 7.2 Create per-category annotation prompt templates (Language, Library split by subcategory, Concept split by subcategory, Domain, Task, Constraint, Agentic, Context)
- [ ] 7.3 Implement single-model annotation pipeline: for each record, run all per-category prompts, merge results
- [ ] 7.4 Implement dual-model annotation: run pipeline with two different models independently
- [ ] 7.5 Implement disagreement arbitration: for each tag disagreement, prompt a third model with context
- [ ] 7.6 Implement golden set output: write results to `annotation/golden_set/golden_set.jsonl`
- [ ] 7.7 Implement quality report: inter-model agreement rate per category, arbitration stats, tag distribution

## 8. Integration & Validation

- [ ] 8.1 End-to-end test: preprocess a sample ShareGPT record → run rule engine → verify output format
- [ ] 8.2 Validate rule engine against golden set: compute precision/recall per category, identify low-performance rules
- [ ] 8.3 Document pattern generation prompts and configuration for reproducibility
