<script>
    import {getConnection} from "$lib/connection.js";
    import {getModel} from "$lib/model.js";
    import { onDestroy } from "svelte";
    import {browser} from "$app/environment"
    import { MESSAGE_ID } from "$lib/const.js";

    
    const connection = getConnection();
    const model = getModel();

    const unsubscribes = []
    
    let presets;
    let cur_preset;
    
    $: console.log(presets);

    let connectionstatus

    unsubscribes.push(model.presets.subscribe((val)=>{
        presets = val;
    }));
    unsubscribes.push(model.cur_preset.subscribe((val)=>{
        cur_preset = val;
    }));

    unsubscribes.push(connection.connected.subscribe((val)=>{
        connectionstatus = val;
    }));

    onDestroy(()=>{
        for(let i in unsubscribes) unsubscribes[i]();
    });

    if(browser){
        connection.connect();
    }


</script>

<style>
     .connection-led{
        width: 15px;
        height: 15px;
        border-radius: 50%;
        left: 6px;
        top: 6px;
        box-shadow: inset 0 -5px 10px -5px black, inset 0 7px 10px -5px rgba(255, 255, 255, 0.5);
    }

    .settings-grid{
        display: grid;
        grid-template-columns: fit-content(100px) fit-content(100px);
        gap: 5px;
        margin: 20px;
    }

    .savebtn{
        grid-column: span 2;
    }
</style>


<div>
    <div>
        <div>

        </div>
    </div>
</div>