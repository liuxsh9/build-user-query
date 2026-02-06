// 6.1-6.5 Search service wrapper around Fuse.js
import Fuse from 'fuse.js';

// 6.2 Configure Fuse.js with weighted keys
const fuseOptions = {
  keys: [
    { name: 'name', weight: 2 },
    { name: 'id', weight: 1.5 },
    { name: 'aliases', weight: 1 },
    { name: 'description', weight: 0.5 }
  ],
  threshold: 0.3, // 6.3 Fuzzy threshold for typo tolerance
  includeScore: true,
  ignoreLocation: true
};

let fuseInstance = null;

// 6.4 Create search index
export function createSearchIndex(tags) {
  fuseInstance = new Fuse(tags, fuseOptions);
  return fuseInstance;
}

// 6.5 Search function returning ranked results
export function search(query, tags) {
  if (!query || !query.trim()) {
    return tags;
  }

  // Create or update index if needed
  if (!fuseInstance || fuseInstance._docs !== tags) {
    createSearchIndex(tags);
  }

  const results = fuseInstance.search(query);
  return results.map(result => result.item);
}

export { fuseOptions };
