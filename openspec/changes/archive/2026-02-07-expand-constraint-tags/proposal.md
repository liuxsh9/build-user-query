## Why

Current Constraint taxonomy (25 tags) contains subjective, non-judgeable tags that cannot be used for objective data annotation and gap detection. Many tags like `readable`, `maintainable`, `testable` are too subjective to evaluate systematically. The taxonomy needs optimization to focus on objective, verifiable constraints that enable rule-based data classification and directed discovery of missing data.

## What Changes

**Remove** subjective/non-judgeable tags (3):
- `readable` - Cannot objectively determine if code is readable
- `maintainable` - Cannot objectively determine maintainability
- `testable` - Ambiguous definition, overlaps with testing concepts

**Merge** performance tags into unified constraint (3→1):
- Merge `high-performance`, `low-latency`, `memory-efficient` → `performance-optimized`
- Rationale: All measure performance aspects, unified tag with clear measurement criteria

**Split/Remove** overly broad tags:
- Remove `secure` - Too broad, replaced by specific verifiable security constraints

**Add** objective, verifiable constraints (8-10 new):
- State management: `stateless`, `immutable`
- Concurrency: `lock-free`, `async`
- Observability: `observable`
- Resource: `bounded-resource`
- Deployment: `zero-downtime`
- Security: `input-validated`, `encrypted` (specific verifiable aspects)

**Result**: 25 → ~22-25 tags, optimized for objectivity and orthogonality

## Capabilities

### New Capabilities
- `constraint-optimization`: Define principles for objective, verifiable constraint tags and apply cleanup/optimization rules to existing taxonomy

### Modified Capabilities
<!-- No existing constraint specs to modify -->

## Impact

**Taxonomy structure**:
- `taxonomy/tags/constraint.yaml` - Remove 3 subjective tags, merge 3 performance tags, add 8-10 objective tags
- Net change: ~22-25 tags (from 25)

**Validation**:
- All constraint tags must have explicit judgment criteria
- Enhanced validation rules to prevent subjective constraints

**Documentation**:
- Update constraint design principles with objectivity requirement
- Document judgment rules for each constraint tag

**Data annotation**:
- Improved ability to systematically classify code samples
- Better gap detection for missing constraint coverage
