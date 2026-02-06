## Context

Current Agentic taxonomy has 19 tags organized into 4 groups:
- **File Operations (4)**: file-read, file-write, file-edit, file-navigation
- **Code Execution (4)**: code-execution, build-execution, test-running, bash-execution
- **External Integration (5)**: api-calling, database-query, web-search, git-operations, dependency-installation
- **Coordination & Reasoning (6)**: multi-step-reasoning, multi-file-coordination, iterative-refinement, context-management, tool-selection, error-recovery

**Gaps identified:**
1. Search capabilities conflated with navigation (file-navigation doesn't cover Glob/Grep)
2. No user interaction capabilities (AskUserQuestion in Claude Code)
3. No subagent management (Task tool in Claude Code)
4. No planning mode support
5. No code intelligence (analysis, generation, refactoring)
6. No multimodal capabilities (visual understanding, diagram generation)
7. No quality tools (static analysis, code review, debugging)
8. No extensibility (skills, plugins, MCP)

Target: Expand to 38 tags (19 new) covering modern coding agent capabilities while maintaining orthogonality.

## Goals / Non-Goals

**Goals:**
- Cover Claude Code tool capabilities (Grep, Glob, Task, Skill, AskUserQuestion, EnterPlanMode)
- Add multimodal capabilities for visual coding workflows
- Enable code intelligence (analysis, generation, refactoring)
- Support quality assurance (testing, review, static analysis)
- Maintain coarse granularity (code-analysis instead of ast-analysis + symbol-lookup + ...)
- Ensure orthogonality with existing 19 tags
- Use framework-agnostic terminology

**Non-Goals:**
- Framework-specific tags (e.g., "claude-code-tools", "opencode-capabilities")
- Fine-grained splits (e.g., separate ast-analysis, symbol-lookup, dependency-graph)
- Version-specific capabilities (e.g., "gpt-4-vision" vs "claude-vision")
- Platform-specific tools (e.g., "github-copilot", "cursor-ai")

## Decisions

### Decision 1: Keep file-search and code-search separate

**Choice:** Maintain two distinct search tags instead of merging into generic "search"

**Rationale:**
- **file-search**: Search by file metadata (path, name, extension) - maps to Glob, find
  - Output: List of file paths
  - Use case: "Find all .ts files in src/"
- **code-search**: Search by file content (code, text) - maps to Grep, ripgrep
  - Output: Matching code snippets with line numbers
  - Use case: "Find all functions calling authenticate()"
- **Fundamental difference**: Metadata search vs content search
- **Different tools**: Glob/find vs Grep/ripgrep/ag
- **Different SFT patterns**: Path patterns vs regex patterns

**Alternatives considered:**
- Single "search" tag: Too coarse, loses important semantic distinction
- Three tags (file-search, code-search, semantic-search): Too fine for current needs

### Decision 2: Include planning as Agentic capability

**Choice:** Add "planning" tag to Agentic category

**Rationale:**
- Planning is a core agent capability, not a task type
- Maps to Claude Code's Plan mode (EnterPlanMode tool)
- Distinct from multi-step-reasoning:
  - planning: Upfront design and task breakdown
  - multi-step-reasoning: Execution-time step-by-step thinking
- Essential for complex implementations requiring design-before-code

**Alternatives considered:**
- Put in Task category: Doesn't fit - Task is about what to do, Agentic is about how
- Put in Concept category: Too abstract - this is a concrete agent action

### Decision 3: Coarse-grained code intelligence tags

**Choice:** Use broad tags (code-analysis, code-generation) instead of fine-grained splits

**Examples of coarseness:**
- **code-analysis** includes: AST parsing, symbol lookup, dependency analysis, call graphs
- **code-generation** includes: Template expansion, scaffolding, boilerplate generation
- **refactoring** includes: Rename, extract function, inline, optimize structure

**Rationale:**
- Aligns with Language taxonomy approach (coarse granularity)
- Avoids tag explosion (3 broad tags instead of 10+ narrow tags)
- Sufficient for SFT query classification
- Can add finer tags later if needed

**Alternatives considered:**
- Fine-grained: ast-analysis, symbol-lookup, dependency-analysis, call-graph-generation
  - Rejected: Too many tags, overlapping use cases
- Ultra-coarse: code-intelligence (single tag)
  - Rejected: Too broad, loses important distinctions (analysis vs generation)

### Decision 4: Add multimodal capabilities

**Choice:** Add 5 multimodal tags covering visual coding workflows

**Tags:**
1. **visual-understanding**: Analyze screenshots, diagrams, designs, architecture docs
2. **diagram-generation**: Generate Mermaid/PlantUML diagrams (architecture, flow, ER)
3. **ui-automation**: Browser automation (Playwright, Selenium), GUI testing
4. **design-to-code**: Convert Figma/sketches to HTML/React components
5. **visual-debugging**: Visual regression testing, UI diff analysis

**Rationale:**
- Modern LLMs support vision (Claude 3.5, GPT-4V)
- Common coding workflows involve visual artifacts (screenshots, diagrams, designs)
- Differentiates from text-only coding agents
- Growing importance of visual tools in development (Figma, Mermaid, UI testing)

**Alternatives considered:**
- Skip multimodal: Misses important modern capabilities
- Single "visual-capabilities" tag: Too coarse, loses distinctions
- Add audio/video: Out of scope for coding workflows

### Decision 5: Merge log-analysis into debugging

**Choice:** Single "debugging" tag covering interactive debugging and log analysis

**Rationale:**
- Both serve diagnostic purposes
- Often used together (debug with logs)
- Coarse granularity principle
- Avoids similar tags (debugging vs log-analysis)

**Alternatives considered:**
- Separate tags: Too fine-grained, overlapping use cases
- Merge into error-recovery: Different - debugging is diagnostic, recovery is corrective

### Decision 6: Include task-tracking in Agentic

**Choice:** Add task-tracking to Agentic category, not Task category

**Rationale:**
- Task-tracking is an agent self-management capability
- Task category is about task types (implementation, debugging, refactoring)
- Agentic category is about agent capabilities (how agents work)
- Maps to Claude Code's TaskCreate/TaskUpdate tools
- Essential for complex multi-step implementations

**Alternatives considered:**
- Put in Task category: Conceptual mismatch - Task is "what", Agentic is "how"
- Skip entirely: Misses important agent self-organization capability

### Decision 7: Framework-agnostic terminology

**Choice:** Use generic terms (subagent-management, skill-execution) not framework-specific names

**Examples:**
- ✓ subagent-management (not "Task tool", "spawn agent")
- ✓ skill-execution (not "Skill tool", "MCP", "/command")
- ✓ user-interaction (not "AskUserQuestion", "prompt user")
- ✓ planning (not "Plan mode", "EnterPlanMode")

**Rationale:**
- Taxonomy should be tool-agnostic
- Supports multiple frameworks (Claude Code, OpenCode, Cursor, Copilot)
- Future-proof as tools evolve
- Focuses on capability, not implementation

**Alternatives considered:**
- Framework-specific tags: Too narrow, doesn't generalize
- Add framework metadata field: Over-engineering for current needs

### Decision 8: Maintain orthogonality with existing tags

**Choice:** Ensure all 19 new tags are distinct from existing 19 tags

**Orthogonality validation:**
- file-search ≠ file-navigation: search vs browse
- code-search ≠ file-read: find vs read
- subagent-management ≠ multi-step-reasoning: delegate vs reason
- planning ≠ multi-step-reasoning: design vs execute
- code-generation ≠ file-write: intelligent generation vs generic write
- refactoring ≠ file-edit: semantic transform vs text edit
- test-generation ≠ test-running: create tests vs run tests
- debugging ≠ error-recovery: diagnose vs recover
- user-interaction: completely new dimension (human-in-the-loop)

**Alternatives considered:**
- Merge similar tags: Loses important distinctions
- Create hierarchy: Over-engineering, flat structure is simpler

## Risks / Trade-offs

**Risk:** 38 tags may be too many to manage
→ **Mitigation:** Still coarse-grained, well-organized into 10 subcategories, aligns with other categories (Language: 75, Library: 339)

**Risk:** Multimodal capabilities may not apply to all LLMs
→ **Mitigation:** Tags describe capabilities, not requirements - applicable when model supports vision

**Risk:** Code intelligence tags (analysis, generation) may overlap
→ **Mitigation:** Clear definitions - analysis: understand existing code, generation: create new code, refactoring: transform existing code

**Trade-off:** Keeping file-search + code-search adds complexity
→ **Acceptable:** Distinction is meaningful for SFT data labeling (path search vs content search)

**Trade-off:** Multimodal tags add new dimension
→ **Acceptable:** Reflects modern coding workflows, differentiates capabilities

**Risk:** Framework-agnostic naming may be less intuitive
→ **Mitigation:** Clear descriptions and examples in taxonomy, aliases can include tool-specific terms

## Open Questions

- Should we add "notebook-execution" for Jupyter/interactive notebooks?
  - Current thinking: Covered by code-execution, can add later if needed
- Should we distinguish "unit-test-generation" vs "integration-test-generation"?
  - Current thinking: Single test-generation tag is sufficient (coarse granularity)
- Should we add "ai-assistance" for copilot-style inline suggestions?
  - Current thinking: Too vague, covered by code-generation
- Should diagram-generation cover data visualization (charts, graphs)?
  - Current thinking: Yes, include under diagram-generation (architecture diagrams + data viz)
