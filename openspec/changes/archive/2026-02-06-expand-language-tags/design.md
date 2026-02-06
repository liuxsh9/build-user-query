## Context

Current Language taxonomy has 50 programming languages with basic coverage, but faces several gaps:
- **Missing common languages**: Build tools (Makefile, CMake), markup/config (XML, JSON, YAML, TOML), documentation (TeX, Markdown), template languages
- **No structured metadata**: Lacks information about paradigm, type system, runtime, and primary use cases
- **Limited real-world validation**: Sources (TIOBE, GitHub) don't fully reflect actual project usage
- **Missing business-critical languages**: ArkTS (HarmonyOS), AscendC (AI accelerators) not included

Target: Expand to ~75-90 languages with balanced coverage across paradigms/use cases, plus rich metadata for sophisticated query generation.

## Goals / Non-Goals

**Goals:**
- Add 25-40 missing languages prioritizing real-world project usage
- Add structured metadata: paradigm, typing, runtime, use_cases
- Include business-critical languages (ArkTS, AscendC)
- Enhance aliases with common abbreviations and variations
- Validate coverage against real project language distributions

**Non-Goals:**
- Language version variants (Python 2/3, C++11/17/20) - treat as single language
- Dialect separation (MySQL vs PostgreSQL for SQL) - use primary language only
- Historical/academic-only languages (ALGOL, Simula) unless still in use
- Esoteric languages (Brainfuck, Whitespace) - focus on production use

## Decisions

### Decision 1: Four-field metadata schema

**Choice:** Add 4 metadata fields with controlled vocabularies

**Schema:**
```yaml
paradigm: list[str]  # Can have multiple, e.g., ["object-oriented", "functional"]
  # Values: imperative, functional, object-oriented, declarative,
  #         logic, procedural, concurrent, event-driven
typing: str
  # Values: static, dynamic, gradual, duck, strong-static, weak-dynamic
runtime: str
  # Values: compiled, interpreted, jit, transpiled, hybrid
use_cases: list[str]
  # Values: web, systems, data-science, mobile, embedded, scripting,
  #         devops, scientific, game-dev, blockchain, markup, config, build
```

**Rationale:**
- Paradigm: Essential for understanding language design philosophy, supports multiple (e.g., Scala is OOP + functional)
- Typing: Critical for developer experience and tooling capabilities
- Runtime: Affects performance characteristics and deployment
- Use cases: Enables domain-specific query filtering

**Alternatives considered:**
- More detailed fields (memory model, concurrency model): Too complex for initial version
- Fewer fields (only use_cases): Misses important technical characteristics
- Freeform text: Not queryable, inconsistent

### Decision 2: Tiered gap analysis for language discovery

**Choice:** Three-tier approach to identify missing languages

**Tier 1 - Critical gaps (Must add):**
- Methodology: Analyze top 100 GitHub repositories by stars
- Criteria: Language appears in >10% of repos, not yet in taxonomy
- Examples: Makefile, Dockerfile, YAML, JSON, TeX

**Tier 2 - Common production languages (Should add):**
- Methodology: Cross-reference PYPL, Stack Overflow tags, RedMonk
- Criteria: Appears in top 50 of at least 2 rankings
- Examples: Groovy variants, domain-specific languages with active communities

**Tier 3 - Business/niche languages (May add):**
- Methodology: Business requirements, emerging ecosystems
- Criteria: Strategic importance or growing adoption in specific domains
- Examples: ArkTS, AscendC, blockchain languages (Move, Cairo)

**Rationale:**
- Tier 1 ensures we don't miss ubiquitous languages
- Tier 2 balances popularity with practicality
- Tier 3 provides flexibility for strategic additions

**Alternatives considered:**
- Single cutoff threshold: Misses important niche languages
- Purely popularity-based: Biased toward web/mobile, misses specialized domains
- Manual curation only: Doesn't scale, personal bias

### Decision 3: Multi-source validation with real-world focus

**Choice:** Prioritize sources reflecting actual project usage

**Sources (priority order):**
1. **GitHub language statistics** (40%) - Real project usage
2. **PYPL / Stack Overflow** (30%) - Developer engagement
3. **TIOBE Index** (20%) - Industry trends
4. **RedMonk Rankings** (10%) - Community + code correlation

**Validation criteria:**
- Language must appear in top 100 of at least one source, OR
- Language serves critical infrastructure role (build/config), OR
- Language is business-critical (ArkTS, AscendC)

**Rationale:**
- GitHub reflects what's actually being written
- PYPL/Stack Overflow shows what developers are learning/struggling with
- TIOBE provides long-term trend perspective
- RedMonk balances GitHub with Stack Overflow

**Alternatives considered:**
- Equal weighting: Doesn't reflect relative importance
- GitHub only: Misses emerging languages in learning phase
- Include academic citation counts: Out of scope for production focus

### Decision 4: No version/dialect splitting (unified representation)

**Choice:** Treat language versions and dialects as single entries

**Policy:**
- **Versions**: Python (not Python 2/3), C++ (not C++11/17/20)
- **Dialects**: SQL (not MySQL/PostgreSQL/T-SQL), Lisp (not Common Lisp/Scheme separately)
  - Exception: Distinct dialects already in taxonomy (Clojure, Scheme) remain separate
- **Rationale via use_cases**: Use metadata to differentiate when needed
  - Example: SQL has use_cases: ["database", "data-analysis"]

**Rationale:**
- Simplifies taxonomy, reduces maintenance
- Version differences mostly syntactic, not capability-based
- Query generation rarely needs version-specific targeting
- Can add version metadata later if needed

**Alternatives considered:**
- Full version tracking: Tag explosion (Python 2, 3, 3.6, 3.7...), high maintenance
- Dialect splitting: Ambiguous boundaries (is TypeScript a JavaScript dialect?)

### Decision 5: Alias expansion from real-world patterns

**Choice:** Collect aliases from code import patterns and community usage

**Sources:**
1. **File extensions**: `.py`, `.js`, `.rs`, `.go`
2. **Common abbreviations**: TypeScript → ts, tsx; JavaScript → js, jsx
3. **Stack Overflow tags**: Extract top 3 tag variations per language
4. **Case variations**: Auto-generate lowercase, uppercase (COBOL), title-case

**Validation:**
- Aliases must be unambiguous (no conflicts with other languages)
- Maintain blocklist for confusing aliases (e.g., "C" conflicts with "C language")

**Rationale:**
- File extensions are universal identifiers
- Community tags reflect actual usage patterns
- Case variations handle different naming conventions

**Alternatives considered:**
- Manual curation only: Misses common variations
- Full automation with ML: Overkill, risk of hallucinations

### Decision 6: Incremental rollout by use case category

**Choice:** Add languages in three phases by use case

**Phase 1 - Infrastructure & Config (Priority: High):**
- Build: Makefile, CMake, Bazel, Gradle, Maven
- Config: YAML, TOML, JSON, XML, INI
- Target: +15 languages
- Rationale: Ubiquitous in all projects, critical gap

**Phase 2 - Specialized & Business-Critical (Priority: High):**
- Documentation: TeX, LaTeX, Markdown, reStructuredText
- Business: ArkTS, AscendC
- Template: Jinja, Handlebars, ERB, EJS
- Target: +10 languages
- Rationale: High frequency or strategic importance

**Phase 3 - Emerging & Domain-Specific (Priority: Medium):**
- Blockchain: Move, Cairo, Yul
- Data: Pig, HiveQL
- Hardware: SystemVerilog (if distinct from Verilog)
- Target: +5-15 languages (flexible based on validation)
- Rationale: Growing ecosystems, domain coverage

**Rationale:**
- Phase 1 addresses most visible gaps
- Phase 2 covers business needs and high-frequency uses
- Phase 3 provides domain completeness without over-expansion

**Alternatives considered:**
- Alphabetical/random: No strategic prioritization
- Popularity-only: Misses critical infrastructure languages (Makefile has low TIOBE rank but universal usage)

## Risks / Trade-offs

**Risk:** Metadata classification may be subjective (e.g., is Python OOP or imperative?)
→ **Mitigation:** Allow multiple paradigms, document clear examples, establish review committee for edge cases

**Risk:** Use case categories may overlap (e.g., Python is web + data-science + scripting)
→ **Mitigation:** Use list field to support multiple use cases, prioritize primary use case first

**Risk:** Build/config languages (Makefile, YAML) blur line between "programming language" and "data format"
→ **Mitigation:** Adopt inclusive definition - "any syntax-driven file type used in software development" qualifies

**Trade-off:** Not splitting dialects means less precision for SQL-specific queries
→ **Acceptable:** Can add dialect metadata later if needed; 80/20 rule favors simplicity now

**Trade-off:** Moderate expansion (75-90) may still miss some languages
→ **Acceptable:** Can expand in future phases; better to validate approach with controlled growth

**Risk:** TIOBE/PYPL rankings have recency bias and may miss legacy-but-used languages
→ **Mitigation:** Include Tier 1 gap analysis from actual GitHub repos to catch ubiquitous languages

**Risk:** Business-critical languages (ArkTS, AscendC) may not appear in rankings
→ **Mitigation:** Tier 3 criteria explicitly allows strategic additions regardless of ranking

## Open Questions

- Should we add `ecosystem` field to link languages to package managers (npm, PyPI, crates.io)?
- How to handle languages that are primarily transpiled (CoffeeScript → JS, Elm → JS)?
  - Current thinking: Include if they have distinct syntax/semantics
- Should we track language maturity/stability (experimental, stable, mature)?
- Do we need a `year_created` field for educational/historical context?
- How to handle markup languages (HTML, Markdown) - are they "programming languages"?
  - Current thinking: Include as use_case: "markup" since they're in codebases
