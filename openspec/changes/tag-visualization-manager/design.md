## Context

The taxonomy system stores 587 tags across 8 categories in YAML files (`taxonomy/tags/*.yaml`). These tags have varying structures based on category - Concept tags include difficulty and subcategory, Library tags include language_scope and subcategories, etc. Tags are updated daily, requiring fresh reads. Currently there is no UI for browsing or editing these tags.

**Current State**:
- YAML files are the source of truth
- Manual editing with text editors (prone to validation errors)
- No search or filter capabilities
- No visibility into tag relationships or coverage

**Constraints**:
- Must preserve YAML file format and structure
- Single-user application (no concurrent editing)
- Manual Git workflow (no auto-commits)
- Relationship features deferred until data exists
- Lightweight bundle size (<100KB total)

**Stakeholders**: Taxonomy maintainers who need to view and edit tags efficiently

## Goals / Non-Goals

**Goals:**
- Provide fast, intuitive browsing of 587 tags with adaptive views
- Enable safe CRUD operations with comprehensive validation
- Support fuzzy search and multi-dimensional filtering
- Maintain YAML file integrity and readability
- Integrate with Git workflow for version control
- Reserve UI space for future relationship features

**Non-Goals:**
- Multi-user collaboration or conflict resolution
- Real-time synchronization across multiple clients
- Automatic Git commits or complex merge strategies
- Complete relationship graph implementation (deferred)
- Authentication or authorization
- Cloud deployment or backend infrastructure

## Decisions

### 1. Framework: SvelteKit

**Decision**: Use SvelteKit for full-stack application with API routes.

**Rationale**:
- Smallest compiled bundle (~3-5KB runtime vs React's ~40KB)
- Built-in API routes eliminate separate backend
- Excellent reactivity model for data-heavy UIs
- SSR capability for fast initial load
- File-based routing matches our needs

**Alternatives Considered**:
- React + Express: Larger bundle, more boilerplate, separate repos
- Vue + Nuxt: Good but larger than Svelte (~35KB)
- Vanilla JS: Too much manual state management for this complexity

### 2. Data Loading: Server-Side YAML Reading

**Decision**: Load YAML files server-side on each request, no client-side caching.

**Rationale**:
- Always shows latest data (tags change daily)
- Avoids stale cache issues
- Server has direct file access
- Tags file is ~100KB total, fast to parse

**Alternatives Considered**:
- Build-time compilation: Stale data, requires rebuild on every tag change
- Client-side YAML parsing: Adds 20KB library, slower initial load
- Database: Overkill for flat file structure, adds complexity

### 3. View Strategy: Adaptive Grid/Table

**Decision**: Automatically switch between grid view (<100 tags) and virtual-scrolled table (≥100 tags).

**Rationale**:
- Grid view is visual and scannable for small datasets
- Table view performs better with 300+ items
- Library category (339 tags) needs virtual scrolling
- Automatic switching provides best UX per context

**Alternatives Considered**:
- Always grid: Performance issues with 339 library tags
- Always table: Less engaging for small categories
- Manual toggle: Extra cognitive load on user

### 4. Search: Fuse.js for Fuzzy Search

**Decision**: Use Fuse.js for client-side fuzzy search with weighted fields.

**Rationale**:
- 12KB library, acceptable for our budget
- Excellent fuzzy matching (typo tolerance)
- Weighted search (name > id > aliases > description)
- Fast enough for 587 items client-side

**Alternatives Considered**:
- FlexSearch: Faster but less fuzzy, worse for tag search
- Simple indexOf: No typo tolerance, poor UX
- Server-side search: Unnecessary latency for small dataset

### 5. Validation: Dual-Layer (Client + Server)

**Decision**: Implement validation both client-side (immediate feedback) and server-side (enforcement).

**Rationale**:
- Client validation provides instant feedback
- Server validation ensures data integrity (no bypass)
- Same validation rules shared between layers
- Prevents invalid YAML writes

**Validation Rules**:
- Required fields by category
- ID format (kebab-case) and uniqueness
- Category/subcategory validity
- Language_scope references valid Language tags
- Difficulty enum values
- Aliases uniqueness
- Cross-field constraints

**Alternatives Considered**:
- Client-only: Can be bypassed, risks bad data
- Server-only: Poor UX, no instant feedback
- JSON Schema: Insufficient for cross-tag validation

### 6. State Management: Svelte Stores

**Decision**: Use Svelte's built-in stores for all state management.

**Rationale**:
- Native to Svelte, zero bundle cost
- Reactive by design
- Derived stores handle computed state cleanly
- Sufficient for single-user application

**Store Structure**:
```
- allTags (writable): Raw tag data from API
- tagsByCategory (derived): Grouped by category
- filteredTags (derived): After search/filter application
- ui (writable): Modal state, selected tag
- git (writable): Uncommitted changes, status
```

**Alternatives Considered**:
- Redux/Zustand: Overkill for this scale
- Component-local state: Too much prop drilling

### 7. YAML Persistence: js-yaml with Format Preservation

**Decision**: Use js-yaml to parse and dump YAML, preserving formatting and structure.

**Rationale**:
- Mature library, handles YAML spec fully
- Dump options preserve readability (indent, line width)
- Maintains YAML compatibility with external tools
- Sorts tags by ID for consistency

**Format Options**:
```javascript
yaml.dump(tags, {
  indent: 2,
  lineWidth: -1,  // No line wrapping
  noRefs: true,   // No anchors/aliases
  sortKeys: false // Preserve order
})
```

**Alternatives Considered**:
- Custom parser: Reinventing wheel, error-prone
- JSON storage: Loses YAML human-readability

### 8. Git Integration: Shell Commands via Child Process

**Decision**: Execute git commands via Node's child_process, display status in UI.

**Rationale**:
- Simple, direct git access
- No library dependencies
- Full git power available
- Manual workflow (no surprises)

**Commands Used**:
- `git status --porcelain taxonomy/tags/`
- `git add taxonomy/tags/`
- `git commit -m "message"`
- `git log --oneline -n 10 -- taxonomy/tags/`

**Alternatives Considered**:
- isomorphic-git: Adds 500KB, overkill for simple commands
- No git integration: Forces manual terminal use

### 9. Virtual Scrolling: IntersectionObserver

**Decision**: Implement virtual scrolling using native IntersectionObserver API.

**Rationale**:
- Zero dependencies
- Excellent browser support
- Sufficient for 339-item library category
- ~50 lines of code

**Alternatives Considered**:
- react-window/svelte-virtual-list: Adds library for simple case
- Render all 339: Causes jank, poor UX

### 10. Relationship Visualization: Reserved Interface

**Decision**: Create UI placeholder for relationships but defer D3 graph implementation.

**Rationale**:
- Relationship data doesn't exist yet in YAML
- Can design schema and UI contracts now
- Implementation when data is ready
- Avoids premature feature development

**Reserved Fields**:
```yaml
prerequisites: [tag-id-1, tag-id-2]
related: [tag-id-3, tag-id-4]
```

## Risks / Trade-offs

### [Risk] YAML file corruption from bad writes
**Mitigation**:
- Comprehensive server-side validation before writes
- Keep backup copy before overwrite (`.yaml.bak`)
- Git provides recovery mechanism
- Validate YAML syntax after write

### [Risk] Concurrent edits (if multiple users access)
**Mitigation**:
- Document as single-user application
- Display warning if git shows uncommitted changes on load
- Manual git workflow forces coordination

### [Risk] Large bundle size from dependencies
**Mitigation**:
- Bundle analysis in build process
- Tree-shake D3 (only import force-graph module)
- Lazy-load relationship graph component
- Target: <80KB total (currently ~60KB)

### [Risk] Performance degradation with more tags
**Mitigation**:
- Virtual scrolling for large lists
- Debounced search (300ms)
- Memoized derived stores
- Client-side search works up to ~2000 tags

### [Risk] YAML formatting changes on write
**Mitigation**:
- Preserve original formatting with yaml.dump options
- Sort by ID for consistency
- Test with round-trip parsing
- Show diff before commit

### [Trade-off] Server-side rendering vs Client-side only
**Chosen**: Server-side rendering (SSR)
- **Pro**: Fast initial load, SEO-friendly (though not needed here)
- **Con**: More complex deployment than static site
- **Justification**: SvelteKit makes SSR easy, worth it for perceived performance

### [Trade-off] Optimistic updates vs Wait for server
**Chosen**: Optimistic updates with rollback
- **Pro**: Instant feedback, feels responsive
- **Con**: Must handle rollback on failure
- **Justification**: Better UX for tag editing, failures are rare

## Migration Plan

### Phase 1: Setup (Day 1)
1. Create `tag-manager/` directory
2. Initialize SvelteKit project with TypeScript
3. Configure TailwindCSS
4. Set up project structure

### Phase 2: Read-Only Viewer (Days 2-3)
1. Implement YAML reading service
2. Build API route: GET /api/tags
3. Create category navigation component
4. Implement grid and table views
5. Add search and filter functionality

### Phase 3: CRUD Operations (Days 4-6)
1. Implement validation rules engine
2. Build tag editor component
3. Create API routes: POST, PUT, DELETE /api/tags
4. Add optimistic updates with rollback
5. Implement error handling and user feedback

### Phase 4: Git Integration (Day 7)
1. Build git service wrapper
2. Add git status display
3. Implement commit UI with message input
4. Show recent commit history

### Phase 5: Polish (Days 8-9)
1. Virtual scrolling for large lists
2. Keyboard shortcuts
3. Dark mode (if time permits)
4. Performance optimization
5. Documentation

### Rollback Strategy
- Application is additive (no existing code changes)
- To rollback: delete `tag-manager/` directory
- YAML files unchanged by installation
- Git history preserves all tag changes

### Deployment
- Development: `npm run dev` (localhost:5173)
- Production: `npm run build` → `node build/` (Node.js server)
- Alternative: Build static version with adapter-static

## Open Questions

1. **Should we add import/export for bulk tag operations?**
   - Useful for migrations or backup
   - CSV export for spreadsheet analysis?
   - Decision: Defer to Phase 6 if needed

2. **Dark mode implementation approach?**
   - TailwindCSS dark: class or system preference?
   - Decision: System preference, low priority

3. **Tag duplication feature?**
   - Quick way to create similar tags
   - Decision: Yes, include in editor as "Duplicate" button

4. **Undo/redo for tag edits?**
   - Complex state management
   - Git provides version history
   - Decision: No, git is sufficient

5. **Keyboard shortcuts - which ones?**
   - Ctrl+K: Quick search
   - Ctrl+N: New tag
   - Esc: Close modal
   - Decision: Implement these three, add more based on usage
