<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { loadTags } from '$lib/stores/tags.js';

	let { children } = $props();

	onMount(() => {
		loadTags();
	});
</script>

<div class="min-h-screen bg-gray-50">
	{@render children()}
</div>
