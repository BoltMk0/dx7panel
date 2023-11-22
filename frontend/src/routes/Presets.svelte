<script>
    export let visible=true;

    import { getModel } from "$lib/model.js";
    import { getConnection } from "$lib/connection.js";
    import { onDestroy } from "svelte";

    import { MESSAGE_ID } from "$lib/const.js";

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



    const DELETE_BTN_STAGES = ['Delete', 'Are you sure?', 'Super duper sure??']
    let deleteBtnVal = 0;
    let deleteBankVal = 0;
    $: deleteBtnText = DELETE_BTN_STAGES[deleteBtnVal]
    $: deleteBankText = DELETE_BTN_STAGES[deleteBankVal]

    function onDeleteVoice(){
        deleteBtnVal++;
        deleteBankVal = 0;
        if(deleteBtnVal >= DELETE_BTN_STAGES.length){
            deleteBtnVal = 0;
            // TODO: delete voice
        }
    }

    function onDeleteBank(){
        deleteBankVal++;
        deleteBtnVal = 0;
        if(deleteBankVal >= DELETE_BTN_STAGES.length){
            deleteBankVal = 0;
            // TODO: delete group
        }
    }

    let newVoiceInput;
    let newVoiceInputContainer;
    let newBankInput;
    let newBankInputContainer;

    let category_sel;
    let group_sel;
    let voice_sel;
    let group_voices = [];

    function select_group(category, groupname){
        category_sel = category;
        group_sel = groupname
        group_voices = presets[category][groupname];
        group_voices.sort();
        deleteBtnVal = 0;
        deleteBankVal = 0;

    }

    function select_voice(voicename){

        voice_sel = voicename;
        model.load_voice(category_sel, group_sel, voicename);
        deleteBtnVal = 0;
        deleteBankVal = 0;
    }

    function onNewBank(){
        group_sel = undefined;
        newBankInputContainer.style.display = 'grid';
        newBankInput.value = '';
        newBankInput.select();
    }

    function onSubmitBank(ev){
        newBankInputContainer.style.display = null;
        const newBankName = newBankInput.value;
        if(newBankName.length > 0){
            if(presets.user[newBankName] === undefined){
                getConnection().send([MESSAGE_ID.NEW_GROUP, newBankName]);
            }
        }
    }

    function onNewVoice(){
        group_sel = undefined;
        newVoiceInputContainer.style.display = 'grid';
        newVoiceInput.value = '';
        newVoiceInput.select();
    }

    function onSubmitVoice(ev){
        newVoiceInputContainer.style.display = null;
        const newBankName = newVoiceInput.value;
        newVoiceInput.value = '';
        if(newBankName.length > 0){
            if(presets.user[newBankName] === undefined){
                // TODO: Request new group
            }
        }
    }

</script>

<style>
    #main{
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background-color: rgba(0, 0, 0, 0.6);
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
        overflow: hidden;
        display: grid;
        grid-template-rows: min-content 1fr;
        max-height: 100%;
    }

    #presets-main{
        overflow: hidden;
        display: grid;
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
        height: 100%;
        display: grid;
        gap: 2px;
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

    .vg-input-container{
        display: none;
        grid-template-columns: 141px min-content;
    }

</style>

<div id="main" on:click={()=>{visible=false;}} style="display: {visible ? "flex" : "none"};">
    <div id="main-window" on:click|preventDefault|stopPropagation={()=>{}}>
        <div>Presets</div>
        <div id="presets-main">
            <div id="presets-container">
                <div>Bank</div>
                <div>Voice</div>
                <div id="groups-container" class="list">
                    {#each Object.keys(presets).filter(k=>k!=='user') as category}
                        <div class="group-section">
                            <div class="section-header">{category}</div>
                            {#each Object.keys(presets[category]) as groupname}
                                <div class="selectable{group_sel==groupname?" selected" : ""}" on:click={()=>{select_group(category, groupname)}}>{groupname}</div>
                            {/each}
                        </div>
                    {/each}
                    <div class='group-section'>
                        <div class="section-header">user</div>
                            {#each Object.keys(presets.user) as groupname}
                                <div class="selectable{group_sel==groupname?" selected" : ""}" on:click={()=>{select_group("user", groupname)}}>{groupname}</div>
                                {#if group_sel === groupname }
                                    <button style="width: 100%;" on:click={onDeleteBank}>{deleteBankText}</button>
                                {/if}
                            {/each}
                        <div bind:this={newBankInputContainer} class="vg-input-container">
                            <input bind:this={newBankInput} type='text'/>
                            <button on:click={onSubmitBank}>Submit</button>
                        </div>
                        <button style="width: 100%;" on:click={onNewBank}>New...</button>
                    </div>
                </div>
                <div id="voices-container" class="list">
                    {#each group_voices as voicename}
                        <div class="selectable{voice_sel === voicename ? ' selected' : ''}" on:click={()=>{select_voice(voicename)}} style="text-align: left;">{voicename.replaceAll('_', ' ')}</div>
                        {#if voice_sel === voicename && category_sel.toLowerCase() === 'user'}
                            <button on:click={onDeleteVoice}>{deleteBtnText}</button>
                        {/if}
                    {/each}
                    {#if group_sel && category_sel.toLowerCase() === 'user'}
                        <div class="vg-input-container" bind:this={newVoiceInputContainer}>
                            <input bind:this={newVoiceInput} type='text'/>
                            <button on:click={onSubmitVoice}>Submit</button>
                        </div>
                        <button disabled={group_voices.length >= 32} on:click={onNewVoice}>New...</button>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</div>