## Context

Current Task taxonomy has 15 tags representing different programming tasks (code-completion, refactoring, optimization, etc.). However:
- Missing fundamental tasks: bug-fixing, feature-implementation, testing
- No descriptions on any tags (consistency issue after Context dimension added descriptions)
- Potential overlap with Agentic dimension needs clarification

**Task vs Agentic boundary**:
- Task: What the user wants to accomplish (goal/objective)
- Agentic: What capabilities the agent uses (method/ability)

Example: "bug-fixing" (Task) vs "debugging" (Agentic)
- Task: "I want to fix this bug" (user's goal)
- Agentic: "Using debugging capability to locate issue" (agent's method)

## Goals / Non-Goals

**Goals:**
- Add 6 fundamental programming tasks commonly found in training data
- Add descriptions to all 21 tasks (15 existing + 6 new)
- Maintain clear boundary between Task and Agentic dimensions
- Improve metadata completeness and usability

**Non-Goals:**
- Not adding every possible task variant (keep manageable)
- Not duplicating Agentic capabilities (maintain orthogonality)
- Not removing existing tags (only additions and enhancements)

## Decisions

### Decision 1: Add bug-fixing as distinct task

**Choice:** Add `bug-fixing` as a fundamental Task tag

**Alternatives:**
- A) Don't add, use code-optimization or code-refactoring
- B) **Add bug-fixing as distinct task** ✓
- C) Merge with error-handling

**Rationale:**
- Bug-fixing is one of the most common programming tasks
- Distinct from optimization (improving working code) and refactoring (restructuring)
- Training data often contains bug fix examples (before/after)
- Clear user intent: "fix this bug" vs "optimize this code"

**Data characteristics:**
- Input: Broken/incorrect code with error description
- Output: Corrected code
- Different from feature-implementation (adding new) or optimization (improving existing)

### Decision 2: Add feature-implementation task

**Choice:** Add `feature-implementation` tag for implementing new functionality

**Alternatives:**
- A) Don't add, too broad
- B) **Add feature-implementation** ✓
- C) Use more specific tags (api-implementation, ui-implementation, etc.)

**Rationale:**
- Extremely common task type in training data
- Clear distinction: implementing NEW vs modifying EXISTING
- Complements bug-fixing (fix existing) and code-refactoring (restructure existing)
- Broad but useful for classification

**Aliases:** `feature-development`, `implementation`, `feature`

### Decision 3: Add testing task

**Choice:** Add `testing` as a Task, distinct from `test-generation` (Agentic)

**Alternatives:**
- A) Use test-generation from Agentic
- B) **Add testing as Task** ✓
- C) Don't add, not needed

**Rationale:**
- **Task vs Agentic boundary**:
  - `testing` (Task): "I want to write tests for this feature" (user goal)
  - `test-generation` (Agentic): Agent's ability to generate test code
- Training data contains: "write tests for X" → test code
- Clear task type distinct from implementation or debugging

**Clarification:**
- Task describes WHAT user wants to do
- Agentic describes HOW agent accomplishes it
- Same code sample can have both tags

### Decision 4: Add error-handling task

**Choice:** Add `error-handling` for adding error handling/validation

**Rationale:**
- Common code improvement task
- Distinct from bug-fixing (fixing errors) vs adding error handling (preventing errors)
- Training data: "add error handling to this function" → code with try-catch/validation

**Examples:**
- Adding try-catch blocks
- Adding input validation
- Adding error messages and logging
- Graceful degradation

### Decision 5: Add logging task

**Choice:** Add `logging` for adding log statements and instrumentation

**Rationale:**
- Common task distinct from monitoring (Task) and observable (Constraint)
- Training data: "add logging to this function" → code with log.info/debug statements
- Different focus:
  - `logging` (Task): Add log statements to code
  - `monitoring` (Task): Set up monitoring infrastructure
  - `observable` (Constraint): Code HAS logging/metrics

### Decision 6: Add code-review-task

**Choice:** Add `code-review-task` as a Task, distinct from `code-review` (Agentic)

**Alternatives:**
- A) Use code-review from Agentic
- B) **Add code-review-task** ✓
- C) Don't add, overlaps with code-review capability

**Rationale:**
- **Task vs Agentic boundary** (same as testing):
  - `code-review-task` (Task): "Review this code and provide feedback" (goal)
  - `code-review` (Agentic): Agent's capability to perform code review
- Training data: Code → review comments/suggestions
- Distinct task type from implementation or explanation

**Naming:** Use `-task` suffix to avoid ID conflict with Agentic dimension

### Decision 7: Description format and content

**Choice:** Add concise, clear descriptions for all tags

**Format guidelines:**
- Start with what the task accomplishes
- Include typical activities or outputs
- 1-2 sentences maximum
- Focus on objective, not method

**Example:**
```yaml
description: Fix bugs and errors in existing code. Identify root cause and correct faulty logic or implementation.
```

### Decision 8: Maintain orthogonality with Agentic

**Choice:** Task tags describe user goals, not agent capabilities

**Orthogonality principle:**
- Same training data can have BOTH Task and Agentic tags
- Task: What user asked for
- Agentic: What capability agent demonstrated

**Example combinations:**
- Task(bug-fixing) + Agentic(debugging) + Agentic(code-analysis)
- Task(feature-implementation) + Agentic(code-generation) + Agentic(planning)
- Task(testing) + Agentic(test-generation) + Agentic(code-analysis)

## Risks / Trade-offs

### Risk 1: Overlap with Agentic dimension

**Risk:** Confusion between Task and Agentic tags with similar names

**Examples:**
- `testing` (Task) vs `test-generation` (Agentic)
- `code-review-task` (Task) vs `code-review` (Agentic)

**Mitigation:**
- Clear documentation of Task vs Agentic boundary
- Naming convention: use `-task` suffix when needed
- Examples showing both tags can coexist

### Risk 2: Task granularity

**Risk:** Tasks might be too broad (feature-implementation) or too specific (logging)

**Mitigation:**
- Focus on common, distinguishable task types
- Use aliases to cover variations
- Can refine later if data shows need

### Risk 3: Subjectivity in classification

**Risk:** Some code changes could be classified as multiple tasks

**Example:** "Add validation to prevent crashes" - bug-fixing or error-handling?

**Mitigation:**
- Provide clear decision guidelines
- Allow multiple task tags when appropriate
- Document edge cases

### Risk 4: Missing descriptions

**Risk:** Inconsistent metadata if some tags lack descriptions

**Mitigation:**
- Add descriptions to ALL tags in this change
- Establish descriptions as required field going forward

## Implementation Plan

1. Add 6 new task tags with complete metadata
2. Add descriptions to all 15 existing tags
3. Review and optimize aliases for all tags
4. Run validation to ensure no conflicts
5. Update documentation with Task vs Agentic guidelines
6. Verify final tag count: 21
