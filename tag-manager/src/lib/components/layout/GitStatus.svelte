<script>
  import { onMount } from 'svelte';
  import { gitStatus, loadGitStatus } from '$lib/stores/git.js';

  onMount(() => {
    loadGitStatus();
  });
</script>

<div class="fixed bottom-4 right-4 bg-white rounded-lg shadow-lg p-4 border border-gray-200">
  <div class="flex items-center gap-2">
    {#if $gitStatus.hasChanges}
      <span class="w-2 h-2 bg-yellow-500 rounded-full"></span>
      <span class="text-sm text-gray-700">
        {$gitStatus.changes.length} uncommitted change{$gitStatus.changes.length !== 1 ? 's' : ''}
      </span>
    {:else}
      <span class="w-2 h-2 bg-green-500 rounded-full"></span>
      <span class="text-sm text-gray-700">No changes</span>
    {/if}
  </div>
</div>
