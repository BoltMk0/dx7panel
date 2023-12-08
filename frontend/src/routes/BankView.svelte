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

    $: shown_bank_category = category;
    $: shown_bank_idx = bank_idx;
    $: console.log(category, bank_idx, shown_bank_idx);

    let storeMode = false;

    function onVoiceBtnPress(i){
        if(storeMode){
            getConnection().send([MESSAGE_ID.VOICE_STORE, [shown_bank_category, shown_bank_idx, i]]);
            storeMode = false;
        } else {
            getConnection().send([MESSAGE_ID.VOICE_LOAD, [shown_bank_category, shown_bank_idx, i]]);
        }
    }

    function bankShift(amt){
        shown_bank_idx+=amt;
        if(shown_bank_category === 'preset'){
            if(shown_bank_idx >= preset_bank_data.length){
                // We're going into user banks
                shown_bank_idx -= preset_bank_data.length;
                shown_bank_category = 'user';
                shown_bank_idx = Math.min(shown_bank_idx, user_bank_data.length);
            } else {
                shown_bank_idx = Math.max(0, shown_bank_idx);
            }
        } else if(shown_bank_category === 'user'){
            if(shown_bank_idx < 0){
                // Going down into the preset banks
                shown_bank_idx += preset_bank_data.length;
                shown_bank_category = 'preset';
                shown_bank_idx = Math.max(0, shown_bank_idx);
            } else{
                shown_bank_idx = Math.min(user_bank_data.length-1, shown_bank_idx);
            }
        }
    }

    function onStore(){
        storeMode = !storeMode;
    }

    function onInit(){
        getConnection().send([MESSAGE_ID.VOICE_INIT]);
    }

    $: bank = (shown_bank_category == 'user' ? user_bank_data : preset_bank_data)[shown_bank_idx];

</script>
<style>
.bank-view-main{
    display: grid;
    justify-content: center;
}
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
    position: relative;
}

.bank-view-title{
    width: 250px;
    text-align: center;
    text-wrap: nowrap;
    background-color: black;
    padding:3px;
    cursor: pointer;
}

.function-btn-container{
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    padding: 5px 0;
}

.function-btn-container > button{
    width: 80px;
    background-color: orange;
    height: 100%;
    padding: 10px;
    font-size: large;
    color: white;
}

.function-btn-container > button:disabled{
    opacity: 0.5;
}

.bank-view-header > button{
    width: 45px;
    background-color: #0f8465;
    color: white;
    font-size:large;
}

@keyframes flashing {
  0% {
    background-color: #0f8465;
  }
  50% {
    background-color: #34c29c;
  }
  100% {
    background-color: #0f8465;
  }
}

.flashing{
    animation: flashing 250ms infinite;
}

</style>




<div class='bank-view-main'>
    <div style="width: min-content;">
        <div class='bank-view-header'>
            <div class='function-btn-container'>
                <button class='store-btn{storeMode ? " flashing" : ""}' on:click|stopPropagation={onStore} disabled={shown_bank_idx < preset_bank_data.length}>Store</button>
                <button class='store-btn' on:click={onInit}>Init</button>
            </div>

            <button on:click={()=>{bankShift(-10)}}>-10</button>
            <button on:click={()=>{bankShift(-1)}}>-</button>
            <div>
                <div style="text-align: center; opacity: 0.5; font-size: small;">Bank</div>
                <div class='bank-view-title' on:click={()=>{dispatcher('showpresets')}}>{shown_bank_category[0].toUpperCase()}{shown_bank_idx+1}: {bank?.name}</div>
            </div>
            <button on:click={()=>{bankShift(1)}}>+</button>
            <button on:click={()=>{bankShift(10)}}>+10</button>
        </div>
        <div class='bank-view-voice-btn-container'>
            {#each {length: 32} as _, i}
                <div class='bank-view-voice-btn{shown_bank_category === category && shown_bank_idx === bank_idx && voice_idx === i ? " selected" : ""}{storeMode ? " flashing" : ""}' on:click={()=>{onVoiceBtnPress(i);}}>
                    <div>{i+1}</div>
                    <div style="font-size: x-small; overflow: hidden">{bank?.voices[i]}</div>
                </div>
            {/each}
        </div>
    </div>
</div>

<svelte:window on:click={()=>{storeMode = false;}}/>