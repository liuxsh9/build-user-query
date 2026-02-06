# Agentic Taxonomy Expansion Report

## Executive Summary
Successfully expanded Agentic taxonomy from 19 to 40 tags (+111%), achieving comprehensive coverage of modern coding agent capabilities including Claude Code tools, multimodal workflows, and advanced code intelligence.

## Expansion Details

### Before & After
- **Existing**: 19 tags
- **New**: 21 tags
- **Total**: 40 tags (+111% growth)

### Category Changes
- **Agentic**: 19 → 40 (+21)
- **Task**: 20 → 15 (-5, moved to Agentic)
- **Concept**: 107 → 106 (-1, moved to Agentic)
- **Net Total**: 651 → 666 (+15 tags)

## New Tags by Category

### 🔍 Search Capabilities (2)
1. **file-search** - Pattern-based file path search
   - Aliases: glob, find, path-search
   - Tools: Glob (Node.js), find (Unix), fd
   - Use case: Find files by path patterns (e.g., "**/*.ts")

2. **code-search** - Content-based code search
   - Aliases: grep, content-search, text-search
   - Tools: Grep, ripgrep, ag (Silver Searcher)
   - Use case: Find code by content (e.g., "function authenticate")

### 💬 Interaction & Coordination (4)
3. **user-interaction** - Request user decisions/confirmations
   - Aliases: ask-user, user-input, confirmation
   - Claude Code: AskUserQuestion tool
   - Use case: Present options, collect preferences

4. **subagent-management** - Spawn/manage specialized agents
   - Aliases: spawn-agent, delegate-task, agent-coordination
   - Claude Code: Task tool
   - Use case: Delegate subtasks to specialized agents

5. **parallel-execution** - Execute multiple tasks concurrently
   - Aliases: concurrent, parallel-tasks
   - Use case: Run independent tasks simultaneously

6. **task-tracking** - Track TODO items and progress
   - Aliases: todo-management, progress-tracking
   - Claude Code: TaskCreate, TaskUpdate tools
   - Use case: Manage complex multi-step workflows

### 📋 Planning & Extensibility (2)
7. **planning** - Task planning and architecture design
   - Aliases: task-planning, design, architecture
   - Claude Code: EnterPlanMode tool
   - Use case: Design implementation before coding

8. **skill-execution** - Execute predefined skills/plugins
   - Aliases: plugin, command, mcp
   - Claude Code: Skill tool, MCP integration
   - Use case: Invoke custom commands and integrations

### 🧬 Code Intelligence (6)
9. **code-analysis** - Code structure analysis (coarse-grained)
   - Aliases: ast-analysis, code-understanding, dependency-analysis
   - Includes: AST parsing, symbol lookup, call graphs, dependency analysis
   - Use case: Understand code structure and relationships

10. **code-generation** - Generate new code
    - Aliases: code-gen, scaffolding, boilerplate
    - Use case: Create code from templates, generate boilerplate

11. **refactoring** - Restructure code preserving semantics
    - Aliases: code-refactor, restructure
    - Use case: Rename, extract function, optimize structure

12. **documentation-generation** - Generate docs and comments
    - Aliases: doc-gen, api-docs, comments
    - Use case: Create API docs, inline comments, README

13. **test-generation** - Generate automated tests
    - Aliases: test-gen, unit-test-gen
    - Use case: Create unit tests, integration tests

14. **code-review** - PR and code quality review
    - Aliases: pr-review, code-quality, style-check
    - Use case: Review PRs, suggest improvements

### 🔬 Quality & Debugging (2)
15. **static-analysis** - Linting and type checking
    - Aliases: linting, type-check, security-scan
    - Tools: ESLint, Pylint, mypy, security scanners
    - Use case: Automated code quality checks

16. **debugging** - Interactive debugging and log analysis
    - Aliases: debug, log-analysis, diagnostics
    - Includes: Breakpoint debugging, log parsing, error diagnosis
    - Use case: Diagnose and fix issues

### 👁️ Multimodal (5)
17. **visual-understanding** - Analyze visual artifacts
    - Aliases: screenshot-analysis, diagram-reading, image-understanding
    - Use case: Understand UI screenshots, architecture diagrams, designs

18. **diagram-generation** - Generate visual diagrams
    - Aliases: diagram-gen, mermaid, plantuml
    - Tools: Mermaid, PlantUML, Graphviz
    - Use case: Create architecture diagrams, flowcharts

19. **ui-automation** - UI testing and automation
    - Aliases: browser-automation, gui-testing, e2e-testing
    - Tools: Playwright, Selenium, Puppeteer
    - Use case: Automated UI testing, browser control

20. **design-to-code** - Convert designs to implementation
    - Aliases: figma-to-code, sketch-to-html
    - Use case: Transform Figma designs to React components

21. **visual-debugging** - Visual UI debugging
    - Aliases: visual-regression, ui-diff, layout-debugging
    - Use case: Visual regression testing, layout diagnosis

## Category Cleanup

### Moved from Task → Agentic (5 tags)
Rationale: These are agent capabilities ("how"), not task types ("what")

- **code-generation**: Capability to generate code
- **code-review**: Capability to review code
- **code-search**: Capability to search code
- **debugging**: Capability to debug
- **test-generation**: Capability to generate tests

Task category now focuses on high-level task types (implementation, deployment, migration), not low-level capabilities.

### Moved from Concept → Agentic (1 tag)
- **refactoring**: Better fit as agent capability than programming concept

## Claude Code Tool Coverage

### Complete Mapping
| Claude Code Tool | Agentic Tag | Status |
|-----------------|-------------|--------|
| Grep | code-search | ✅ |
| Glob | file-search | ✅ |
| Task | subagent-management | ✅ |
| Skill | skill-execution | ✅ |
| AskUserQuestion | user-interaction | ✅ |
| EnterPlanMode | planning | ✅ |
| Read/Write/Edit | file-* (existing) | ✅ |
| Bash | bash-execution (existing) | ✅ |
| WebFetch/WebSearch | api-calling, web-search (existing) | ✅ |

## Design Principles Applied

### 1. Orthogonality ✅
- All 21 new tags are distinct from existing 19 tags
- Clear separation: file-search (metadata) vs code-search (content)
- Distinct roles: subagent-management (delegate) vs multi-step-reasoning (execute)

### 2. Coarse Granularity ✅
- code-analysis combines: AST + symbols + dependencies + call graphs
- debugging combines: interactive debugging + log analysis
- Avoids tag explosion while maintaining semantic clarity

### 3. Framework-Agnostic ✅
- Generic terms: subagent-management (not "Task tool")
- Universal concepts: planning (not "Plan mode")
- Tool-neutral: skill-execution (covers Skill tool, MCP, plugins)

### 4. Multimodal First ✅
- 5 visual capabilities added
- Supports modern LLM vision capabilities
- Differentiates from text-only agents

## Validation Results

```
✅ 0 errors
⚠️  11 warnings (all pre-existing, unrelated to new tags)

Category Orthogonality: ✅ PASS
Tag Uniqueness: ✅ PASS
Schema Compliance: ✅ PASS
Referential Integrity: ✅ PASS
```

## Impact Assessment

### Quantitative
- **Tag count**: 651 → 666 (+15 net, +2.3%)
- **Agentic growth**: 19 → 40 (+111%)
- **Claude Code coverage**: 9/9 core tools mapped (100%)
- **Multimodal coverage**: 5 new visual capabilities

### Qualitative
- **Modern workflows**: Comprehensive multimodal support
- **Agent coordination**: Full subagent management and parallel execution
- **Code intelligence**: Complete analysis/generation/refactoring pipeline
- **Quality tools**: Static analysis, code review, debugging
- **Extensibility**: Skills, plugins, MCP integration

## All 40 Agentic Tags (Organized)

### Existing Capabilities (19)
**File Operations**: file-read, file-write, file-edit, file-navigation
**Code Execution**: code-execution, build-execution, test-running, bash-execution
**External Integration**: api-calling, database-query, web-search, git-operations, dependency-installation
**Coordination**: multi-step-reasoning, multi-file-coordination, iterative-refinement, context-management, tool-selection, error-recovery

### New Capabilities (21)
**Search**: file-search, code-search
**Interaction**: user-interaction, subagent-management, parallel-execution, task-tracking
**Planning**: planning, skill-execution
**Code Intelligence**: code-analysis, code-generation, refactoring, documentation-generation, test-generation, code-review
**Quality**: static-analysis, debugging
**Multimodal**: visual-understanding, diagram-generation, ui-automation, design-to-code, visual-debugging

## Next Steps (Optional)

### Potential Future Additions
If further expansion needed:
- **notebook-execution**: Jupyter/interactive notebook support
- **ai-assistance**: Copilot-style inline suggestions
- **incremental-compilation**: Hot reload, fast feedback loops
- **remote-execution**: Cloud/remote code execution

### Maintenance
- Quarterly review for emerging agent capabilities
- Monitor new Claude Code tools for mapping
- Track multimodal LLM advancements
- Update visualization as taxonomy evolves

## Conclusion

The Agentic taxonomy expansion successfully achieved all objectives:
- ✅ Doubled tag count (19 → 40)
- ✅ Complete Claude Code tool coverage
- ✅ Comprehensive multimodal support
- ✅ Advanced code intelligence capabilities
- ✅ Framework-agnostic design
- ✅ Maintained orthogonality
- ✅ All validations passing

The taxonomy is now production-ready for SFT query generation with state-of-the-art coding agent capabilities.
