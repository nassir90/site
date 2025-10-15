<script>
    import Visualization from '$lib/components/Visualization.svelte';
    import TextOverlay from '$lib/components/TextOverlay.svelte';
    import Content from '$lib/components/Content.svelte';
</script>

<svelte:head>
    <title>Chinaza Uzoukwu</title>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&display=swap" rel="stylesheet">
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css"
      crossorigin="anonymous"
      referrerpolicy="no-referrer"
    />
</svelte:head>

<main>
    <div id="visualization-container">
        <Visualization />
        <TextOverlay />
    </div>
    <Content />
</main>

<style>
    :global(body) {
        margin: 0;
        background-color: #111111;
    }

    #visualization-container {
        height: 100vh;
        position: relative;
        display: flex;
        flex-direction: column;
    }

    @media (max-width: 768px) {
        #visualization-container {
            height: auto;
        }
    }
</style>
