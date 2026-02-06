## Why

Current Agentic taxonomy has 19 tags covering basic agent capabilities (file operations, code execution, external integrations), but lacks coverage for modern coding agent capabilities essential for tools like Claude Code, OpenCode, and other agentic coding frameworks. Critical gaps include:

- **Search capabilities**: No distinction between file path search (Glob) vs content search (Grep)
- **User interaction**: Missing ability to request user decisions/confirmations
- **Agent coordination**: No support for subagent management, parallel execution
- **Planning**: Missing task planning and architecture design capabilities
- **Code understanding**: No code analysis, AST parsing, dependency analysis
- **Code generation**: Missing automated code generation, refactoring, test generation
- **Multimodal**: No visual understanding, diagram generation, UI automation
- **Advanced tooling**: Missing skill/plugin execution, static analysis, debugging

## What Changes

- Expand Agentic tags from 19 to 38 tags (2x growth)
- Add search capabilities: file-search, code-search (Glob vs Grep distinction)
- Add user interaction: user-interaction
- Add agent coordination: subagent-management, parallel-execution
- Add planning & extensibility: planning, skill-execution
- Add code intelligence: code-analysis, code-generation, refactoring
- Add quality & testing: test-generation, documentation-generation, code-review, static-analysis, debugging
- Add multimodal capabilities: visual-understanding, diagram-generation, ui-automation, design-to-code, visual-debugging
- Add project management: task-tracking

## Capabilities

### New Capabilities
All 19 new tags are new capabilities - no modifications to existing tags needed.

**Search & Discovery (2):**
- `file-search`: Pattern-based file path search (Glob, find)
- `code-search`: Content-based code search (Grep, ripgrep)

**Interaction & Coordination (4):**
- `user-interaction`: Request user decisions/confirmations
- `subagent-management`: Spawn/manage sub-agents
- `parallel-execution`: Execute multiple tasks concurrently
- `task-tracking`: Track TODO items and progress

**Planning & Extensibility (2):**
- `planning`: Task planning and architecture design
- `skill-execution`: Execute predefined skills/plugins (MCP)

**Code Intelligence (6):**
- `code-analysis`: AST parsing, symbol lookup, dependency analysis
- `code-generation`: Generate new code from templates/requirements
- `refactoring`: Restructure code while preserving semantics
- `documentation-generation`: Generate API docs and comments
- `test-generation`: Generate unit/integration tests
- `code-review`: PR review, style checking, best practices

**Quality & Debugging (2):**
- `static-analysis`: Linting, type checking, security scanning
- `debugging`: Interactive debugging and log analysis

**Multimodal (5):**
- `visual-understanding`: Analyze screenshots, diagrams, designs
- `diagram-generation`: Generate architecture/flow diagrams
- `ui-automation`: Browser automation, GUI testing
- `design-to-code`: Convert designs to code implementation
- `visual-debugging`: Visual regression testing, UI debugging

### Modified Capabilities
None - all existing 19 tags remain unchanged.

## Impact

- Increases Agentic tags from 19 to 38 (2x growth, 100% increase)
- Enables comprehensive coverage of modern coding agent capabilities
- Supports Claude Code tool mapping (Read/Write/Edit/Bash/Grep/Glob/Task/Skill/AskUserQuestion)
- Enables multimodal coding workflows (screenshot analysis, diagram generation, UI automation)
- Provides foundation for advanced SFT query generation with agent capabilities
- Maintains orthogonality with existing 19 tags (no overlap or conflicts)
- No breaking changes to existing taxonomy structure
