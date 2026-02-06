<script>
  import TopBar from '$lib/components/layout/TopBar.svelte';
  import CategoryNav from '$lib/components/layout/CategoryNav.svelte';
  import GitStatus from '$lib/components/layout/GitStatus.svelte';
  import TagGrid from '$lib/components/views/TagGrid.svelte';
  import TagTable from '$lib/components/views/TagTable.svelte';
  import TagEditor from '$lib/components/editor/TagEditor.svelte';
  import { filteredTags, selectedCategory } from '$lib/stores/filters.js';
</script>

<div class="flex flex-col h-screen">
  <TopBar />

  <div class="flex flex-1 overflow-hidden">
    <CategoryNav />

    <main class="flex-1 overflow-auto p-6">
      <div class="mb-4">
        <h2 class="text-xl font-semibold text-gray-900">
          {$selectedCategory} Tags ({$filteredTags.length})
        </h2>
      </div>

      {#if $filteredTags.length < 100}
        <TagGrid tags={$filteredTags} />
      {:else}
        <TagTable tags={$filteredTags} />
      {/if}
    </main>
  </div>

  <GitStatus />
  <TagEditor />
</div>
