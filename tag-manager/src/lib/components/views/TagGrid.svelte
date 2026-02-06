<script>
  import TagCard from './TagCard.svelte';

  export let tags = [];
</script>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {#each tags as tag (tag.id)}
    <TagCard {tag} />
  {/each}
</div>

{#if tags.length === 0}
  <div class="text-center py-12 text-gray-500">
    No tags found
  </div>
{/if}
