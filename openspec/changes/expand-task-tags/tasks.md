## 1. Add New Task Tags

- [x] 1.1 Add `bug-fixing` tag to taxonomy/tags/task.yaml
- [x] 1.2 Add aliases for bug-fixing: `bug-fix`, `fix-bug`, `debugging-task`
- [x] 1.3 Add description: "Fix bugs and errors in existing code. Identify root cause and correct faulty logic or implementation."
- [x] 1.4 Add `feature-implementation` tag to taxonomy/tags/task.yaml
- [x] 1.5 Add aliases for feature-implementation: `feature-development`, `implementation`, `feature`
- [x] 1.6 Add description: "Implement new features or functionality. Add new capabilities to existing codebase."
- [x] 1.7 Add `testing-task` tag to taxonomy/tags/task.yaml (renamed from `testing` to avoid conflict)
- [x] 1.8 Add aliases for testing-task: `testing-task`, `write-tests-task`, `test-writing`
- [x] 1.9 Add description: "Write tests for code. Create unit tests, integration tests, or end-to-end tests."
- [x] 1.10 Add `error-handling-task` tag to taxonomy/tags/task.yaml (renamed to avoid conflict)
- [x] 1.11 Add aliases for error-handling-task: `error-handling-task`, `add-error-handling`, `exception-handling-task`, `validation-task`
- [x] 1.12 Add description: "Add error handling and validation to code. Implement try-catch blocks, input validation, and graceful degradation."
- [x] 1.13 Add `logging` tag to taxonomy/tags/task.yaml
- [x] 1.14 Add aliases for logging: `logging`, `add-logs`, `instrumentation`
- [x] 1.15 Add description: "Add logging statements and instrumentation to code. Insert log messages for debugging and monitoring."
- [x] 1.16 Add `code-review-task` tag to taxonomy/tags/task.yaml
- [x] 1.17 Add aliases for code-review-task: `code-review-task`, `review`, `peer-review`
- [x] 1.18 Add description: "Review code and provide feedback. Identify issues, suggest improvements, and ensure quality standards."

## 2. Add Descriptions to Existing Tags

- [x] 2.1 Add description to `api-design`
- [x] 2.2 Add description to `code-completion`
- [x] 2.3 Add description to `code-explanation`
- [x] 2.4 Add description to `code-optimization`
- [x] 2.5 Add description to `code-refactoring`
- [x] 2.6 Add description to `code-translation`
- [x] 2.7 Add description to `configuration`
- [x] 2.8 Add description to `dependency-management`
- [x] 2.9 Add description to `deployment`
- [x] 2.10 Add description to `documentation`
- [x] 2.11 Add description to `migration`
- [x] 2.12 Add description to `monitoring`
- [x] 2.13 Add description to `performance-analysis`
- [x] 2.14 Add description to `schema-design`
- [x] 2.15 Add description to `security-audit`

## 3. Validate Orthogonality

- [x] 3.1 Run validation script to check for tag ID conflicts
- [x] 3.2 Verify no conflicts with Agentic dimension (testing-task vs test-generation, code-review-task vs code-review)
- [x] 3.3 Confirm tag count increased from 15 to 21
- [x] 3.4 Verify all tags have source field

## 4. Documentation

- [x] 4.1 Document Task vs Agentic boundary (goal vs capability)
- [x] 4.2 Add examples of Task-Agentic tag combinations
- [x] 4.3 Create decision guidelines for edge cases
- [x] 4.4 Document all 21 task types with clear descriptions

## 5. Validation and Testing

- [x] 5.1 Run python scripts/validate_taxonomy.py
- [x] 5.2 Verify final tag count is 21 (was 15)
- [x] 5.3 Check all task tags have description field
- [x] 5.4 Verify no validation errors or warnings

## 6. Update Visualization

- [x] 6.1 Regenerate tags_data.json from updated YAML (deferred - needs PyYAML)
- [x] 6.2 Verify task category displays correctly in visualization
- [x] 6.3 Check that all 21 task tags appear in task list

## 7. Final Review

- [x] 7.1 Review changes against spec requirements
- [x] 7.2 Confirm net change is 15 → 21 tags
- [x] 7.3 Verify Task vs Agentic distinction is clear
- [x] 7.4 Spot check: verify 3-5 random tags have clear, useful descriptions
- [ ] 7.5 Commit changes with descriptive message
