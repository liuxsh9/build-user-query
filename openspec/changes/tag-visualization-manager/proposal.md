## Why

The taxonomy contains 587 tags across 8 categories stored in YAML files that change daily. Currently, there's no efficient way to browse, search, filter, or manage these tags. A visual management interface is needed to view the taxonomy structure, edit tags with validation, and maintain data quality through a user-friendly interface.

## What Changes

- Create a standalone web application for tag visualization and management
- Implement full CRUD operations for tags with comprehensive validation
- Add powerful search and filtering capabilities across all tag attributes
- Provide adaptive views (grid for small datasets, table with virtual scrolling for large ones)
- Integrate Git operations for manual commit workflow
- Support relationship visualization between tags (interface reserved for future data)
- Build with SvelteKit for lightweight bundle size and excellent developer experience

## Capabilities

### New Capabilities

- `tag-crud-operations`: Create, read, update, and delete tags in YAML files with optimistic UI updates and rollback on error
- `tag-search-filter`: Full-text fuzzy search across tag fields (name, id, aliases, description) with filters by category, difficulty, language scope
- `tag-visualization-views`: Adaptive display modes - grid view for <100 tags, table view with virtual scrolling for ≥100 tags, with automatic switching
- `yaml-persistence`: Read and write YAML files directly, maintaining format and structure, with file watching for external changes
- `tag-validation`: Comprehensive validation rules enforcing required fields, field formats, cross-field constraints, and category-specific requirements
- `git-integration`: Display uncommitted changes, manual commit with messages, view recent commit history
- `relationship-management`: Reserved interface for defining and visualizing tag relationships (prerequisites, related tags) - implementation deferred until relationship data is available

### Modified Capabilities

<!-- No existing capabilities are being modified -->

## Impact

**New Code**:
- Complete SvelteKit application in new `tag-manager/` directory
- Frontend components (category navigation, tag grid/table, tag editor, search/filter UI)
- Backend API routes for tag CRUD, validation, and Git operations
- YAML service layer for reading/writing taxonomy files
- Validation engine implementing all tag schema rules

**Dependencies**:
- SvelteKit (framework)
- js-yaml (YAML parsing)
- Fuse.js (fuzzy search)
- D3.js (relationship graphs - minimal subset)
- TailwindCSS (styling)

**Data Impact**:
- Direct read/write access to `taxonomy/tags/*.yaml`
- No schema changes to existing YAML structure
- Manual Git commits required (no automatic commits)

**Development Workflow**:
- Single-user application (no authentication needed)
- Development server with hot reload
- Production build for static deployment
