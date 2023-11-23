<script lang="ts">
    import {getConnection, WS_PORT} from "$lib/connection";

    const connection = getConnection();

    const unsubscribes = [];  

    let connectionState;
    unsubscribes.push(connection.connected.subscribe(val=>{connectionState = val;}));



    const CONNECTION_LED_COLORS = ["red", "yellow", "green"];
    $: connectionLEDColor = CONNECTION_LED_COLORS[connectionState];


    let host;
    let overlayShow = false;
    function showOverlay(){
        host = connection.get_host();
        overlayShow = true;
    }

    function onChange(ev){
        host = ev.target.value;
        connection.set_host(host);
    }
</script>
<style>

    .led{
        width: 20px;
        height: 20px;
        border-radius: 50%;
        position: fixed;
        top: 3px;
        left: 3px;
        border: 1px solid black;
        box-shadow: inset 0 0 2px black;
        cursor: pointer;
        z-index: 9999;
    }

    .connection-edit-overlay{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }

    .connection-edit-overlay > .overlay-panel{
        padding: 20px 30px;
        background-color: wheat;
        border: 2px solid black;
        z-index: 1001;
    }

</style>
<div class="led" style="background-color: {connectionLEDColor}" on:click={showOverlay}/>

{#if overlayShow}
<div class="connection-edit-overlay" on:mousedown={()=>{overlayShow = false; }}>
    <div on:mousedown|stopPropagation class="overlay-panel">
        <input on:change={onChange} value="{host}"/>
        <button on:mousedown={()=>{host = `${window.location.hostname}:${WS_PORT}`}}>Reset</button>
    </div>
</div>
{/if}