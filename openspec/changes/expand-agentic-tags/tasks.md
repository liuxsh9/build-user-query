## 1. Validate Current Agentic Tags

- [ ] 1.1 Review existing 19 Agentic tags for completeness
- [ ] 1.2 Verify no duplicates or overlaps in current tags
- [ ] 1.3 Confirm current tags align with taxonomy schema
- [ ] 1.4 Run validation to establish baseline

## 2. Add Search Capabilities (2 tags)

- [ ] 2.1 Add file-search tag (Glob, find)
  - ID: file-search
  - Name: File Search
  - Aliases: glob, find, path-search
  - Description: Search files by path, name, extension patterns
- [ ] 2.2 Add code-search tag (Grep, ripgrep)
  - ID: code-search
  - Name: Code Search
  - Aliases: grep, content-search, text-search
  - Description: Search code by content using regex/patterns
- [ ] 2.3 Validate search tags don't conflict with file-navigation

## 3. Add Interaction & Coordination Capabilities (4 tags)

- [ ] 3.1 Add user-interaction tag
  - ID: user-interaction
  - Aliases: ask-user, user-input, confirmation
  - Claude Code: AskUserQuestion tool
- [ ] 3.2 Add subagent-management tag
  - ID: subagent-management
  - Aliases: spawn-agent, delegate-task, agent-coordination
  - Claude Code: Task tool
- [ ] 3.3 Add parallel-execution tag
  - ID: parallel-execution
  - Aliases: concurrent, parallel-tasks
- [ ] 3.4 Add task-tracking tag
  - ID: task-tracking
  - Aliases: todo-management, progress-tracking
  - Claude Code: TaskCreate, TaskUpdate tools

## 4. Add Planning & Extensibility Capabilities (2 tags)

- [ ] 4.1 Add planning tag
  - ID: planning
  - Aliases: task-planning, design, architecture
  - Claude Code: EnterPlanMode tool
- [ ] 4.2 Add skill-execution tag
  - ID: skill-execution
  - Aliases: plugin, command, mcp
  - Claude Code: Skill tool, MCP integration

## 5. Add Code Intelligence Capabilities (6 tags)

- [ ] 5.1 Add code-analysis tag
  - ID: code-analysis
  - Aliases: ast-analysis, code-understanding, dependency-analysis
  - Includes: AST parsing, symbol lookup, call graphs
- [ ] 5.2 Add code-generation tag
  - ID: code-generation
  - Aliases: code-gen, scaffolding, boilerplate
- [ ] 5.3 Add refactoring tag
  - ID: refactoring
  - Aliases: code-refactor, restructure
- [ ] 5.4 Add documentation-generation tag
  - ID: documentation-generation
  - Aliases: doc-gen, api-docs, comments
- [ ] 5.5 Add test-generation tag
  - ID: test-generation
  - Aliases: test-gen, unit-test-gen
- [ ] 5.6 Add code-review tag
  - ID: code-review
  - Aliases: pr-review, code-quality, style-check

## 6. Add Quality & Debugging Capabilities (2 tags)

- [ ] 6.1 Add static-analysis tag
  - ID: static-analysis
  - Aliases: linting, type-check, security-scan
  - Includes: ESLint, Pylint, type checking, SAST
- [ ] 6.2 Add debugging tag
  - ID: debugging
  - Aliases: debug, log-analysis, diagnostics
  - Includes: Interactive debugging, log parsing, error diagnosis

## 7. Add Multimodal Capabilities (5 tags)

- [ ] 7.1 Add visual-understanding tag
  - ID: visual-understanding
  - Aliases: screenshot-analysis, diagram-reading, image-understanding
  - Use cases: UI screenshots, UML diagrams, architecture diagrams
- [ ] 7.2 Add diagram-generation tag
  - ID: diagram-generation
  - Aliases: diagram-gen, mermaid, plantuml
  - Tools: Mermaid, PlantUML, Graphviz
- [ ] 7.3 Add ui-automation tag
  - ID: ui-automation
  - Aliases: browser-automation, gui-testing, e2e-testing
  - Tools: Playwright, Selenium, Puppeteer
- [ ] 7.4 Add design-to-code tag
  - ID: design-to-code
  - Aliases: figma-to-code, sketch-to-html
- [ ] 7.5 Add visual-debugging tag
  - ID: visual-debugging
  - Aliases: visual-regression, ui-diff, layout-debugging

## 8. Update Taxonomy Schema (if needed)

- [ ] 8.1 Check if taxonomy.yaml needs updates for Agentic category
- [ ] 8.2 Add any new metadata fields if required
- [ ] 8.3 Update validation script for new tag patterns

## 9. Validate New Tags

- [ ] 9.1 Run full taxonomy validation
- [ ] 9.2 Verify total Agentic tag count (19 → 38)
- [ ] 9.3 Check for alias conflicts across all categories
- [ ] 9.4 Verify orthogonality (no overlaps with existing 19 tags)
- [ ] 9.5 Validate all new tags have proper aliases
- [ ] 9.6 Check descriptions are clear and distinct

## 10. Update Documentation & Integration

- [ ] 10.1 Update scripts/generate_tags_data.py to include new tags
- [ ] 10.2 Update visualization HTML (all 3 versions)
- [ ] 10.3 Generate updated tags statistics
- [ ] 10.4 Update README.md with new Agentic counts
- [ ] 10.5 Create AGENTIC_EXPANSION_REPORT.md documenting changes
- [ ] 10.6 Verify visualization displays all 38 tags correctly

## 11. Testing & Validation

- [ ] 11.1 Test each new tag category independently
- [ ] 11.2 Verify Claude Code tool mapping is complete
- [ ] 11.3 Check multimodal tags are well-defined
- [ ] 11.4 Validate no semantic overlaps between tags
- [ ] 11.5 Review aliases for completeness
- [ ] 11.6 Final validation run (0 errors expected)
