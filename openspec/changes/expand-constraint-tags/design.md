## Context

Current Constraint taxonomy has 25 tags representing non-functional requirements. However, the core purpose of this taxonomy is data annotation and gap detection - tags must be objectively verifiable through rules/tools/tests.

**Current Problems:**
- Subjective tags (`readable`, `maintainable`, `testable`) cannot be evaluated systematically
- Redundant performance tags (`high-performance`, `low-latency`, `memory-efficient`) measure similar aspects
- Overly broad tags (`secure`) are too vague to be useful for classification
- Missing important objective constraints (state management, concurrency models, observability)

**Core Principle:** Every constraint tag must answer "How do we determine if code has this property?" with a clear, objective rule.

## Goals / Non-Goals

**Goals:**
- Establish objectivity as the core design principle for Constraint tags
- Remove all subjective/non-judgeable tags
- Consolidate redundant tags measuring similar properties
- Add missing objective constraints for modern software patterns
- Maintain ~25 tag count (quality over quantity)
- Ensure all tags are orthogonal and independently verifiable

**Non-Goals:**
- Not adding every possible constraint - only those with clear judgment rules
- Not creating fine-grained constraints - maintain coarse granularity
- Not framework-specific constraints (keep generic where possible)
- Not overlapping with Concept/Agentic/Task dimensions

## Decisions

### Decision 1: Objectivity as Core Requirement

**Choice:** Require explicit judgment criteria for every constraint tag

**Alternatives:**
- A) Keep subjective tags, rely on human judgment
- B) Mixed approach - allow some subjective tags with guidelines
- C) **Strict objectivity requirement** ✓

**Rationale:**
- Data annotation cannot scale with subjective judgment
- Gap detection requires deterministic classification
- Objective criteria enable automated tooling

**Judgment Criteria Types:**
- Static analysis (code structure detection)
- Dynamic testing (behavior verification)
- Tool-based measurement (metrics, benchmarks)
- Checklist validation (compliance standards)

### Decision 2: Remove Subjective Tags

**Choice:** Remove `readable`, `maintainable`, `testable`

**Rationale:**
- `readable` - Highly subjective, varies by developer preference
- `maintainable` - No objective metric, composite of many factors
- `testable` - Ambiguous (has tests? or easy to test?), overlaps with Concept

**Alternative considered:** Define metrics (cyclomatic complexity for readability)
**Rejected because:** Metrics don't capture full meaning, better to remove entirely

### Decision 3: Merge Performance Tags

**Choice:** Merge `high-performance`, `low-latency`, `memory-efficient` → `performance-optimized`

**Alternatives:**
- A) Keep separate tags for each performance dimension
- B) Remove all performance tags (too subjective)
- C) **Merge into single tag with multi-dimensional criteria** ✓

**Rationale:**
- All measure optimization aspects (time, space, latency)
- Judgment rule: Has performance benchmarks/profiling or uses optimization techniques
- Single tag reduces redundancy while maintaining usefulness
- Aliases preserve searchability

**Judgment criteria:**
- Uses profiling/benchmarking tools
- Applies algorithmic optimizations (memoization, caching)
- Uses efficient data structures
- Has documented performance characteristics

### Decision 4: Remove `secure` Tag

**Choice:** Remove overly broad `secure`, replace with specific verifiable constraints if needed

**Alternatives:**
- A) Keep `secure` as general marker
- B) **Remove and use specific constraints** ✓
- C) Keep and add specific constraints

**Rationale:**
- "Secure" is too broad - encompasses encryption, auth, input validation, etc.
- Cannot objectively verify "is this code secure?"
- Specific constraints (like `input-validated`, `encrypted`) are verifiable
- Concept dimension already has `security`, `authentication`, `encryption`

**Decision:** Don't add specific security constraints in this change (avoid overlap with Concept)

### Decision 5: Add State Management Constraints

**Choice:** Add `stateless` and `immutable`

**Judgment criteria:**
- `stateless`: No global variables, no persistent state between calls
- `immutable`: No mutation operations, uses immutable data structures

**Rationale:**
- Common architectural patterns with clear definitions
- Easily verifiable through static analysis
- Important for distributed systems and functional programming

### Decision 6: Add Concurrency Constraints

**Choice:** Add `lock-free` and `async`

**Judgment criteria:**
- `lock-free`: No mutex/lock primitives used
- `async`: Uses async/await, Promises, coroutines, or async frameworks

**Rationale:**
- Distinct concurrency models with clear patterns
- Easily detectable through code analysis
- `async` already appears in Concept (`async-await`) - **NEED TO VERIFY NO CONFLICT**

**Risk:** Potential overlap with Concept dimension
**Mitigation:** Constraint = "code IS async", Concept = "knowledge OF async/await patterns"

### Decision 7: Add Observability Constraint

**Choice:** Add `observable` / `instrumented`

**Judgment criteria:**
- Uses logging frameworks
- Implements metrics/monitoring (Prometheus, StatsD)
- Has distributed tracing (OpenTelemetry, Jaeger)
- Structured logging with correlation IDs

**Rationale:**
- Critical for production systems
- Objectively verifiable (check for logging/metrics libraries)
- Not covered by existing tags

### Decision 8: Selective Addition of New Constraints

**Choice:** Add only high-value, clearly verifiable constraints

**Included:**
- `stateless`, `immutable` (state management)
- `lock-free`, `async` (concurrency)
- `observable` (observability)

**Considered but excluded:**
- `bounded-resource` - Too vague (what resource? what bound?)
- `zero-downtime` - Deployment property, not code property
- `input-validated` - Too specific, overlaps with security concept
- `encrypted` - Too specific, overlaps with encryption concept

**Rationale:** Keep count manageable, avoid edge cases

### Decision 9: Granularity - Coarse Over Fine

**Choice:** Maintain coarse-grained constraints

**Examples:**
- `performance-optimized` (not separate time/space/latency)
- `observable` (not separate logging/metrics/tracing)
- Keep domain-specific tags (`gas-optimized`, `misra-c-compliant`) for specialized use

**Rationale:**
- Consistency with Agentic dimension approach
- Avoid tag explosion
- Tags are composable - can use multiple on same code

## Risks / Trade-offs

### Risk 1: Overlap with Concept Dimension
**Risk:** `async` constraint vs `async-await` concept may confuse users

**Mitigation:**
- Clear semantic distinction: Constraint = property of code, Concept = knowledge domain
- Document difference: "async" tag means code IS asynchronous, "async-await" means code DEMONSTRATES async/await pattern
- Validation to ensure no ID conflicts

### Risk 2: Judgment Criteria May Still Be Subjective
**Risk:** Some "objective" criteria may require interpretation

**Example:** What qualifies as "performance-optimized"?

**Mitigation:**
- Document judgment rules explicitly in spec
- Focus on detectable patterns (uses profiling tools, optimization libraries)
- Accept some gray area - better than purely subjective tags

### Risk 3: Loss of Useful Subjective Tags
**Risk:** Developers may want `readable` or `maintainable` tags

**Mitigation:**
- These concepts still exist in Concept dimension
- Focus shifted to objective criteria for data annotation
- Can add back if objective metrics emerge (e.g., tooling consensus)

### Risk 4: Tag Count Reduction May Limit Coverage
**Risk:** Removing tags reduces expressiveness

**Impact:** 25 → ~23 tags (net -2)

**Mitigation:**
- Removed tags were low-value (subjective/redundant)
- Quality over quantity - remaining tags are more useful
- Can expand later if objective constraints identified

## Implementation Phases

### Phase 1: Remove Subjective Tags
- Remove `readable`, `maintainable`, `testable` from constraint.yaml
- Update validation to check for subjectivity

### Phase 2: Merge Performance Tags
- Merge into `performance-optimized`
- Preserve aliases for backward compatibility
- Document judgment criteria

### Phase 3: Remove Broad Tags
- Remove `secure`
- Document why removed in migration notes

### Phase 4: Add New Constraints
- Add `stateless`, `immutable`, `lock-free`, `async`, `observable`
- Document judgment criteria for each
- Validate no conflicts with other dimensions

### Phase 5: Validation & Documentation
- Run taxonomy validation
- Update constraint design documentation
- Create spec with judgment criteria
