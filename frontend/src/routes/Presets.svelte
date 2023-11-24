<script>
    export let visible=true;

    import { getModel } from "$lib/model.js";
    import { getConnection } from "$lib/connection.js";
    import { onDestroy } from "svelte";

    import { MESSAGE_ID } from "$lib/const.js";
    import UploadBankOverlay from "./UploadBankOverlay.svelte";

    const model = getModel();

    let preset_banks;
    let user_banks;
    
    let cur_bank_idx;
    let cur_voice_idx;
    let cur_bank_cat = 'preset';

    $: selected_bank_idx = cur_bank_idx;
    $: selected_bank_cat = cur_bank_cat;
    $: selected_bank = selected_bank_cat === 'user' ? user_banks[selected_bank_idx] : preset_banks[selected_bank_idx];

    const unsubscribes = [];
    unsubscribes.push(model.cur_bank_cat.subscribe((val)=>{
        cur_bank_cat = val;
    }));
    unsubscribes.push(model.preset_banks.subscribe((val)=>{
        preset_banks = val;
    }));
    unsubscribes.push(model.user_banks.subscribe((val)=>{
        user_banks = val;
    }));
    unsubscribes.push(model.cur_bank_idx.subscribe((val)=>{
        cur_bank_idx = val;
    }));
    unsubscribes.push(model.cur_voice_idx.subscribe((val)=>{
        cur_voice_idx = val;
    }));

    onDestroy(()=>{
        for(let i of unsubscribes) i();
    });

    const DELETE_BTN_STAGES = ['Delete Bank', 'Are you sure?', 'Super duper sure??']

    let deleteBankVal = 0;
    $: deleteBankText = DELETE_BTN_STAGES[deleteBankVal]

    function onDeleteBank(){
        deleteBankVal++;
        if(deleteBankVal >= DELETE_BTN_STAGES.length){
            deleteBankVal = 0;
            getConnection().send([MESSAGE_ID.DELETE_USER_BANK, [selected_bank_cat, selected_bank_idx]]);
        }
    }

    let newBankInput;
    let newBankInputContainer;

    function select_group(category, groupIdx){
        selected_bank_cat = category;
        selected_bank_idx = groupIdx;
        deleteBankVal = 0;
    }

    function select_voice(category, bankIdx, voiceIdx){
        getConnection().send([MESSAGE_ID.VOICE_LOAD, [category, bankIdx, voiceIdx]]);
    }

    function onNewBank(){
        newBankInputContainer.style.display = 'grid';
        newBankInput.value = '';
        newBankInput.select();
    }

    function onSubmitBank(){
        newBankInputContainer.style.display = null;
        const newBankName = newBankInput.value;
        if(newBankName.length > 0){
            getConnection().send([MESSAGE_ID.NEW_USER_BANK, newBankName]);
        }
    }

    let _showBankUpload = false;

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
        z-index: 100;
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

    .user-bank{
        display: flex;
        gap: 5px;
    }

    .bank-label{
        text-wrap: nowrap;
        overflow: hidden;
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
                    <div class="group-section">
                        <div class="section-header">Preset</div>
                        {#each preset_banks as bank, i (bank.name)}
                        <div class="selectable{selected_bank_cat === 'preset' && selected_bank_idx === i ? ' selected' : ''}" on:click={()=>{select_group('preset', i)}}>
                            <div class='bank-label'>{bank.name}</div>
                        </div>
                        {/each}
                    </div>
                    <div class="group-section">
                        <div class="section-header">User</div>
                        {#each user_banks as bank, i (bank.name)}
                        <div class="user-bank selectable{selected_bank_cat === 'user' && selected_bank_idx === i ? ' selected' : ''}" on:click={()=>{select_group('user', i)}}>
                            <div class='bank-label'>{bank.name}</div>
                        </div>
                        {/each}

                        <div bind:this={newBankInputContainer} class="vg-input-container">
                            <input bind:this={newBankInput} type='text'/>
                            <button on:click={onSubmitBank}>Submit</button>
                        </div>
                        <button style="width: 100%;" on:click={onNewBank}>New...</button>
                        <button style="width: 100%;" on:click={()=>{_showBankUpload=true;}}>Upload...</button>
                    </div>
                </div>

                <div id="voices-container" class="list">
                    {#if selected_bank !== undefined}
                    {#each selected_bank.voices as voicename, i}
                    <div class="selectable{cur_bank_idx === selected_bank_idx && cur_voice_idx === i ? ' selected' : ''}" on:click={()=>{select_voice(selected_bank_cat, selected_bank_idx, i)}} style="text-align: left;">{voicename.replaceAll('_', ' ')}</div>
                    {/each}
                    {/if}
                    {#if selected_bank_cat === 'user'}
                    <button on:click={onDeleteBank}>{deleteBankText}</button>
                    {/if}
                </div>
            </div>
        </div>
    </div>
</div>
{#if _showBankUpload}
<UploadBankOverlay on:close={()=>{_showBankUpload = false;}}/>
{/if}