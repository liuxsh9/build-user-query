## Context

The Concept category contains 93 tags across 3 subcategories (Fundamentals, Advanced, Engineering) covering programming concepts and knowledge areas. Following the successful expansion of Library tags with granularity guidelines, automated alias expansion, and multi-source collection, we need similar infrastructure for Concept tags. However, Concept tags have unique characteristics:

- **Difficulty levels** are critical (basic, intermediate, advanced)
- **Language-specific concepts** require proper language_scope metadata
- **Prerequisite relationships** exist between concepts (e.g., understanding variables before closures)
- **Educational sources** are more relevant than package registries

Current state: 93 Concept tags with ~30% having difficulty levels, ~15% with language_scope. No prerequisite relationships defined.

## Goals / Non-Goals

**Goals:**
- Expand Concept tags from 93 to ~150 with balanced subcategory distribution
- Create CONCEPT_GUIDELINES.md defining granularity for each subcategory
- Add prerequisite field to schema and define key prerequisite relationships
- Ensure all Concept tags have difficulty levels assigned
- Validate language_scope for language-specific concepts
- Extend collection scripts to support educational sources (MDN, W3Schools, academic curricula)

**Non-Goals:**
- Creating a complete prerequisite graph for all concepts (only key relationships)
- Multi-source weighted collection (educational sources are more qualitative)
- Automated difficulty classification (requires human judgment for accuracy)
- Expanding other categories (Language, Domain, Task, etc.)

## Decisions

### Decision 1: Prerequisite Relationships - Explicit vs Inferred

**Options:**
- A) Explicit prerequisite field in schema (e.g., `prerequisites: ["variables", "functions"]`)
- B) Infer from difficulty levels (basic → intermediate → advanced)
- C) No prerequisites, rely on difficulty alone

**Choice: A - Explicit prerequisite field**

**Rationale:**
- Difficulty level alone doesn't capture prerequisite relationships (e.g., "async-programming" and "error-handling" are both intermediate but independent)
- Explicit prerequisites enable better query generation (ensure prerequisite concepts are covered first)
- Allows validation of prerequisite chains (no circular dependencies)
- More maintainable than inference rules

**Trade-off:** Requires manual curation of prerequisite relationships, but only for key concepts (~30-40 relationships needed).

### Decision 2: Granularity Approach - Reuse Library Model vs Concept-Specific

**Options:**
- A) Reuse Library's 3-tier model (library/module/component)
- B) Create Concept-specific granularity levels
- C) Use subcategories as granularity (Fundamentals/Advanced/Engineering)

**Choice: C - Use subcategories as granularity**

**Rationale:**
- Concept tags already have meaningful subcategories that represent granularity
- Fundamentals = foundational concepts (variables, loops, functions)
- Advanced = complex concepts (metaprogramming, concurrency, design patterns)
- Engineering = practices and methodologies (testing, CI/CD, code review)
- Adding another granularity dimension would be redundant

**Trade-off:** Less flexibility than Library model, but simpler and more intuitive.

### Decision 3: Difficulty Classification - Automated vs Manual

**Options:**
- A) Automated classification using LLM or heuristics
- B) Manual classification during collection
- C) Hybrid: automated suggestions, manual approval

**Choice: B - Manual classification during collection**

**Rationale:**
- Difficulty is subjective and context-dependent (e.g., "recursion" is basic in functional programming, advanced in imperative)
- Automated classification would require extensive training data
- Manual classification ensures accuracy and consistency
- Only ~60 new tags need classification (manageable workload)

**Trade-off:** More manual work, but higher quality results.

### Decision 4: Collection Sources - Educational vs Technical

**Options:**
- A) Use same sources as Library (Stack Overflow, GitHub, package registries)
- B) Use educational sources (MDN, W3Schools, programming curricula)
- C) Use academic sources (CS textbooks, research papers)
- D) Hybrid approach with multiple source types

**Choice: B - Educational sources (with manual curation)**

**Rationale:**
- Educational sources better represent concepts developers need to learn
- Stack Overflow is problem-focused, not concept-focused
- Academic sources are too theoretical for practical taxonomy
- Manual curation from trusted sources (MDN, W3Schools, freeCodeCamp) ensures quality

**Trade-off:** No automated weighted scoring like Library tags, but better concept coverage.

### Decision 5: Language-Specific Concepts - Separate Tags vs Metadata

**Options:**
- A) Separate tags for each language (e.g., `rust-borrow-checker`, `python-decorators`)
- B) Generic tags with language_scope metadata (e.g., `borrow-checker` with `language_scope: ["rust"]`)
- C) Hybrid: language-agnostic concepts generic, language-specific concepts separate

**Choice: B - Generic tags with language_scope metadata (existing approach)**

**Rationale:**
- Maintains category orthogonality (Concept vs Language)
- Reduces tag proliferation
- Allows querying by language scope
- Already implemented and working well

**Trade-off:** None - this is the established pattern.

## Risks / Trade-offs

**Risk: Prerequisite cycles**
→ Mitigation: Add validation to detect circular dependencies in prerequisite chains

**Risk: Difficulty level inconsistency**
→ Mitigation: Create difficulty guidelines with examples in CONCEPT_GUIDELINES.md

**Risk: Language-specific concepts missing language_scope**
→ Mitigation: Add validation rule to flag concepts with language-specific names but no language_scope

**Risk: Unbalanced subcategory distribution**
→ Mitigation: Set target ranges per subcategory (Fundamentals: 40-50, Advanced: 50-60, Engineering: 40-50)

**Trade-off: Manual curation vs automation**
- Manual curation ensures quality but requires more time
- Acceptable for ~60 new tags, would not scale to 300+

## Migration Plan

1. **Schema Extension** (non-breaking)
   - Add optional `prerequisites` field to tag schema
   - Add validation for prerequisite references

2. **Guidelines Creation**
   - Create CONCEPT_GUIDELINES.md with subcategory definitions and examples
   - Document difficulty level criteria

3. **Collection & Normalization**
   - Extend scripts to support Concept-specific validation
   - Collect new tags from educational sources
   - Manually assign difficulty levels and prerequisites

4. **Validation**
   - Run enhanced validation with prerequisite cycle detection
   - Verify difficulty distribution
   - Check language_scope coverage

5. **Rollback Strategy**
   - Prerequisites are optional, can be removed without breaking existing functionality
   - New tags can be reverted by restoring concept.yaml from git

## Open Questions

None - design is complete and ready for implementation.
