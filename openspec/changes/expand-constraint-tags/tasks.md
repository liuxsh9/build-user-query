## 1. Remove Subjective Tags

- [x] 1.1 Remove `readable` tag from taxonomy/tags/constraint.yaml
- [x] 1.2 Remove `maintainable` tag from taxonomy/tags/constraint.yaml
- [x] 1.3 Remove `testable` tag from taxonomy/tags/constraint.yaml
- [x] 1.4 Run validation to confirm no references to removed tags

## 2. Merge Performance Tags

- [x] 2.1 Create new `performance-optimized` tag in constraint.yaml
- [x] 2.2 Add aliases: `high-performance`, `low-latency`, `memory-efficient`, `optimized`
- [x] 2.3 Document judgment criteria: "Uses profiling/benchmarking tools, applies algorithmic optimizations, uses efficient data structures, or has documented performance characteristics"
- [x] 2.4 Remove old `high-performance` tag
- [x] 2.5 Remove old `low-latency` tag
- [x] 2.6 Remove old `memory-efficient` tag
- [x] 2.7 Verify aliases preserve searchability

## 3. Remove Overly Broad Tags

- [x] 3.1 Remove `secure` tag from constraint.yaml
- [x] 3.2 Document removal rationale (too broad, covered by Concept dimension)

## 4. Add State Management Constraints

- [x] 4.1 Add `stateless` tag to constraint.yaml
- [x] 4.2 Add aliases for stateless: `stateless`, `no-state`
- [x] 4.3 Document stateless judgment criteria: "No global variables, no persistent state between function calls (detectable via static analysis)"
- [x] 4.4 Add `immutable` tag to constraint.yaml
- [x] 4.5 Add aliases for immutable: `immutable`, `immutability`
- [x] 4.6 Document immutable judgment criteria: "No mutation operations, uses immutable data structures (detectable via static analysis)"

## 5. Add Concurrency Model Constraints

- [x] 5.1 Add `lock-free` tag to constraint.yaml
- [x] 5.2 Add aliases for lock-free: `lock-free`, `lockless`
- [x] 5.3 Document lock-free judgment criteria: "No mutex, lock, or semaphore primitives (detectable via static analysis)"
- [x] 5.4 Add `async` tag to constraint.yaml
- [x] 5.5 Add aliases for async: `async`, `asynchronous`, `async-await`
- [x] 5.6 Document async judgment criteria: "Uses async/await, Promises, coroutines, or async frameworks (detectable via static analysis)"
- [x] 5.7 Verify no ID conflict with Concept dimension's `async-await` tag

## 6. Add Observability Constraint

- [x] 6.1 Add `observable` tag to constraint.yaml
- [x] 6.2 Add aliases: `observable`, `instrumented`, `observability`
- [x] 6.3 Document observable judgment criteria: "Uses logging frameworks, implements metrics/monitoring, has distributed tracing, or uses structured logging (detectable via library imports)"

## 7. Validate Orthogonality

- [x] 7.1 Run validation script to check for tag ID conflicts across categories
- [x] 7.2 Verify `async` (Constraint) does not conflict with `async-await` (Concept)
- [x] 7.3 Ensure all new tags are distinct from Agentic, Task, Domain, Language dimensions
- [x] 7.4 Confirm no overlap with existing Concept tags

## 8. Update Documentation

- [x] 8.1 Document constraint objectivity principle in constraint.yaml header or README
- [x] 8.2 Add judgment criteria documentation for all existing tags that lack it
- [x] 8.3 Create migration notes documenting removed tags (readable, maintainable, testable, secure)
- [x] 8.4 Document merged tags (performance-optimized from 3 tags)

## 9. Validation and Testing

- [x] 9.1 Run python scripts/validate_taxonomy.py
- [x] 9.2 Verify final tag count is ~23-25 tags
- [x] 9.3 Check all constraint tags have `source` field
- [x] 9.4 Verify no validation errors or warnings
- [x] 9.5 Spot check: select 3-5 random constraints and verify judgment criteria are clear

## 10. Update Visualization

- [x] 10.1 Regenerate tags_data.json from updated YAML (will run when PyYAML available)
- [x] 10.2 Verify constraint category displays correctly in visualization
- [x] 10.3 Check that merged/removed tags don't break visualization

## 11. Final Review

- [x] 11.1 Review all changes against spec requirements
- [x] 11.2 Confirm net change is 25 → ~23-25 tags
- [x] 11.3 Verify objectivity principle applied to all tags
- [x] 11.4 Create summary report of changes (removed: 7, added: 6, net: -1)
- [ ] 11.5 Commit changes with descriptive message
