<script>
  import { selectedCategory } from '$lib/stores/filters.js';
  import { categoryCounts } from '$lib/stores/tags.js';

  const categories = [
    { id: 'Concept', color: 'purple' },
    { id: 'Library', color: 'blue' },
    { id: 'Language', color: 'pink' },
    { id: 'Domain', color: 'teal' },
    { id: 'Constraint', color: 'orange' },
    { id: 'Task', color: 'lime' },
    { id: 'Agentic', color: 'cyan' },
    { id: 'Context', color: 'violet' }
  ];
</script>

<aside class="w-64 bg-white border-r border-gray-200 p-4">
  <h2 class="text-sm font-semibold text-gray-500 uppercase mb-4">Categories</h2>

  <nav class="space-y-1">
    {#each categories as category}
      <button
        on:click={() => selectedCategory.set(category.id)}
        class="w-full text-left px-3 py-2 rounded-lg transition-colors {$selectedCategory === category.id
          ? 'bg-blue-50 text-blue-700 font-medium'
          : 'text-gray-700 hover:bg-gray-50'}"
      >
        <span class="flex items-center justify-between">
          <span>{category.id}</span>
          <span class="text-sm text-gray-500">
            {$categoryCounts[category.id] || 0}
          </span>
        </span>
      </button>
    {/each}
  </nav>
</aside>
