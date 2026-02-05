## Context

Current Library taxonomy has 85 tags with significant quality issues:
- **Granularity inconsistency**: Mix of library-level (React, Django) and module-level (Pandas GroupBy) tags
- **Incomplete aliases**: Missing common variations, abbreviations, and community terminology
- **Limited sources**: Only curated lists, missing real-world usage data

Target: Expand to ~300 high-quality tags with consistent granularity and comprehensive aliases.

## Goals / Non-Goals

**Goals:**
- Establish clear granularity guidelines (3 levels: library, module, component)
- Expand to ~300 Library tags across 5 subcategories
- Implement automated alias extraction from multiple sources
- Integrate Stack Overflow, npm/PyPI, GitHub Topics, academic papers
- Add granularity metadata to enable filtering

**Non-Goals:**
- Function-level tags (too fine-grained, unmaintainable)
- Deprecated/unmaintained libraries (focus on active ecosystem)
- Internal/proprietary libraries (only public, widely-used tools)
- Automatic tag generation without human review

## Decisions

### Decision 1: Three-tier granularity system

**Choice:** Define 3 explicit granularity levels with clear rules

**Levels:**
- **Library-level**: Entire framework/library (e.g., `react`, `django`, `pytorch`)
  - Use when: The library is monolithic or commonly used as a whole
- **Module-level**: Major subsystem/module (e.g., `django-orm`, `pytorch-nn`, `pandas-dataframe`)
  - Use when: Module represents distinct capability worth tracking separately
- **Component-level**: Specific feature/API (e.g., `react-hooks`, `pandas-groupby`)
  - Use when: Component is frequently used independently and represents learnable skill

**Rationale:**
- Provides flexibility while maintaining consistency
- Aligns with how developers think about capabilities
- Enables filtering by granularity for different use cases

**Alternatives considered:**
- Two-tier (library/module): Too coarse, misses important component-level skills
- Four-tier (add function-level): Too fine, leads to tag explosion

### Decision 2: Multi-source collection with weighted prioritization

**Choice:** Collect from 4 sources with priority weighting

**Sources & Weights:**
1. **Stack Overflow tags** (weight: 0.4) - Real developer usage
2. **Package registry stats** (weight: 0.3) - npm/PyPI download counts
3. **GitHub Topics** (weight: 0.2) - Community categorization
4. **Academic papers** (weight: 0.1) - Emerging/research tools

**Rationale:**
- Stack Overflow reflects actual developer pain points and usage
- Download stats indicate real-world adoption
- GitHub Topics capture community consensus
- Academic papers identify emerging tools before mainstream

**Alternatives considered:**
- Single source (curated lists): Misses real-world usage patterns
- Equal weighting: Doesn't reflect relative importance
- Automated scraping only: Risk of noise and low-quality tags

### Decision 3: Automated alias expansion with human validation

**Choice:** Build tool to extract aliases, require human approval

**Extraction methods:**
1. **Import statement analysis**: Parse code repos for common import patterns
   - `import pandas as pd` → alias: "pd"
   - `from django.db import models` → alias: "django-models"
2. **Documentation mining**: Extract abbreviations from official docs
3. **Community terminology**: Analyze Stack Overflow question titles
4. **Case variations**: Auto-generate lowercase, uppercase, kebab-case variants

**Validation workflow:**
1. Tool generates candidate aliases with confidence scores
2. High-confidence (>0.8) auto-approved
3. Medium-confidence (0.5-0.8) flagged for human review
4. Low-confidence (<0.5) discarded

**Rationale:**
- Automation scales to 300+ tags
- Human validation prevents hallucinations and noise
- Confidence scoring focuses human effort on uncertain cases

**Alternatives considered:**
- Fully manual: Too slow for 300 tags
- Fully automated: Risk of incorrect/misleading aliases
- No aliases: Reduces discoverability

### Decision 4: Granularity metadata field

**Choice:** Add `granularity` field to tag schema

```yaml
granularity: enum  # library | module | component
```

**Rationale:**
- Enables filtering by granularity level
- Makes granularity explicit and queryable
- Supports future use cases (e.g., "show only library-level tags")

**Alternatives considered:**
- Encode in tag ID (e.g., `react-lib` vs `react-hooks-component`): Verbose, breaks naming conventions
- Infer from naming patterns: Unreliable, implicit

### Decision 5: Incremental expansion by subcategory

**Choice:** Expand one subcategory at a time in priority order

**Order:**
1. Web (24 → 80 tags) - Largest ecosystem, highest impact
2. Data (17 → 70 tags) - Critical for ML/data science use cases
3. Infrastructure (18 → 60 tags) - DevOps is growing rapidly
4. Testing (14 → 50 tags) - Important for quality
5. Database (12 → 40 tags) - Smaller but essential

**Rationale:**
- Allows validation of process before scaling
- Focuses effort on highest-impact areas first
- Enables parallel work if needed

**Alternatives considered:**
- All at once: Risky, hard to validate quality
- Random order: Misses opportunity to prioritize impact

## Risks / Trade-offs

**Risk:** Granularity guidelines may be subjective for edge cases
→ **Mitigation:** Document examples for each level, establish review process for ambiguous cases

**Risk:** Automated alias extraction may generate incorrect aliases
→ **Mitigation:** Require human validation, use confidence scoring, maintain blocklist of known false positives

**Risk:** 300 tags may still be insufficient for full coverage
→ **Mitigation:** Design for extensibility, plan quarterly reviews to add emerging libraries

**Trade-off:** More tags = more maintenance overhead
→ **Acceptable:** Quality over quantity, focus on widely-used libraries

**Trade-off:** Multi-source collection adds complexity
→ **Acceptable:** Better coverage justifies complexity, sources can be added incrementally

**Risk:** Stack Overflow/npm data may have recency bias
→ **Mitigation:** Balance with academic sources, include "classic" libraries manually

## Open Questions

- Should we version tags to track library version differences (e.g., React 16 vs React 18)?
- How to handle libraries that span multiple subcategories (e.g., FastAPI is both Web and API)?
- Should we track library popularity/maturity as metadata?
