## Context

The Domain category currently has 32 tags representing major application domains (Web Frontend, Machine Learning, IoT, etc.). Based on the successful expansion of Library tags (86→339), we're now expanding Domain tags to improve coverage of modern software development areas.

**Current state:**
- 32 domain tags covering traditional application areas
- Gaps in emerging domains (MLOps, Edge Computing, Serverless)
- Missing specialized subfields (Bioinformatics, Geospatial, Audio Processing)
- Lacking cross-cutting domains (Accessibility, Internationalization)

**Constraints:**
- Domain tags must be at application-level granularity (not too broad like "Software", not too narrow like "React Forms")
- Must maintain flat taxonomy structure (no subcategories)
- Must be orthogonal to other categories (Library, Concept, etc.)
- Each domain should represent a distinct application area with its own ecosystem

## Goals / Non-Goals

**Goals:**
- Expand Domain tags from 32 to ~50-60 tags
- Cover emerging technology domains (MLOps, DataOps, Edge Computing, Serverless, etc.)
- Cover specialized application subfields (Bioinformatics, Geospatial, Audio/Video Processing, etc.)
- Cover cross-cutting domains (Accessibility, Internationalization, Real-time Systems, etc.)
- Ensure all tags have clear descriptions and aliases
- Maintain validation passing with 0 errors

**Non-Goals:**
- Not building automated collection tools (manual curation is sufficient)
- Not adding subcategories to Domain (keep flat structure)
- Not expanding other categories in this change
- Not changing existing domain tags (only additions)

## Decisions

### Decision 1: Manual Curation vs Automated Collection
**Choice:** Manual curation
**Rationale:**
- Domain tags require careful consideration of scope and granularity
- Only adding ~18-28 tags (manageable manually)
- Quality over speed - each domain needs thoughtful definition
- Proven successful with Library expansion

**Alternatives considered:**
- Automated collection from job postings: Too noisy, requires heavy filtering
- Industry survey scraping: Time-consuming, may miss emerging domains

### Decision 2: Target Count (50-60 tags)
**Choice:** Aim for 50-60 total tags (~18-28 new)
**Rationale:**
- Balances comprehensive coverage with maintainability
- Aligns with taxonomy design principle of medium granularity
- Enough to cover emerging and specialized domains without over-fragmenting

**Alternatives considered:**
- 100+ tags: Too granular, would overlap with Library/Concept categories
- 40 tags: Insufficient coverage of emerging domains

### Decision 3: Three Focus Areas
**Choice:** Organize collection around three themes:
1. **Emerging domains**: MLOps, DataOps, Edge Computing, Serverless, Platform Engineering
2. **Specialized subfields**: Bioinformatics, Geospatial, Audio/Video Processing, Quantum Computing
3. **Cross-cutting domains**: Accessibility, Internationalization, Real-time Systems, Observability

**Rationale:**
- Ensures systematic coverage without gaps
- Each theme addresses a different type of missing coverage
- Easy to validate completeness

### Decision 4: Validation Criteria
**Choice:** Each domain tag must pass:
- **Scope test**: Represents a distinct application area (not a library or concept)
- **Granularity test**: Not too broad (e.g., "Software") or too narrow (e.g., "Login Forms")
- **Distinctiveness test**: Not overlapping with existing domains
- **Ecosystem test**: Has its own tools, libraries, and community

**Rationale:**
- Maintains taxonomy quality and orthogonality
- Prevents scope creep and category confusion
- Ensures each tag adds value

## Risks / Trade-offs

**Risk:** Domain boundaries may be fuzzy (e.g., is "MLOps" part of "Machine Learning" or separate?)
→ **Mitigation:** Use the distinctiveness test - if a domain has its own ecosystem, tools, and job roles, it's distinct enough

**Risk:** Emerging domains may become obsolete quickly
→ **Mitigation:** Focus on domains with established communities and tooling (not experimental trends)

**Risk:** May overlap with Library or Concept categories
→ **Mitigation:** Apply strict scope test - domains are application areas, not technologies or patterns

**Trade-off:** Manual curation is slower than automation
→ **Accepted:** Quality and thoughtfulness are more important than speed for taxonomy expansion

## Migration Plan

Not applicable - this is an additive change with no breaking changes or migrations needed.

## Open Questions

None - approach is straightforward based on Library expansion experience.
