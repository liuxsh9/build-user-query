<script>
  import { selectedCategory, searchQuery } from '$lib/stores/filters.js';
  import { openEditor } from '$lib/stores/ui.js';
</script>

<header class="bg-white border-b border-gray-200 px-6 py-4">
  <div class="flex items-center justify-between">
    <h1 class="text-2xl font-bold text-gray-900">🏷️ Tag Manager</h1>

    <div class="flex items-center gap-4">
      <input
        type="text"
        placeholder="Search tags..."
        bind:value={$searchQuery}
        class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <button
        on:click={() => openEditor()}
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        + New Tag
      </button>
    </div>
  </div>
</header>
