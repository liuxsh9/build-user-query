# Tag Manager

A lightweight web application for visualizing and managing taxonomy tags. Built with SvelteKit, this tool provides CRUD operations, search, filtering, and Git integration for tag management.

## Features

- **CRUD Operations**: Create, read, update, and delete tags with validation
- **Search & Filter**: Fuzzy search with typo tolerance, filter by difficulty and language
- **Adaptive Views**: Grid view for small datasets, table view for large ones
- **YAML Persistence**: Direct read/write to YAML files with format preservation
- **Validation**: Comprehensive validation rules on both client and server
- **Git Integration**: View uncommitted changes and commit directly from UI
- **Optimistic Updates**: Instant UI feedback with rollback on error

## Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Usage

1. Open http://localhost:5173 in your browser
2. Browse tags by category in the left sidebar
3. Search tags using the search bar (supports fuzzy matching)
4. Click "+ New Tag" to create a new tag
5. Click on any tag card/row to edit
6. Changes are saved to YAML files in `../taxonomy/tags/`
7. View uncommitted changes in the bottom-right Git status widget

## API Endpoints

- `GET /api/tags` - Get all tags
- `GET /api/tags/[category]` - Get tags by category
- `POST /api/tags` - Create new tag
- `PUT /api/tags/[category]/[id]` - Update tag
- `DELETE /api/tags/[category]/[id]` - Delete tag
- `POST /api/validate` - Validate tag
- `GET /api/git/status` - Get git status
- `POST /api/git/commit` - Commit changes

## Technology Stack

- **SvelteKit** - Full-stack framework
- **TailwindCSS** - Styling
- **Fuse.js** - Fuzzy search
- **js-yaml** - YAML parsing
- **TypeScript** - Type safety

## License

MIT
