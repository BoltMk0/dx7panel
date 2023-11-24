<script>
    import { createEventDispatcher, onDestroy } from "svelte";
    import {showMessage} from "$lib/errorMessage.js";
    import {getModel} from "$lib/model.js";
    import {getConnection} from "$lib/connection.js";
    import {MESSAGE_ID} from "$lib/const.js";

    const dispatcher = createEventDispatcher();
    const model = getModel();

    const unsubscribes = [];

    onDestroy(()=>{
        for(const u of unsubscribes) u();
    });

    let userBankNames = [];
    let presetBankNames = [];
    unsubscribes.push(model.user_banks.subscribe(val=>{
        userBankNames = Array.from(val, v=>v.name);
    }));
    unsubscribes.push(model.preset_banks.subscribe(val=>{
        presetBankNames = Array.from(val, v=>v.name);
    }));

    $: bankNames = [...userBankNames, ...presetBankNames];
    

    let submit_btn;
    let bank_name_input;
    let bank_file_input;

    function onSubmit(){
        const reader = new FileReader();

        reader.onload = function(){
            const resultString = new TextDecoder().decode(reader.result);
            console.log(resultString.length);
            getConnection().send([MESSAGE_ID.BANK_UPLOAD, [curName, resultString]]);
            dispatcher('close');
        }

        reader.readAsArrayBuffer(bank_file_input.files[0]);
    }

    let curName = '';
    let curFileName = '';
    function onNameChange(){
        curName = bank_name_input.value.trim();
    }

    function checkHeader(b){
        return new Promise((resolve, reject)=>{
            const r = new FileReader();
            r.onload = function(){
                const chunk = new Uint8Array(r.result);
                if(chunk[0] !== 0b11110000) return reject('Invalid header - not sysex');
                if(chunk[3] !== 9) return reject('Invalid sysex format for DX7 voice bank');
                const dataSize = chunk[4] << 7 | chunk[5];
                if(dataSize !== 4096) return reject(`Invalid sysex data size for DX7 voice bank (got ${dataSize}, expected 4096)`);
                resolve();
            }
            r.readAsArrayBuffer(b.slice(0, 6));
        });
    }

    function getBankVoiceNames(file){
        return new Promise(async (resolve, reject)=>{
            checkHeader(file).then(()=>{
                const to_ret = [];
                const reader = new FileReader();
                const chunkSize = 128;
                

                let offset = 6;
                reader.onload = function(){
                    const chunk = reader.result;
                    const lastTenBytes = chunk.slice(-10);
                    const lastTenBytesString = new TextDecoder().decode(lastTenBytes);

                    to_ret.push(lastTenBytesString);
                    if(offset + chunkSize <= file.size) {
                        readNextChunk();
                    } else {
                        if(to_ret.length !== 32) return reject(`Not enough voices found in sysex (found ${to_ret.length})- incomplete?`)
                        return resolve(to_ret);
                    }
                }

                function readNextChunk() {
                    const blob = file.slice(offset, offset + chunkSize);
                    reader.readAsArrayBuffer(blob)
                    offset += chunkSize;
                }

                readNextChunk();
            }).catch(er=>{reject(er)});
        });
    }

    let bankVoiceNames;
    function onFileChange(){

        getBankVoiceNames(bank_file_input.files[0]).then(names=>{
            bankVoiceNames = names;
            curFileName = bank_file_input.files[0].name;
            curName = curFileName.split('.')[0];
            bank_name_input.value = curName;
            rejection_reason = check_for_rejection();
            console.log(rejection_reason);
        }).catch(er=>{
            bank_file_input.value = null;
            showMessage(er);
        });
    }
    
    function check_for_rejection(){
        if(curFileName === undefined) return "Select a sysex file to upload"
        if(curName.length === 0) return "Enter a bank name";
        if(bankNames.includes(curName.trim())) return `Bank with name ${curName} already exists`;
        return null;
    }

    $: rejection_reason = check_for_rejection(curName, curFileName);
    $: submit_enabled = rejection_reason === null;
</script>
<style>
    .upload-bank-overlay-main{
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: rgba(0, 0, 0, 0.5);
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        z-index: 200;
    }

    .upload-bank-overlay-window{
        background-color: #333;
        color: white;
        padding: 10px 30px 20px 30px;
        display: block;
    }

    button{
        width: 100%;
        margin-top: 10px;
    }

    .header{
        width: 100%;
        text-align: center;
        margin-bottom: 10px;
        font-size: large;
        opacity: 0.5;
    }

    .discovered-voices-grid{
        display: grid;
        grid-template-rows: repeat(16, auto);
        grid-auto-flow: column;
    }

</style>
<div class='upload-bank-overlay-main' on:click|stopPropagation={()=>{dispatcher('close')}}>
    <div class='upload-bank-overlay-window' on:click|stopPropagation>
        <div class='header'>Upload</div>
        <div style="display: grid; grid-template-columns: max-content 1fr; gap: 4px 20px;">
            <div>Bank .syx file</div>
            <input bind:this={bank_file_input} on:change={onFileChange} type="file"/>

            {#if bankVoiceNames !== undefined}

            <div style="grid-column: 1/3">
                <div>Discovered Voices:</div>
                <div class='discovered-voices-grid'>
                    {#each bankVoiceNames as name, i}
                        <div>{i+1}: {name}</div>
                    {/each}
                </div>
            </div>
            {/if}
            <div>Bank Name</div>
            <input bind:this={bank_name_input} on:input={onNameChange} type="text" placeholder="Bank Name..."/>
        </div>
        <button bind:this={submit_btn} disabled={!submit_enabled} on:click={onSubmit}>{rejection_reason === null ? 'Submit' : rejection_reason}</button>
    </div>
</div>