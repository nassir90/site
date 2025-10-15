<script lang="ts">
    let { children } = $props();
    export const prerender = true;
</script>

<svelte:head>
	<link rel="icon" href="/favicon.png" />
</svelte:head>

{@render children?.()}
