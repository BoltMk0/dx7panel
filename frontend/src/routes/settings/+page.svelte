<script>
    import {getConnection} from "$lib/connection.js";
    import {getModel} from "$lib/model.js";
    import { onDestroy } from "svelte";
    import {browser} from "$app/environment"
    import { MESSAGE_ID } from "$lib/const.js";

    
    const connection = getConnection();
    const model = getModel();

    const unsubscribes = []
    
    let settings;
    let connectionstatus

    unsubscribes.push(model.settings.subscribe((val)=>{
        settings = val;
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


    const CONNECTION_LED_COLORS = ["red", "yellow", "green"];

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
        grid-template-columns: fit-content(200px) fit-content(100px);
        gap: 5px;
        margin: 20px;
    }

    .savebtn{
        grid-column: span 2;
    }
</style>

<div>
    <div class="connection-led" style="background-color: {CONNECTION_LED_COLORS[connectionstatus]};"/>
    <div class="settings-grid">
            <div>MIDI Input Device</div>
            <select on:change={(ev)=>{settings.set_input_device(ev.target.value)}}>
                {#each settings.get_input_devices() as device, i(i)}
                    <option value={device} selected={device == settings.get_input_device()}>{device}</option>
                {/each}
            </select>
            <div>MIDI Output Device</div>
            <select on:change={(ev)=>{settings.set_output_device(ev.target.value)}}>
                {#each settings.get_output_devices() as device, i(i)}
                    <option value={device} selected={device == settings.get_output_device()}>{device}</option>
                {/each}
            </select>
            <div>MIDI Thru Device</div>
            <select on:change={(ev)=>{settings.set_thru_device(ev.target.value)}}>
                {#each settings.get_thru_devices() as device, i(i)}
                    <option value={device} selected={device == settings.get_thru_device()}>{device}</option>
                {/each}
            </select>
            <div>Velocity Correction</div>
            <input type="checkbox" checked={settings.get_vel_correction()} on:change={(ev)=>{settings.set_vel_correction(ev.target.checked)}}/>
            <button class="savebtn" on:click={()=>{settings.save();}}>Save</button>
    </div>
</div>
