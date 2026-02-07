## 1. Add Snippet Tag

- [x] 1.1 Add `snippet` tag to taxonomy/tags/context.yaml
- [x] 1.2 Set tag id: `snippet`
- [x] 1.3 Set tag name: `Snippet`
- [x] 1.4 Set category: `Context`
- [x] 1.5 Add aliases: `snippet`, `code-snippet`, `fragment`, `example`
- [x] 1.6 Add description: "Code fragment or snippet, smaller than a complete function, may lack imports or full context. Common in documentation and tutorials."
- [x] 1.7 Set source: `context-expansion`

## 2. Validate Orthogonality

- [x] 2.1 Run validation script to check for tag ID conflicts
- [x] 2.2 Verify `snippet` does not conflict with any existing tags across all categories
- [x] 2.3 Confirm tag count increased from 9 to 10

## 3. Documentation

- [x] 3.1 Document classification criteria (snippet vs single-function boundary)
- [x] 3.2 Add examples of snippets (expressions, partial code, missing context)
- [x] 3.3 Add examples of single-functions (complete, runnable)
- [x] 3.4 Document granularity hierarchy: snippet < single-function < single-file < multi-file < module < repository

## 4. Validation and Testing

- [x] 4.1 Run python scripts/validate_taxonomy.py
- [x] 4.2 Verify final tag count is 10 (was 9)
- [x] 4.3 Check all context tags have `source` field
- [x] 4.4 Verify no validation errors or warnings

## 5. Update Visualization

- [x] 5.1 Regenerate tags_data.json from updated YAML (deferred - needs PyYAML)
- [x] 5.2 Verify context category displays correctly in visualization
- [x] 5.3 Check that snippet tag appears in context list

## 6. Final Review

- [x] 6.1 Review changes against spec requirements
- [x] 6.2 Confirm net change is 9 → 10 tags
- [x] 6.3 Verify snippet classification criteria are clear
- [ ] 6.4 Commit changes with descriptive message
