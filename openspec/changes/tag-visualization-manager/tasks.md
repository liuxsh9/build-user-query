## 1. Project Setup

- [x] 1.1 Create tag-manager directory in project root
- [x] 1.2 Initialize SvelteKit project with TypeScript template
- [x] 1.3 Install core dependencies (js-yaml, fuse.js, d3, tailwindcss)
- [x] 1.4 Configure TailwindCSS with custom theme for tag categories and difficulty levels
- [x] 1.5 Set up project structure with lib/components, lib/stores, lib/services directories
- [x] 1.6 Configure vite.config.js with path to taxonomy/tags directory
- [x] 1.7 Create .env file for feature flags (ENABLE_RELATIONSHIPS=false)

## 2. YAML Persistence Layer

- [x] 2.1 Create YamlService class in lib/server/yaml-service.js
- [x] 2.2 Implement getAllTags() method to read all YAML files
- [x] 2.3 Implement readCategory(category) method to read single category file
- [x] 2.4 Implement writeCategory(category, tags) with proper YAML formatting options
- [x] 2.5 Implement createTag(category, tagData) with ID sorting
- [x] 2.6 Implement updateTag(category, id, updates) with merge logic
- [x] 2.7 Implement deleteTag(category, id) with filtering
- [x] 2.8 Add error handling for file system errors (ENOENT, EACCES, etc)
- [x] 2.9 Add categoryNameFromFile() helper for filename to category mapping

## 3. Validation Engine

- [x] 3.1 Create validation-rules.js with VALIDATION_RULES constants
- [x] 3.2 Implement validateTag() function with all validation rules
- [x] 3.3 Add required field validation for all categories
- [x] 3.4 Add field format validation (ID pattern, enums)
- [x] 3.5 Add ID uniqueness validation across all tags
- [x] 3.6 Add category-specific required field validation
- [x] 3.7 Add subcategory consistency validation
- [x] 3.8 Add language_scope reference validation
- [x] 3.9 Add aliases uniqueness validation
- [x] 3.10 Add relationship field validation (prerequisites, related)
- [x] 3.11 Create client-side validator.js with same rules for UI
- [x] 3.12 Add structured error message formatting

## 4. API Routes

- [x] 4.1 Create routes/api/tags/+server.js for GET all tags
- [x] 4.2 Create routes/api/tags/[category]/+server.js for GET by category
- [x] 4.3 Create routes/api/tags/[category]/[id]/+server.js for PUT and DELETE
- [x] 4.4 Add POST endpoint for creating new tags
- [x] 4.5 Integrate validation in all write endpoints (POST, PUT)
- [x] 4.6 Add error handling with proper HTTP status codes (400, 404, 500)
- [x] 4.7 Create routes/api/validate/+server.js for validation-only requests
- [x] 4.8 Add CORS headers if needed for development

## 5. State Management

- [x] 5.1 Create stores/tags.js with allTags writable store
- [x] 5.2 Add loadTags() function to fetch from API
- [x] 5.3 Create tagsByCategory derived store with grouping logic
- [x] 5.4 Create categoryCounts derived store
- [x] 5.5 Implement createTag(), updateTag(), deleteTag() with optimistic updates
- [x] 5.6 Add rollback logic for failed optimistic updates
- [x] 5.7 Create stores/filters.js with selectedCategory, searchQuery, difficultyFilter, languageFilter, sortBy
- [x] 5.8 Create filteredTags derived store combining all filters
- [x] 5.9 Create stores/ui.js for modal state, selected tag, toast notifications
- [x] 5.10 Create stores/git.js for git status and commit state

## 6. Search and Filter

- [x] 6.1 Create services/search.js wrapper around Fuse.js
- [x] 6.2 Configure Fuse.js with weighted keys (name: 2, id: 1.5, aliases: 1, description: 0.5)
- [x] 6.3 Set fuzzy threshold to 0.3 for typo tolerance
- [x] 6.4 Implement createSearchIndex() function
- [x] 6.5 Add search() function returning ranked results
- [x] 6.6 Implement sortTags() utility in utils/sorting.js
- [x] 6.7 Add sorting by name, id, and difficulty

## 7. Layout Components

- [x] 7.1 Create routes/+layout.svelte with app shell structure
- [x] 7.2 Create components/layout/TopBar.svelte with title, search, and action buttons
- [x] 7.3 Create components/layout/CategoryNav.svelte with category list and counts
- [x] 7.4 Add active category highlighting in CategoryNav
- [x] 7.5 Create components/layout/GitStatus.svelte widget
- [x] 7.6 Implement responsive layout (sidebar collapse on mobile)

## 8. Tag Visualization Views

- [x] 8.1 Create components/views/TagGrid.svelte for grid view
- [x] 8.2 Implement adaptive view logic (< 100 tags = grid, >= 100 = table)
- [x] 8.3 Create components/views/TagCard.svelte with tag info display
- [x] 8.4 Add difficulty color coding (green, amber, red) in TagCard
- [x] 8.5 Add hover actions (edit, delete) to TagCard
- [x] 8.6 Create components/views/TagTable.svelte for table view
- [x] 8.7 Add sortable column headers in TagTable
- [x] 8.8 Implement row click to open editor in TagTable
- [ ] 8.9 Create components/shared/VirtualScroll.svelte using IntersectionObserver
- [ ] 8.10 Integrate VirtualScroll into TagTable for large lists
- [ ] 8.11 Add subcategory grouping headers with collapsible sections
- [ ] 8.12 Create empty state component for no results

## 9. Search and Filter UI

- [x] 9.1 Create components/filters/SearchBar.svelte with input and clear button
- [ ] 9.2 Add debouncing (300ms) to search input
- [ ] 9.3 Create components/filters/FilterPanel.svelte
- [ ] 9.4 Add difficulty filter dropdown (All, Basic, Intermediate, Advanced)
- [ ] 9.5 Add language filter dropdown populated from Language tags
- [ ] 9.6 Add sort selector dropdown (Name, ID, Difficulty)
- [ ] 9.7 Display "Showing X of Y tags" count
- [ ] 9.8 Add "Clear all filters" button

## 10. Tag Editor

- [x] 10.1 Create components/editor/TagEditor.svelte modal component
- [x] 10.2 Create components/editor/BasicFields.svelte (id, name, category, source)
- [x] 10.3 Create components/editor/MetadataFields.svelte (subcategory, difficulty, description, aliases)
- [x] 10.4 Implement category-specific field visibility logic
- [ ] 10.5 Add language_scope multi-select populated from Language tags
- [ ] 10.6 Create components/editor/RelationshipFields.svelte (disabled by default)
- [ ] 10.7 Implement client-side validation with real-time feedback
- [ ] 10.8 Add field-level error messages
- [x] 10.9 Implement form submission with API call
- [x] 10.10 Add success/error toast notifications
- [ ] 10.11 Implement duplicate tag button
- [ ] 10.12 Add delete confirmation dialog
- [ ] 10.13 Handle modal close with unsaved changes warning

## 11. Git Integration

- [x] 11.1 Create lib/server/git-service.js with GitService class
- [x] 11.2 Implement getStatus() method using git status --porcelain
- [x] 11.3 Implement commit(message) method with git add and git commit
- [x] 11.4 Implement getRecentCommits(limit) using git log
- [x] 11.5 Add parseStatus() helper for status codes
- [x] 11.6 Add escapeMessage() for commit message sanitization
- [x] 11.7 Create routes/api/git/status/+server.js
- [x] 11.8 Create routes/api/git/commit/+server.js with POST handler
- [x] 11.9 Update GitStatus.svelte to display uncommitted changes
- [ ] 11.10 Add color coding for file status (modified, added, deleted)
- [ ] 11.11 Create commit modal with message input
- [ ] 11.12 Add commit message validation (non-empty)
- [ ] 11.13 Display recent commits list in GitStatus widget
- [ ] 11.14 Add auto-refresh of git status after tag CRUD operations
- [ ] 11.15 Add manual refresh button
- [ ] 11.16 Implement warning badge for uncommitted changes

## 12. Shared Components

- [ ] 12.1 Create components/shared/Modal.svelte with backdrop and ESC handling
- [ ] 12.2 Create components/shared/Button.svelte with variants (primary, secondary, danger)
- [ ] 12.3 Create components/shared/Badge.svelte for difficulty and category tags
- [ ] 12.4 Create components/shared/Toast.svelte for notifications
- [x] 12.5 Implement toast queue in ui store
- [x] 12.6 Add toast auto-dismiss after 5 seconds

## 13. Main Application Page

- [x] 13.1 Create routes/+page.svelte as main application interface
- [ ] 13.2 Create routes/+page.js to load initial tag data
- [x] 13.3 Wire up CategoryNav with selectedCategory store
- [x] 13.4 Wire up SearchBar with searchQuery store
- [ ] 13.5 Wire up FilterPanel with filter stores
- [x] 13.6 Conditionally render TagGrid or TagTable based on tag count
- [x] 13.7 Connect TagEditor modal to ui store state
- [x] 13.8 Handle "New Tag" button click to open editor
- [x] 13.9 Handle tag card/row click to open editor with existing tag
- [x] 13.10 Integrate GitStatus widget into layout

## 14. Relationship Management (Reserved)

- [x] 14.1 Add ENABLE_RELATIONSHIPS feature flag check
- [ ] 14.2 Conditionally show/hide relationship UI based on flag
- [ ] 14.3 Add relationship fields to tag schema types
- [ ] 14.4 Create placeholder components/RelationshipGraph.svelte
- [ ] 14.5 Add "View Relationships" button (disabled when flag=false)
- [ ] 14.6 Show "Coming Soon" modal when relationship button clicked
- [ ] 14.7 Document relationship schema in code comments

## 15. Styling and Design

- [x] 15.1 Define color palette in tailwind.config.js for categories
- [x] 15.2 Define difficulty badge colors (green, amber, red)
- [x] 15.3 Style CategoryNav with hover and active states
- [x] 15.4 Style TagCard with shadow and hover effects
- [x] 15.5 Style TagTable with alternating row colors
- [x] 15.6 Style TagEditor modal with proper spacing
- [x] 15.7 Style form inputs with focus states
- [ ] 15.8 Style validation error messages in red
- [ ] 15.9 Add loading spinners for async operations
- [ ] 15.10 Add smooth transitions for view switching

## 16. Keyboard Shortcuts

- [ ] 16.1 Implement Ctrl+K / Cmd+K for quick search focus
- [ ] 16.2 Implement Ctrl+N / Cmd+N for new tag
- [ ] 16.3 Implement ESC to close modal
- [ ] 16.4 Add keyboard shortcut hints in UI (tooltips)
- [ ] 16.5 Handle keyboard navigation in search results

## 17. Error Handling and Resilience

- [ ] 17.1 Add global error boundary in +layout.svelte
- [ ] 17.2 Handle API fetch errors with user-friendly messages
- [ ] 17.3 Add retry logic for transient network errors
- [ ] 17.4 Handle YAML parse errors gracefully
- [ ] 17.5 Add validation error display in editor
- [ ] 17.6 Handle git command failures with informative errors
- [ ] 17.7 Add browser unload warning when uncommitted changes exist

## 18. Performance Optimization

- [ ] 18.1 Implement debouncing on search input (300ms)
- [ ] 18.2 Add memoization to expensive derived stores
- [ ] 18.3 Optimize virtual scrolling buffer size (20 items above/below viewport)
- [ ] 18.4 Lazy load relationship graph component (code splitting)
- [ ] 18.5 Add loading states for slow operations
- [ ] 18.6 Bundle analysis and tree-shaking verification
- [ ] 18.7 Compress assets in production build

## 19. Testing and Validation

- [ ] 19.1 Test CRUD operations for each category type
- [ ] 19.2 Test validation rules with invalid data
- [ ] 19.3 Test search with fuzzy matching and typos
- [ ] 19.4 Test filtering combinations (category + difficulty + language)
- [ ] 19.5 Test virtual scrolling with Library category (339 tags)
- [ ] 19.6 Test git integration (status, commit, error cases)
- [ ] 19.7 Test optimistic updates and rollback on error
- [ ] 19.8 Test YAML format preservation after write
- [ ] 19.9 Test keyboard shortcuts
- [ ] 19.10 Test responsive layout on mobile

## 20. Documentation and Polish

- [x] 20.1 Write README.md with setup instructions
- [x] 20.2 Document API endpoints and request/response formats
- [ ] 20.3 Document validation rules reference
- [ ] 20.4 Add inline code comments for complex logic
- [ ] 20.5 Create user guide with screenshots
- [x] 20.6 Document feature flag usage
- [x] 20.7 Add development workflow guide (npm scripts)
- [ ] 20.8 Document deployment options (Node.js server, static build)
