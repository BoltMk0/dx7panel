<script>
    import {getModel} from "$lib/model.js";
    import {getConnection} from "$lib/connection.js";
    import {MESSAGE_ID} from "$lib/const.js";
    import { createEventDispatcher, onDestroy } from "svelte";

    const model = getModel();
    const dispatcher = createEventDispatcher();

    let user_bank_data;
    let preset_bank_data;

    let category = 'preset';
    let bank_idx = 0;
    let voice_idx = 0;


    const unsubscribes = [];
    unsubscribes.push(model.user_banks.subscribe(val=>{user_bank_data = val;}));
    unsubscribes.push(model.preset_banks.subscribe(val=>{preset_bank_data = val;}));
    unsubscribes.push(model.cur_bank_cat.subscribe(val=>{category = val;}));
    unsubscribes.push(model.cur_bank_idx.subscribe(val=>{
        bank_idx = val;
    }));
    unsubscribes.push(model.cur_voice_idx.subscribe(val=>{voice_idx = val;}));

    onDestroy(()=>{
        for(const u of unsubscribes) u();
    });

    $: shown_bank_idx = category === 'preset' ? bank_idx : preset_bank_data.length + bank_idx;
    $: console.log(category, bank_idx, shown_bank_idx);

    function onVoiceBtnPress(i){
        let cat = shown_bank_idx > preset_bank_data.length ? 'user' : 'preset';
        let bi = shown_bank_idx > preset_bank_data.length ? shown_bank_idx - preset_bank_data.length : shown_bank_idx;
        getConnection().send([MESSAGE_ID.VOICE_LOAD, [cat, bi, i]]);
    }

    function bankShift(amt){
        shown_bank_idx = Math.max(0, Math.min(preset_bank_data.length + user_bank_data.length - 1, shown_bank_idx+amt));
    }

    $: bank = shown_bank_idx >= preset_bank_data.length ? user_bank_data[shown_bank_idx - preset_bank_data.length] : preset_bank_data[shown_bank_idx];
</script>
<style>
.bank-view-voice-btn-container{
    display: grid;
    grid-template-columns: repeat(16, min-content);
    justify-content: center;
    gap:2px;
    margin-bottom: 10px;
}

.bank-view-voice-btn-container > .bank-view-voice-btn{
    text-align: center;
    width: 45px;
    padding:3px 6px;
    background-color: #0f8465;
    cursor: pointer;
    text-wrap: nowrap;
}
.bank-view-voice-btn-container > .bank-view-voice-btn.selected{
    background-color: #34c29c;
}

.bank-view-header{
    display: flex;
    gap: 3px;
    justify-content: center;
    padding: 5px;
}

.bank-view-title{
    width: 250px;
    text-align: center;
    text-wrap: nowrap;
    background-color: black;
    padding:3px;
    cursor: pointer;
}

.bank-view-header > button{
    width: 45px;
    background-color: #0f8465;
    color: white;
    font-size:large;
}
</style>




<div class='bank-view-main'>
    <div class='bank-view-header'>
        <button on:click={()=>{bankShift(-10)}}>-10</button>
        <button on:click={()=>{bankShift(-1)}}>-</button>
        <div>
            <div style="text-align: center; opacity: 0.5">Bank</div>
            <div class='bank-view-title' on:click={()=>{dispatcher('showpresets')}}>{shown_bank_idx >= preset_bank_data.length ? "U" : "P"}{shown_bank_idx+1}: {bank?.name}</div>
        </div>
        <button on:click={()=>{bankShift(1)}}>+</button>
        <button on:click={()=>{bankShift(10)}}>+10</button>
    </div>
    <div class='bank-view-voice-btn-container'>
        {#each {length: 32} as _, i}
            <div class='bank-view-voice-btn{ (shown_bank_idx >= preset_bank_data.length ? shown_bank_idx - preset_bank_data.length : shown_bank_idx) === bank_idx && voice_idx === i ? " selected" : ""}' on:click={()=>{onVoiceBtnPress(i);}}>
                <div>{i+1}</div>
                <div style="font-size: x-small; overflow: hidden">{bank?.voices[i]}</div>
            </div>
        {/each}
    </div>
</div>