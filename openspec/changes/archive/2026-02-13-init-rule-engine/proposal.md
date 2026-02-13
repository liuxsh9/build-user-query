## Why

We need to annotate ~3M SFT training records (ShareGPT format) with our 672-tag capability taxonomy (8 categories). Direct LLM annotation over all 672 tags is infeasible at this scale. This change builds the initialization infrastructure — rule engine framework, LLM-generated detection patterns, and mapping tables — that all subsequent annotation phases depend on.

## What Changes

- Add a rule engine framework that can execute detection rules against ShareGPT conversation data
- Generate detection patterns for all 672 tags via LLM calls (~1500 calls), organized by category:
  - Library import/usage patterns (339 tags)
  - Concept keyword dictionaries with strong/weak signals (106 tags)
  - Constraint static-analysis detection rules (24 tags)
  - Task conversation-pattern detection rules (21 tags)
  - Context structural-feature detection rules (10 tags)
  - Agentic tool_calls field mapping rules (40 tags)
  - Language syntax fingerprint rules (75 tags)
  - Domain inference via Library→Domain mapping (57 tags)
- Alias completion and cross-check for all 672 tags
- Build Library→Domain mapping table
- Build Concept candidate reduction mapping (given Language+Library+Domain → narrowed Concept candidates)
- Golden Set construction pipeline: per-category LLM annotation with multi-model verification

## Capabilities

### New Capabilities
- `rule-engine`: Core framework for executing tag detection rules against ShareGPT data, including text preprocessing (code block extraction, import extraction, tool_calls parsing, intent verb extraction) and rule matching
- `detection-pattern-generation`: LLM-driven pipeline to generate detection patterns for each tag category (import patterns, keyword dictionaries, structural rules, conversation patterns)
- `tag-mapping-tables`: Static mapping tables derived from taxonomy (Library→Domain, Language+Library+Domain→Concept candidates) used for cross-category inference and candidate reduction
- `golden-set-pipeline`: Pipeline for constructing high-quality labeled golden sets by splitting annotation into per-category small tasks for LLM, with multi-model verification

### Modified Capabilities
- `taxonomy-schema`: Add detection metadata fields to tag schema (import_patterns, usage_patterns, keyword_signals, detection_rules)

## Impact

- New directory `annotation/` for rule engine code, generated patterns, and mapping tables
- New fields in taxonomy YAML files for detection metadata
- Dependencies: Python standard library + YAML parser (no heavy dependencies for rule engine itself)
- LLM API access required for pattern generation (~1500 calls) and golden set construction (~10000 calls)
- Downstream: This is Phase 0 of the 4-phase annotation pipeline; Phases 1-3 depend entirely on the outputs produced here
