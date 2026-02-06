// 5.1-5.6 Tag state management
import { writable, derived } from 'svelte/store';

// 5.1 Raw tag data
export const allTags = writable([]);
export const loading = writable(false);
export const error = writable(null);

// 5.2 Load tags from API
export async function loadTags() {
  loading.set(true);
  error.set(null);

  try {
    const response = await fetch('/api/tags');
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to load tags');
    }

    allTags.set(data.tags);
  } catch (err) {
    error.set(err.message);
    console.error('Failed to load tags:', err);
  } finally {
    loading.set(false);
  }
}

// 5.3 Tags grouped by category
export const tagsByCategory = derived(allTags, $allTags => {
  const grouped = {};

  for (const tag of $allTags) {
    if (!grouped[tag.category]) {
      grouped[tag.category] = [];
    }
    grouped[tag.category].push(tag);
  }

  return grouped;
});

// 5.4 Category counts
export const categoryCounts = derived(tagsByCategory, $grouped => {
  const counts = {};
  for (const [category, tags] of Object.entries($grouped)) {
    counts[category] = tags.length;
  }
  return counts;
});

// 5.5 Create tag with optimistic updates
export async function createTag(category, tagData) {
  const newTag = { ...tagData, category };

  // Optimistic update
  allTags.update(tags => [...tags, newTag]);

  try {
    const response = await fetch('/api/tags', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category, tag: tagData })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to create tag');
    }

    // Replace optimistic tag with server response
    allTags.update(tags =>
      tags.map(t => t.id === newTag.id && t.category === category ? data.tag : t)
    );

    return data.tag;
  } catch (err) {
    // 5.6 Rollback on error
    allTags.update(tags => tags.filter(t => t !== newTag));
    throw err;
  }
}

// 5.5 Update tag with optimistic updates
export async function updateTag(category, id, updates) {
  let previousTag = null;

  // Optimistic update
  allTags.update(tags => {
    return tags.map(t => {
      if (t.category === category && t.id === id) {
        previousTag = { ...t };
        return { ...t, ...updates };
      }
      return t;
    });
  });

  try {
    const response = await fetch(`/api/tags/${category}/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to update tag');
    }

    // Replace with server response
    allTags.update(tags =>
      tags.map(t => t.category === category && t.id === id ? data.tag : t)
    );

    return data.tag;
  } catch (err) {
    // 5.6 Rollback on error
    if (previousTag) {
      allTags.update(tags =>
        tags.map(t => t.category === category && t.id === id ? previousTag : t)
      );
    }
    throw err;
  }
}

// 5.5 Delete tag with optimistic updates
export async function deleteTag(category, id) {
  let previousTags = [];

  // Optimistic update
  allTags.update(tags => {
    previousTags = [...tags];
    return tags.filter(t => !(t.category === category && t.id === id));
  });

  try {
    const response = await fetch(`/api/tags/${category}/${id}`, {
      method: 'DELETE'
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to delete tag');
    }

    return data;
  } catch (err) {
    // 5.6 Rollback on error
    allTags.set(previousTags);
    throw err;
  }
}
