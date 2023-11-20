<script>
    export let visible=true;

    import { getModel } from "$lib/model.js";
    import { getConnection } from "$lib/connection.js";
    import { onDestroy } from "svelte";

    const model = getModel();

    let presets = {};
    let cur_preset;

    const unsubscribes = [];
    unsubscribes.push(model.presets.subscribe((val)=>{
        presets = val;
    }));
    unsubscribes.push(model.cur_preset.subscribe((val)=>{
        cur_preset = val;
    }));

    onDestroy(()=>{
        for(let i in unsubscribes) unsubscribes[i]();
    });

    let category_sel;
    let group_sel;
    let group_voices = [];
    function select_group(category, groupname){
        category_sel = category;
        group_sel = groupname
        group_voices = presets[category][groupname];
    }

    function select_voice(voicename){
        model.load_voice(category_sel, group_sel, voicename);
    }

</script>

<style>
    #main{
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background-color: rgba(0, 0, 0, 0.6);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 999;
    }

    #main-window{
        background-color: #333;
        border: 2px solid #111;
        box-shadow: 0 0 50px 10px black;
        padding: 14px 20px;
        text-align: center;
    }

    #presets-container{
        display: grid;
        grid-template-columns: 200px 200px;
        text-align: center;
        background-color: #252729;
        padding: 5px;
        overflow: hidden;
    }

    #presets-container > .list{
        overflow-y: scroll;
        max-height: 400px;
        display: grid;
        gap: 4px;
    }

    .group-section{
        border: 1px solid black;
        background-color: rgba(255, 255, 255, 0.1);
    }

    .group-section>.section-header{
        font-style: italic;
        background-color: rgba(0, 0, 0, 0.3);
    }

    .selectable{
        padding: 4px 8px;
        cursor: pointer;
    }

    .selectable.selected{
        background-color: rgba(255, 255, 255, 0.3);
    }
</style>

<div id="main" on:click={()=>{visible=false;}} style="display: {visible ? "flex" : "none"};">
    <div id="main-window" on:click|preventDefault|stopPropagation={()=>{}}>
        <div>Presets</div>
        <div id="presets-main">
            <div id="presets-container">
                <div>Groups</div>
                <div>Voices</div>
                <div id="groups-container" class="list">
                    {#each Object.keys(presets) as category}
                        <div class="group-section">
                            <div class="section-header">{category}</div>
                            {#each Object.keys(presets[category]) as groupname}
                                <div class="selectable{group_sel==groupname?" selected" : ""}" on:click={()=>{select_group(category, groupname)}}>{groupname}</div>
                            {/each}
                        </div>
                    {/each}
                </div>
                <div id="voices-container" class="list">
                    {#each group_voices as voicename}
                        <div class="selectable" on:click={()=>{select_voice(voicename)}}>{voicename}</div>
                    {/each}
                </div>
            </div>
        </div>
    </div>
</div>