// 5.10 Git state management
import { writable } from 'svelte/store';

export const gitStatus = writable({
  hasChanges: false,
  changes: [],
  error: null
});

export const recentCommits = writable([]);
export const isCommitting = writable(false);

// Load git status
export async function loadGitStatus() {
  try {
    const response = await fetch('/api/git/status');
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to load git status');
    }

    gitStatus.set(data);
  } catch (err) {
    gitStatus.set({
      hasChanges: false,
      changes: [],
      error: err.message
    });
  }
}

// Commit changes
export async function commitChanges(message) {
  isCommitting.set(true);

  try {
    const response = await fetch('/api/git/commit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to commit changes');
    }

    // Refresh git status
    await loadGitStatus();

    return data;
  } finally {
    isCommitting.set(false);
  }
}
