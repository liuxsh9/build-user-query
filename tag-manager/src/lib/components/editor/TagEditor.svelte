<script>
  import { isEditorOpen, selectedTag, editorMode, closeEditor } from '$lib/stores/ui.js';
  import { createTag, updateTag } from '$lib/stores/tags.js';
  import { showToast } from '$lib/stores/ui.js';

  let formData = {
    id: '',
    name: '',
    category: 'Concept',
    subcategory: '',
    difficulty: 'basic',
    source: 'manual',
    aliases: [],
    description: '',
    language_scope: []
  };

  $: if ($selectedTag && $isEditorOpen) {
    formData = { ...$selectedTag };
  }

  async function handleSubmit() {
    try {
      if ($editorMode === 'create') {
        await createTag(formData.category, formData);
        showToast('Tag created successfully', 'success');
      } else {
        await updateTag(formData.category, formData.id, formData);
        showToast('Tag updated successfully', 'success');
      }
      closeEditor();
    } catch (error) {
      showToast(error.message, 'error');
    }
  }
</script>

{#if $isEditorOpen}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" on:click={closeEditor}>
    <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto" on:click|stopPropagation>
      <h2 class="text-2xl font-bold mb-4">
        {$editorMode === 'create' ? 'Create New Tag' : 'Edit Tag'}
      </h2>

      <form on:submit|preventDefault={handleSubmit} class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">ID</label>
          <input
            type="text"
            bind:value={formData.id}
            disabled={$editorMode === 'edit'}
            class="w-full px-3 py-2 border rounded-lg"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Name</label>
          <input
            type="text"
            bind:value={formData.name}
            class="w-full px-3 py-2 border rounded-lg"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Category</label>
          <select bind:value={formData.category} class="w-full px-3 py-2 border rounded-lg" disabled={$editorMode === 'edit'}>
            <option>Concept</option>
            <option>Library</option>
            <option>Language</option>
            <option>Domain</option>
            <option>Constraint</option>
            <option>Task</option>
            <option>Agentic</option>
            <option>Context</option>
          </select>
        </div>

        {#if formData.category === 'Concept'}
          <div>
            <label class="block text-sm font-medium mb-1">Subcategory</label>
            <select bind:value={formData.subcategory} class="w-full px-3 py-2 border rounded-lg">
              <option>Fundamentals</option>
              <option>Advanced</option>
              <option>Engineering</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-1">Difficulty</label>
            <select bind:value={formData.difficulty} class="w-full px-3 py-2 border rounded-lg">
              <option value="basic">Basic</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
        {/if}

        <div>
          <label class="block text-sm font-medium mb-1">Source</label>
          <select bind:value={formData.source} class="w-full px-3 py-2 border rounded-lg">
            <option value="manual">Manual</option>
            <option value="curated-list">Curated List</option>
            <option value="educational-sources">Educational Sources</option>
            <option value="TIOBE">TIOBE</option>
            <option value="GitHub">GitHub</option>
          </select>
        </div>

        <div class="flex gap-2 justify-end">
          <button
            type="button"
            on:click={closeEditor}
            class="px-4 py-2 text-gray-700 border rounded-lg hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            {$editorMode === 'create' ? 'Create' : 'Save'}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}
