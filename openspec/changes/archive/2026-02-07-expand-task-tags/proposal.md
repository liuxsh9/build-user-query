## Why

Current Task taxonomy (15 tags) lacks fundamental programming tasks like bug-fixing, feature implementation, and testing that are extremely common in training data. Additionally, all tags lack descriptions, reducing usability and clarity. Need to add essential task types and improve metadata completeness.

## What Changes

**Add** 6 new fundamental task types:
- `bug-fixing` - Fixing bugs and errors in code
- `feature-implementation` - Implementing new features or functionality
- `testing` - Writing tests (unit, integration, e2e)
- `error-handling` - Adding error handling and validation
- `logging` - Adding logging and instrumentation
- `code-review-task` - Performing code review and providing feedback

**Enhance** all existing tags:
- Add descriptions to all 15 existing tags (currently none have descriptions)
- Review and optimize aliases for searchability

**Result**: 15 → 21 tags, all with complete metadata

## Capabilities

### New Capabilities
- `task-expansion`: Define 6 new fundamental task types and add descriptions to all task tags

### Modified Capabilities
<!-- No existing task specs to modify -->

## Impact

**Taxonomy structure**:
- `taxonomy/tags/task.yaml` - Add 6 new tags and descriptions for all 21 tags
- Net change: 15 → 21 tags (+6)

**Task coverage**:
- Fills critical gaps in fundamental programming tasks
- Distinguishes Task (what user wants to do) from Agentic (agent capabilities)
- Better classification of common training data patterns

**Data annotation**:
- Improved ability to classify bug-fixing, feature development, testing tasks
- All tags now have clear descriptions for annotators
- Better task type coverage for diverse code samples

**Metadata quality**:
- All tags will have descriptions explaining their purpose
- Consistent metadata structure across all task tags
