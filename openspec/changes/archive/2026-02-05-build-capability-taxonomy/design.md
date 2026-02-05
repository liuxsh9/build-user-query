## Context

We're building a capability taxonomy to systematically map the programming abilities needed for code generation models. This taxonomy will serve as the foundation for generating diverse SFT queries and measuring training data coverage. The system needs to balance comprehensiveness with maintainability—categories should be stable while tags remain extensible.

## Goals / Non-Goals

**Goals:**
- Define 8 orthogonal categories that cover all dimensions of programming capability
- Create extensible tag system with rich metadata (aliases, difficulty, language scope)
- Build semi-automated tooling for tag collection from multiple sources
- Establish validation rules to maintain taxonomy quality
- Support future labeling workflows (not implemented in this change)

**Non-Goals:**
- Automated labeling of existing training data (future work)
- Query generation based on taxonomy (future work)
- Coverage analysis tools (future work)
- Web UI for taxonomy browsing (YAML files are sufficient for now)

## Decisions

### Decision 1: YAML-based storage over database

**Choice:** Store taxonomy and tags as YAML files in version control

**Rationale:**
- Human-readable and easy to review in PRs
- Version control provides full audit trail
- Simple to edit without tooling
- Easy to consume by downstream scripts
- No infrastructure overhead

**Alternatives considered:**
- SQLite database: Better for querying but adds complexity, harder to review changes
- JSON: Less human-friendly than YAML for manual editing

### Decision 2: Mixed hierarchy (some categories two-level, others flat)

**Choice:** Library and Concept use subcategories; others remain flat

**Rationale:**
- Library has 500-1000 tags—subcategories (Web, Data, Infrastructure) aid navigation
- Concept benefits from Fundamentals/Advanced/Engineering grouping
- Other categories have <100 tags each—flat structure is simpler
- Avoids over-engineering while providing structure where needed

**Alternatives considered:**
- All flat: Would make Library category unwieldy
- All hierarchical: Unnecessary complexity for small categories

### Decision 3: Medium-granularity tags

**Choice:** Tags like `pandas-groupby` (module-level) not `pandas-dataframe-merge` (function-level)

**Rationale:**
- Balances specificity with maintainability
- Can distinguish "basic Pandas" from "advanced aggregations"
- Avoids tag explosion (thousands of function-level tags)
- Aligns with how developers think about capabilities

**Alternatives considered:**
- Coarse (library-level): Can't distinguish skill levels within a library
- Fine (function-level): Unmaintainable, 10,000+ tags

### Decision 4: Language-scoped concepts in Concept category

**Choice:** Rust-specific concepts like "borrow-checker" go in Concept with `language_scope: [rust]`

**Rationale:**
- Maintains category orthogonality (Language = which language, Concept = what knowledge)
- `language_scope` metadata makes applicability explicit
- Supports both language-specific and cross-language concepts in one place

**Alternatives considered:**
- Separate "Language Features" category: Adds complexity, unclear boundary with Concept
- Nested under Language: Breaks orthogonality, makes querying harder

### Decision 5: LLM-assisted collection with human validation

**Choice:** Use LLM to generate candidate tags from sources, require human approval

**Rationale:**
- LLM can quickly extract tags from docs, awesome-lists, benchmarks
- Human validation ensures quality and prevents hallucinations
- Semi-automated approach balances speed with accuracy
- Iterative: start with high-confidence sources, expand over time

**Alternatives considered:**
- Fully manual: Too slow for 1000+ tags
- Fully automated: Risk of low-quality or hallucinated tags

## Risks / Trade-offs

**Risk:** Tag granularity inconsistency across categories
→ **Mitigation:** Document granularity guidelines per category, review in validation script

**Risk:** Taxonomy becomes stale as new libraries/languages emerge
→ **Mitigation:** Design for extensibility, establish quarterly review process

**Risk:** Subjective categorization (is X a Concept or a Domain?)
→ **Mitigation:** Document decision criteria, maintain examples in taxonomy.yaml

**Trade-off:** YAML files don't support complex queries
→ **Acceptable:** For initial version, simple scripts suffice. Can migrate to DB later if needed.

**Trade-off:** Medium granularity may miss nuances
→ **Acceptable:** Can split tags later if coverage analysis reveals gaps. Start conservative.

## Open Questions

- Should we version the taxonomy schema to support evolution?
- How often should we refresh tags from external sources (quarterly, annually)?
- Do we need a formal process for proposing new tags, or is PR-based sufficient?
