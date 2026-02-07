## Why

Current Context taxonomy (9 tags) covers code organization granularity (function → file → module → repository) but lacks the "snippet" granularity for incomplete code fragments. Training data often includes code snippets from documentation, tutorials, and Q&A sites that are smaller than complete functions and need distinct classification.

## What Changes

**Add** one new tag:
- `snippet` - Code fragment/snippet, smaller than a complete function, may lack full context

**Result**: 9 → 10 tags, completing the granularity spectrum

## Capabilities

### New Capabilities
- `context-snippet`: Define the snippet context tag for code fragments smaller than complete functions

### Modified Capabilities
<!-- No existing context specs to modify -->

## Impact

**Taxonomy structure**:
- `taxonomy/tags/context.yaml` - Add 1 new tag: `snippet`
- Net change: 9 → 10 tags (+1)

**Granularity completeness**:
- Fills the gap below `single-function` for incomplete code fragments
- Enables classification of documentation examples, tutorial snippets, Q&A answers

**Data annotation**:
- Better classification of code fragment samples
- Distinguishes complete vs incomplete code units
- Improves coverage for tutorial and documentation content
