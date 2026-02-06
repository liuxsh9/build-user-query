// 5.7-5.8 Filter state management
import { writable, derived } from 'svelte/store';
import { allTags } from './tags.js';
import { search } from '$lib/services/search.js';
import { sortTags } from '$lib/utils/sorting.js';

// 5.7 Filter stores
export const selectedCategory = writable('Concept');
export const searchQuery = writable('');
export const difficultyFilter = writable('all');
export const languageFilter = writable('all');
export const sortBy = writable('name'); // name, id, difficulty

// 5.8 Filtered tags derived store with Fuse.js integration
export const filteredTags = derived(
  [allTags, selectedCategory, searchQuery, difficultyFilter, languageFilter, sortBy],
  ([$allTags, $category, $search, $difficulty, $language, $sort]) => {
    let tags = $allTags.filter(t => t.category === $category);

    // Search filter with Fuse.js
    if ($search.trim()) {
      tags = search($search, tags);
    }

    // Difficulty filter
    if ($difficulty !== 'all') {
      tags = tags.filter(t => t.difficulty === $difficulty);
    }

    // Language filter
    if ($language !== 'all') {
      tags = tags.filter(t =>
        t.language_scope && t.language_scope.includes($language)
      );
    }

    // Sorting
    tags = sortTags(tags, $sort);

    return tags;
  }
);
