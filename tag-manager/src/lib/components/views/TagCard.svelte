<script>
  import { openEditor } from '$lib/stores/ui.js';

  export let tag;

  const difficultyColors = {
    basic: 'bg-green-100 text-green-800',
    intermediate: 'bg-amber-100 text-amber-800',
    advanced: 'bg-red-100 text-red-800'
  };
</script>

<div class="bg-white rounded-lg p-4 shadow-sm border border-gray-200 hover:shadow-md transition-shadow group">
  <div class="flex items-start justify-between">
    <div class="flex-1">
      <h3 class="font-semibold text-gray-900">{tag.name}</h3>
      <p class="text-sm text-gray-500 mt-1">{tag.id}</p>

      {#if tag.difficulty}
        <span class="inline-block mt-2 px-2 py-1 text-xs font-medium rounded {difficultyColors[tag.difficulty] || 'bg-gray-100 text-gray-800'}">
          {tag.difficulty}
        </span>
      {/if}

      {#if tag.aliases && tag.aliases.length > 0}
        <p class="text-xs text-gray-400 mt-2">{tag.aliases[0]}</p>
      {/if}
    </div>

    <div class="opacity-0 group-hover:opacity-100 transition-opacity flex gap-2">
      <button
        on:click={() => openEditor(tag)}
        class="text-blue-600 hover:text-blue-700 text-sm"
      >
        Edit
      </button>
    </div>
  </div>
</div>
