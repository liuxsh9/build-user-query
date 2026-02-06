# agentic-coordination Specification

## Purpose
Define coordination capabilities enabling agents to interact with users, manage subagents, execute tasks in parallel, and track progress. Essential for complex multi-step workflows requiring human-in-the-loop and agent delegation.

## Requirements

### Requirement: Define user-interaction capability
The system SHALL provide user-interaction capability for requesting human decisions and feedback.

#### Scenario: Request user decision
- **WHEN** agent faces multiple valid options
- **THEN** it SHALL use user-interaction to present options and await user choice

#### Scenario: Request user confirmation
- **WHEN** agent needs approval before critical action
- **THEN** it SHALL use user-interaction to request confirmation

#### Scenario: Collect user preferences
- **WHEN** agent needs to understand user preferences
- **THEN** it SHALL use user-interaction to gather preference information

#### Scenario: Multiple choice questions
- **WHEN** user-interaction presents choices
- **THEN** it SHALL support 2-4 options with descriptions

#### Scenario: Free-form input
- **WHEN** user needs to provide custom input
- **THEN** user-interaction SHALL support "Other" option for freeform text

#### Scenario: Tool mapping
- **WHEN** implementing user-interaction
- **THEN** it MAY map to: AskUserQuestion (Claude Code), input() (Python), prompt() (JavaScript)

### Requirement: Define subagent-management capability
The system SHALL provide subagent-management for spawning and managing specialized agents.

#### Scenario: Spawn specialized subagent
- **WHEN** agent encounters task requiring specialized capability
- **THEN** it SHALL spawn subagent with specific role (e.g., "test-runner", "build-validator")

#### Scenario: Pass context to subagent
- **WHEN** spawning subagent
- **THEN** it SHALL provide relevant context and task description

#### Scenario: Await subagent completion
- **WHEN** subagent is working
- **THEN** parent agent SHALL wait for completion or poll status

#### Scenario: Retrieve subagent results
- **WHEN** subagent completes
- **THEN** parent agent SHALL retrieve results and incorporate into workflow

#### Scenario: Handle subagent failure
- **WHEN** subagent fails
- **THEN** parent agent SHALL handle error and potentially retry or escalate

#### Scenario: Tool mapping
- **WHEN** implementing subagent-management
- **THEN** it MAY map to: Task tool (Claude Code), subprocess (Python), child_process (Node.js)

### Requirement: Define parallel-execution capability
The system SHALL provide parallel-execution for concurrent task processing.

#### Scenario: Execute independent tasks concurrently
- **WHEN** agent has multiple independent tasks
- **THEN** it SHALL execute them in parallel to improve throughput

#### Scenario: Await all parallel tasks
- **WHEN** parallel tasks are running
- **THEN** agent SHALL wait for all to complete before proceeding

#### Scenario: Handle partial failures
- **WHEN** some parallel tasks fail
- **THEN** agent SHALL handle failures gracefully and report which succeeded/failed

#### Scenario: Resource-aware parallelism
- **WHEN** spawning parallel tasks
- **THEN** agent SHOULD consider resource limits (CPU, memory, API rate limits)

#### Scenario: Tool mapping
- **WHEN** implementing parallel-execution
- **THEN** it MAY use: Promise.all (JavaScript), asyncio.gather (Python), parallel Task tools

### Requirement: Define task-tracking capability
The system SHALL provide task-tracking for managing TODO items and progress.

#### Scenario: Create task item
- **WHEN** agent starts complex work
- **THEN** it SHALL create task items for tracking progress

#### Scenario: Update task status
- **WHEN** agent completes subtask
- **THEN** it SHALL update task status (pending → in_progress → completed)

#### Scenario: Track dependencies
- **WHEN** tasks have dependencies
- **THEN** task-tracking SHALL record blockedBy and blocks relationships

#### Scenario: Report progress
- **WHEN** user requests progress update
- **THEN** task-tracking SHALL show completed vs pending tasks

#### Scenario: Tool mapping
- **WHEN** implementing task-tracking
- **THEN** it MAY map to: TaskCreate/TaskUpdate (Claude Code), TODO comments, GitHub Issues

### Requirement: Ensure orthogonality with existing coordination tags
The system SHALL maintain distinction from existing multi-step-reasoning and iterative-refinement.

#### Scenario: user-interaction vs autonomous operation
- **WHEN** comparing user-interaction to other tags
- **THEN** user-interaction SHALL be unique in requiring human input

#### Scenario: subagent-management vs multi-step-reasoning
- **WHEN** comparing subagent-management to multi-step-reasoning
- **THEN** subagent-management SHALL delegate to other agents, multi-step-reasoning SHALL execute steps internally

#### Scenario: parallel-execution vs iterative-refinement
- **WHEN** comparing parallel-execution to iterative-refinement
- **THEN** parallel-execution SHALL run tasks concurrently, iterative-refinement SHALL improve sequentially

#### Scenario: task-tracking vs context-management
- **WHEN** comparing task-tracking to context-management
- **THEN** task-tracking SHALL manage TODO items, context-management SHALL manage information/memory
