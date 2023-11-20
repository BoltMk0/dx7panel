<script>
    import Switch from "../../Switch.svelte";
    export let checked=false;

</script>
<style>
    #main{
        height: 100%;
        display: flex;
        justify-content: center;
    }

    #container{
        display: flex; 
        gap: 10px;
        align-items: center;
    }

</style>


<div class="osc-section" id="main">
    <div id="container">
        <div>Ratio</div>
        <Switch inverted bind:checked/>
        <div>Fixed</div>
    </div>
</div>