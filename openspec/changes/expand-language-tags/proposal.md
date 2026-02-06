## Why

Current Language taxonomy has 50 programming languages with basic coverage, but misses many commonly-used languages critical for real-world projects (Makefile, TeX, XML, JSON, YAML, etc.) and lacks structured metadata about language characteristics (paradigm, typing, runtime) needed for sophisticated query generation. Additionally, business-critical languages (ArkTS, AscendC) are not yet included.

## What Changes

- Expand Language tags from 50 to ~75-90 tags with balanced coverage across paradigms and use cases
- Add missing common languages: build tools (Makefile, CMake), markup/config (XML, JSON, YAML, TOML), documentation (TeX, Markdown), and business-critical languages (ArkTS, AscendC)
- Add structured metadata fields:
  - `paradigm`: Programming paradigm(s) - imperative, functional, object-oriented, declarative, etc.
  - `typing`: Type system - static, dynamic, gradual, duck, strong, weak
  - `runtime`: Execution model - compiled, interpreted, jit, transpiled
  - `use_cases`: Primary domains - web, systems, data-science, mobile, embedded, scripting, etc.
- Enhance alias coverage with real-world usage patterns from Stack Overflow, GitHub, and PYPL
- Focus on languages actively used in production projects, not academic/historical languages

## Capabilities

### New Capabilities
- `language-metadata-schema`: Define structured metadata schema for paradigm, typing, runtime, and use_cases
- `language-gap-analysis`: Identify missing common languages from real-world project data sources
- `language-alias-collection`: Extract common aliases from Stack Overflow tags, GitHub Topics, PYPL rankings

### Modified Capabilities
- `tag-collection`: Extend to support language-specific sources (PYPL, Stack Overflow, RedMonk, IEEE Spectrum)
- `tag-normalization`: Add metadata validation for paradigm, typing, runtime consistency
- `taxonomy-validation`: Add Language-specific validation rules for metadata completeness

## Impact

- Increases Language tags from 50 to ~75-90 (1.5-1.8x growth)
- Adds 5 new metadata fields per language for richer query generation
- Covers critical gaps in build tools, markup/config, and documentation languages
- Includes business-critical languages (ArkTS, AscendC) for enterprise use cases
- Enables paradigm-based and use-case-based query filtering
- Requires schema updates to taxonomy.yaml for new metadata fields
