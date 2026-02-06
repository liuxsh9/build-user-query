// 5.9 UI state management
import { writable } from 'svelte/store';

// Modal state
export const isEditorOpen = writable(false);
export const selectedTag = writable(null);
export const editorMode = writable('create'); // 'create' | 'edit'

// Toast notifications
export const toasts = writable([]);

let toastId = 0;

export function showToast(message, type = 'info') {
  const id = toastId++;
  const toast = { id, message, type };

  toasts.update(current => [...current, toast]);

  // Auto-dismiss after 5 seconds
  setTimeout(() => {
    removeToast(id);
  }, 5000);

  return id;
}

export function removeToast(id) {
  toasts.update(current => current.filter(t => t.id !== id));
}

// Editor helpers
export function openEditor(tag = null) {
  selectedTag.set(tag);
  editorMode.set(tag ? 'edit' : 'create');
  isEditorOpen.set(true);
}

export function closeEditor() {
  isEditorOpen.set(false);
  selectedTag.set(null);
}
