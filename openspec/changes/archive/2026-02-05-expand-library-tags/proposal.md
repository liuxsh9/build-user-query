## Why

Current Library taxonomy has only 85 tags with inconsistent granularity (mixing library-level like "React" with module-level like "Pandas GroupBy"), incomplete alias coverage, and limited data sources. This prevents comprehensive coverage of the library/framework landscape needed for diverse SFT query generation.

## What Changes

- Expand Library tags from 85 to ~300 tags across all 5 subcategories
- Establish clear granularity guidelines distinguishing library-level vs module-level tags
- Enhance alias coverage with automated extraction from multiple sources
- Integrate new data sources: Stack Overflow tags, npm/PyPI download stats, GitHub Topics, academic papers
- Add granularity metadata to each tag (library-level, module-level, function-level)
- Implement automated alias expansion tool

## Capabilities

### New Capabilities
- `library-granularity-guidelines`: Define clear rules for when to use library-level vs module-level tags
- `automated-alias-expansion`: Tool to extract aliases from code repositories, documentation, and community usage
- `multi-source-tag-collection`: Integrate Stack Overflow, npm/PyPI, GitHub Topics, and academic sources

### Modified Capabilities
- `tag-collection`: Extend to support new data sources and granularity classification
- `tag-normalization`: Add granularity validation and alias expansion steps

## Impact

- Increases Library tags from 85 to ~300 (3.5x growth)
- Improves tag quality through standardized granularity
- Enhances discoverability through comprehensive aliases
- Enables more precise capability labeling for SFT data
- Requires updates to collection and normalization scripts
