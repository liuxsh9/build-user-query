<script>
  import { openEditor } from '$lib/stores/ui.js';

  export let tags = [];
</script>

<div class="bg-white rounded-lg border border-gray-200 overflow-hidden">
  <table class="w-full">
    <thead class="bg-gray-50">
      <tr>
        <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
        <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
        <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Subcategory</th>
        <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Difficulty</th>
        <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-200">
      {#each tags as tag (tag.id)}
        <tr class="hover:bg-gray-50 cursor-pointer" on:click={() => openEditor(tag)}>
          <td class="px-4 py-3 text-sm text-gray-900">{tag.name}</td>
          <td class="px-4 py-3 text-sm text-gray-500">{tag.id}</td>
          <td class="px-4 py-3 text-sm text-gray-500">{tag.subcategory || '-'}</td>
          <td class="px-4 py-3 text-sm">
            {#if tag.difficulty}
              <span class="px-2 py-1 text-xs rounded {
                tag.difficulty === 'basic' ? 'bg-green-100 text-green-800' :
                tag.difficulty === 'intermediate' ? 'bg-amber-100 text-amber-800' :
                'bg-red-100 text-red-800'
              }">
                {tag.difficulty}
              </span>
            {:else}
              -
            {/if}
          </td>
          <td class="px-4 py-3 text-sm">
            <button class="text-blue-600 hover:text-blue-700" on:click|stopPropagation={() => openEditor(tag)}>
              Edit
            </button>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>

  {#if tags.length === 0}
    <div class="text-center py-12 text-gray-500">
      No tags found
    </div>
  {/if}
</div>
