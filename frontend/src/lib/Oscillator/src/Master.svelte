<script>
    export let idx;
    export let enabled;
    import VertSwitch from "../../VertSwitch.svelte";
</script>
<style>
    #main{
        display: grid;
        grid-template-columns: auto fit-content(10px);
        justify-content: center;
        align-items: center;
    }
    #text{
        padding: 5px;
        font-size: x-large;
        opacity: 0.5;
    }
</style>

<div id="main">
    <div id="toggle">
        <VertSwitch bind:checked={enabled} />
    </div>
    <div id="text">{idx+1}</div>
</div>