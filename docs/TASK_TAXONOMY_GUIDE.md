# Task Taxonomy Guide

## Purpose

Task tags represent **what the user wants to accomplish** - the goal or objective of their request. This is distinct from Agentic tags which represent **what capabilities the agent uses** to accomplish the task.

## Task vs Agentic Boundary

**Key Distinction:**
- **Task (Goal)**: What the user wants to do
- **Agentic (Method)**: What capability/tool the agent uses

**Important**: The same training data sample can have BOTH Task and Agentic tags.

### Examples of Task-Agentic Combinations

**Example 1: Bug Fixing**
- User request: "Fix the bug in this authentication function"
- Task tag: `bug-fixing` (goal: fix bugs)
- Agentic tags: `debugging` (capability: locate issue), `code-analysis` (capability: understand code)

**Example 2: Writing Tests**
- User request: "Write unit tests for this API endpoint"
- Task tag: `testing-task` (goal: write tests)
- Agentic tags: `test-generation` (capability: generate test code), `code-analysis` (capability: understand what to test)

**Example 3: Code Review**
- User request: "Review this pull request"
- Task tag: `code-review-task` (goal: review code)
- Agentic tags: `code-review` (capability: perform review), `static-analysis` (capability: analyze code quality)

**Example 4: Feature Implementation**
- User request: "Implement user authentication"
- Task tag: `feature-implementation` (goal: add new feature)
- Agentic tags: `code-generation` (capability: generate code), `planning` (capability: plan implementation)

## All 21 Task Types

### Development Tasks

**bug-fixing**
- **Purpose**: Fix bugs and errors in existing code
- **Activities**: Identify root cause, correct faulty logic, fix implementation errors
- **Aliases**: bug-fix, fix-bug, debugging-task
- **vs Agentic**: Task = "fix this bug", Agentic = "using debugging capability"

**feature-implementation**
- **Purpose**: Implement new features or functionality
- **Activities**: Add new capabilities, extend existing codebase
- **Aliases**: feature-development, implementation, feature
- **vs bug-fixing**: Implementation adds NEW, bug-fixing corrects EXISTING

**code-completion**
- **Purpose**: Complete partial code or suggest next snippets
- **Activities**: Auto-complete function calls, variable names, code blocks
- **Aliases**: completion, autocomplete

**code-optimization**
- **Purpose**: Optimize code for better performance or efficiency
- **Activities**: Improve algorithms, optimize data structures, reduce resource usage
- **Aliases**: optimization, optimize
- **vs bug-fixing**: Optimization improves WORKING code, bug-fixing corrects BROKEN code

**code-refactoring**
- **Purpose**: Restructure existing code without changing behavior
- **Activities**: Improve code quality, readability, maintainability
- **Aliases**: refactoring, refactor
- **vs feature-implementation**: Refactoring restructures EXISTING, implementation adds NEW

**code-translation**
- **Purpose**: Translate code from one language to another
- **Activities**: Convert between programming languages or paradigms
- **Aliases**: translation, transpilation

### Code Quality Tasks

**testing-task**
- **Purpose**: Write tests for code
- **Activities**: Create unit tests, integration tests, end-to-end tests
- **Aliases**: testing-task, write-tests-task, test-writing
- **vs Concept**: testing-task (Task) = write tests, testing (Concept) = testing knowledge/patterns
- **vs Agentic**: testing-task (Task) = goal to write tests, test-generation (Agentic) = capability to generate tests

**error-handling-task**
- **Purpose**: Add error handling and validation to code
- **Activities**: Implement try-catch blocks, input validation, graceful degradation
- **Aliases**: error-handling-task, add-error-handling, exception-handling-task, validation-task
- **vs bug-fixing**: error-handling-task ADDS handling to PREVENT errors, bug-fixing FIXES existing errors
- **vs Concept**: error-handling-task (Task) = add handling, error-handling (Concept) = error handling patterns

**code-review-task**
- **Purpose**: Review code and provide feedback
- **Activities**: Identify issues, suggest improvements, ensure quality standards
- **Aliases**: code-review-task, review, peer-review
- **vs Agentic**: code-review-task (Task) = goal to review, code-review (Agentic) = capability to perform review

**logging**
- **Purpose**: Add logging statements and instrumentation to code
- **Activities**: Insert log messages for debugging and monitoring
- **Aliases**: logging, add-logs, instrumentation
- **vs monitoring**: logging = add log STATEMENTS, monitoring = set up monitoring INFRASTRUCTURE
- **vs Constraint**: logging (Task) = add logging, observable (Constraint) = code HAS logging

**security-audit**
- **Purpose**: Audit code for security vulnerabilities
- **Activities**: Scan for security issues, recommend fixes
- **Aliases**: security-audit, vulnerability-scan

### Design Tasks

**api-design**
- **Purpose**: Design application programming interfaces
- **Activities**: Define endpoints, request/response formats, API contracts
- **Aliases**: api-design

**schema-design**
- **Purpose**: Design database schemas and data models
- **Activities**: Define tables, relationships, constraints
- **Aliases**: schema-design, data-modeling

### Documentation & Explanation

**documentation**
- **Purpose**: Write documentation for code, APIs, or projects
- **Activities**: Create README files, API docs, inline comments
- **Aliases**: docs, documentation

**code-explanation**
- **Purpose**: Explain how code works
- **Activities**: Describe logic, algorithms, implementation in natural language
- **Aliases**: explanation, explain

### Configuration & Infrastructure

**configuration**
- **Purpose**: Configure software settings and build tools
- **Activities**: Set up environment variables, configuration files
- **Aliases**: config, configuration

**dependency-management**
- **Purpose**: Manage project dependencies and packages
- **Activities**: Add, update, remove external libraries and versions
- **Aliases**: dependencies

**deployment**
- **Purpose**: Deploy applications to production or staging
- **Activities**: Set up deployment pipelines and infrastructure
- **Aliases**: deploy, deployment

**monitoring**
- **Purpose**: Set up monitoring and observability for applications
- **Activities**: Configure metrics, alerts, dashboards
- **Aliases**: monitoring, observability
- **vs logging**: monitoring = infrastructure setup, logging = add statements

### Maintenance Tasks

**migration**
- **Purpose**: Migrate code to newer versions, frameworks, or platforms
- **Activities**: Upgrade dependencies, refactor for compatibility
- **Aliases**: migration, upgrade

**performance-analysis**
- **Purpose**: Analyze and profile code performance
- **Activities**: Identify bottlenecks, measure execution time
- **Aliases**: profiling, performance

## Edge Cases and Decision Guidelines

### When to use bug-fixing vs error-handling-task?
- **bug-fixing**: Code is BROKEN, needs correction
- **error-handling-task**: Code works but needs error handling ADDED to prevent future issues

### When to use feature-implementation vs code-refactoring?
- **feature-implementation**: Adding NEW functionality
- **code-refactoring**: Restructuring EXISTING code (same behavior)

### When to use testing-task vs code-review-task?
- **testing-task**: Writing test code
- **code-review-task**: Reviewing and providing feedback on code

### Can a sample have multiple Task tags?
Yes! For example:
- "Refactor this code and add error handling" → `code-refactoring` + `error-handling-task`
- "Fix this bug and write a test" → `bug-fixing` + `testing-task`

### When to use Task tag vs just Agentic tag?
- Use Task tag when user explicitly states a GOAL
- Use Agentic tag when agent demonstrates a CAPABILITY
- Often use BOTH to capture full context

## Naming Conventions

**Why the `-task` suffix?**
Some task names could conflict with other dimensions:
- `testing-task` (Task) vs `testing` (Concept)
- `error-handling-task` (Task) vs `error-handling` (Concept)
- `code-review-task` (Task) vs `code-review` (Agentic)

The `-task` suffix makes the distinction clear and avoids ID conflicts.

## Summary

Task taxonomy provides 21 tags covering:
- 7 development tasks (bug-fixing, features, completion, optimization, refactoring, translation, review)
- 4 code quality tasks (testing, error-handling, logging, security-audit)
- 2 design tasks (API, schema)
- 2 documentation tasks (docs, explanation)
- 4 infrastructure tasks (config, dependencies, deployment, monitoring)
- 2 maintenance tasks (migration, performance-analysis)

All tasks describe user goals, maintaining clear orthogonality with Agentic capabilities.
