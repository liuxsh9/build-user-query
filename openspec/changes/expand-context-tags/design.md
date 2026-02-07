## Context

Current Context taxonomy has 9 tags covering code organization granularity:
- `single-function` - Complete, runnable function
- `single-file` - Complete file with imports and structure
- `multi-file` - Cross-file changes
- `module` - Module/package level
- `repository` - Repository level

**Gap**: No tag for code fragments smaller than complete functions (snippets from docs, tutorials, Q&A sites).

## Goals / Non-Goals

**Goals:**
- Add `snippet` tag to represent code fragments/incomplete code units
- Complete the granularity spectrum from snippet to repository
- Enable classification of tutorial/documentation code samples
- Maintain orthogonality with other dimensions

**Non-Goals:**
- Not adding multiple snippet types (keep simple)
- Not adding other context dimensions (interface types, deployment targets, etc.)
- Not changing existing 9 tags

## Decisions

### Decision 1: Add `snippet` as the smallest granularity

**Choice:** Add `snippet` tag below `single-function` in the granularity hierarchy

**Alternatives:**
- A) Don't add, consider snippets as `single-function`
- B) **Add `snippet` as distinct granularity** ✓
- C) Add multiple snippet types (expression, statement, block)

**Rationale:**
- Snippets are fundamentally different from complete functions:
  - **Complete function**: Has signature, full implementation, can be run/tested independently
  - **Snippet**: May lack context, imports, or full structure; often for illustration
- Common in training data: StackOverflow answers, documentation examples, tutorial code
- Distinction matters for task generation and evaluation

**Definition criteria:**
- Snippet: < complete function (few lines, may lack context)
- Single-function: Complete, runnable function with signature and body
- Single-file: Complete file with imports, multiple functions/classes

### Decision 2: Use "snippet" over alternatives

**Choice:** Use `snippet` as the tag ID and name

**Alternatives:**
- `snippet` ✓
- `code-fragment`
- `code-sample`
- `example`

**Rationale:**
- "Snippet" is universally understood in programming contexts
- Shorter and more common than "code-fragment"
- More specific than "example" or "sample"
- Aligns with IDE features ("insert snippet", "code snippets")

### Decision 3: Aliases for searchability

**Choice:** Include aliases: `snippet`, `code-snippet`, `fragment`, `example`

**Rationale:**
- `code-snippet` - Common full form
- `fragment` - Technical synonym
- `example` - Common in documentation context
- Maximizes searchability while keeping primary ID simple

### Decision 4: Keep Context focused on organization

**Choice:** Only add `snippet`, no other context expansions

**Rationale:**
- Maintains Context dimension focus: "code organization structure"
- Other characteristics covered by tag combinations:
  - Test code: `Task(testing)` + `Context(single-function)`
  - Config file: `Task(configuration)` + `Context(single-file)`
  - CLI tool: `Domain(cli)` + `Context(module)`
- Preserves orthogonality and simplicity

### Decision 5: Placement in granularity spectrum

**Choice:** snippet < single-function < single-file < multi-file < module < repository

**Rationale:**
- Clear hierarchy by scope size
- snippet is explicitly the smallest unit
- No ambiguity in classification

## Risks / Trade-offs

### Risk 1: Overlap with single-function
**Risk:** Unclear boundary between snippet and single-function

**Examples:**
- Simple one-liner function - snippet or single-function?
- Function without docstring - snippet or single-function?

**Mitigation:**
- Clear definition: snippet = **incomplete/lacks context**, function = **complete/runnable**
- Decision rule: Can it run independently? → function. Needs context? → snippet
- Document examples in spec

### Risk 2: Subjectivity in classification
**Risk:** Different annotators may classify the same code differently

**Mitigation:**
- Objective criteria: "Has function signature and can be executed independently" → single-function
- "Missing imports, incomplete, or illustrative only" → snippet
- Provide clear examples in documentation

### Risk 3: Minimal impact
**Risk:** Only adding 1 tag, limited value for effort

**Impact assessment:**
- Small change (1 tag), low implementation cost
- High conceptual value: completes granularity spectrum
- Important for documentation/tutorial data classification
- **Proceed**: value justifies minimal effort

## Implementation Plan

1. Add `snippet` tag to `taxonomy/tags/context.yaml`
2. Define aliases and description
3. Run validation (no conflicts expected)
4. Update visualization
5. Document classification guidelines with examples
