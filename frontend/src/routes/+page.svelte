<script>
    import Oscillator from "$lib/Oscillator/Oscillator.svelte";
    import Fullscreen from "svelte-fullscreen";
    import Eg from "../lib/Oscillator/src/EG.svelte";
    import Knob from "svelte-knob";
    import {getModel} from "$lib/model.js";
    import {getConnection} from "$lib/connection.js";
    import {onDestroy} from "svelte";
    import {browser} from "$app/environment"
    import Presets from "./Presets.svelte";

    const model = getModel();
    const connection = getConnection();
    const unsubscribes = [];

    const CONNECTION_LED_COLORS = ['red', 'yellow', 'green'];
    
    let connection_status;

    if(browser){
        connection.connect();
        unsubscribes.push(connection.connected.subscribe((val)=>{
            connection_status = val;
        }));
        unsubscribes.push(model.cur_preset.subscribe((val)=>{
            if(val)
                preset_btn_title = val.join('/');
        }))
    }

    let _fullscreen = false;
    let presets_visible=false;
    let preset_btn_title='Load preset'

    const KNOB_SIZE = "40";
    const KNOB_COLOR_PRIMARY = "#55A";
    const KNOB_COLOR_SECONDARY = "#222";
    const KNOB_COLOR_TEXT = "#EEE";
    const KNOB_STROKE_WIDTH = "20";

    let tune_val;
    let cutoff_val;
    let resonance_val;

    let pl1_val;
    let pl2_val;
    let pl3_val;
    let pl4_val;
    let pr1_val;
    let pr2_val;
    let pr3_val;
    let pr4_val;

    const WAVEFORMS = ["Sine", "Triangle", "Square", "S/Hold"];

    let selected_algorithm;
    let selected_waveform;
    let feedback_val;

    let lfo_pmod_sens_val;
    let lfo_rate_val;
    let lfo_delay_val;
    let lfo_pmod_val;
    let lfo_amod_val;
    let lfo_sync_val;

    let osc_sync_val;


    unsubscribes.push(model.pitch_level1.subscribe((val)=>{pl1_val=val;}));
    unsubscribes.push(model.pitch_level2.subscribe((val)=>{pl2_val=val;}));
    unsubscribes.push(model.pitch_level3.subscribe((val)=>{pl3_val=val;}));
    unsubscribes.push(model.pitch_level4.subscribe((val)=>{pl4_val=val;}));
    unsubscribes.push(model.pitch_rate1.subscribe((val)=>{pr1_val=val;}));
    unsubscribes.push(model.pitch_rate2.subscribe((val)=>{pr2_val=val;}));
    unsubscribes.push(model.pitch_rate3.subscribe((val)=>{pr3_val=val;}));
    unsubscribes.push(model.pitch_rate4.subscribe((val)=>{pr4_val=val;}));
    unsubscribes.push(model.algo_sel.subscribe((val)=>{selected_algorithm=val;}));
    unsubscribes.push(model.feedback.subscribe((val)=>{feedback_val=val;}));
    unsubscribes.push(model.osc_sync.subscribe((val)=>{osc_sync_val=val;}));
    unsubscribes.push(model.lfo_speed.subscribe((val)=>{lfo_rate_val=val;}));
    unsubscribes.push(model.lfo_delay.subscribe((val)=>{lfo_delay_val=val;}));
    unsubscribes.push(model.lfo_pitch_mod.subscribe((val)=>{lfo_pmod_val=val;}));
    unsubscribes.push(model.lfo_amp_mod.subscribe((val)=>{lfo_amod_val=val;}));
    unsubscribes.push(model.lfo_sync.subscribe((val)=>{lfo_sync_val=val;}));
    unsubscribes.push(model.lfo_wave.subscribe((val)=>{selected_waveform=val;}));
    unsubscribes.push(model.mod_sens_pitch.subscribe((val)=>{lfo_pmod_sens_val=val;}));
    unsubscribes.push(model.transpose.subscribe((val)=>{tune_val=val;}));

    $: model.pitch_level1.set(pl1_val);
    $: model.pitch_level2.set(pl2_val);
    $: model.pitch_level3.set(pl3_val);
    $: model.pitch_level4.set(pl4_val);
    $: model.pitch_rate1.set(pr1_val);
    $: model.pitch_rate2.set(pr2_val);
    $: model.pitch_rate3.set(pr3_val);
    $: model.pitch_rate4.set(pr4_val);
    $: model.algo_sel.set(selected_algorithm);
    $: model.feedback.set(feedback_val);
    $: model.osc_sync.set(osc_sync_val);
    $: model.lfo_speed.set(lfo_rate_val);
    $: model.lfo_delay.set(lfo_delay_val);
    $: model.lfo_pitch_mod.set(lfo_pmod_val);
    $: model.lfo_amp_mod.set(lfo_amod_val);
    $: model.lfo_sync.set(lfo_sync_val);
    $: model.lfo_wave.set(selected_waveform);
    $: model.mod_sens_pitch.set(lfo_pmod_sens_val);
    $: model.transpose.set(tune_val);


    function set_algorithm(val){
        selected_algorithm = Math.max(0, Math.min(32, val));
    }

    function set_waveform(val){
        selected_waveform = Math.max(0, Math.min(4, val));
    }


    onDestroy(()=>{
        for(let u in unsubscribes) unsubscribes[u]();
    });

</script>
<style>
    #main-window{
        background-color: #333;
    }

    :global(body){
        margin: 0;
    }

    :global(.osc-panel) {
        background-color: #444;
    }

    :global(.osc-section) {
        background-color: #333;
    }

    :global(body){
        background: black;
        color: #EEE;
    }

    #main-window{
        width: 100%;
        display: grid;
        grid-template-columns: 320px auto;
        gap: 5px;
    }

    #main-window-container{
        display: flex;
        justify-content: center;
        align-content: center;
        margin: 0;
        overflow: hidden;
        height: 100vh;
    }

    #osc-section{
        display: flex;
        flex-wrap: wrap;
        grid-template-rows: min-content(50px) auto;
        overflow: hidden;
    }

    #osc-container{
        display: flex;
        flex-wrap: wrap;
        /* justify-content: center;
        align-content: center; */
        /* display: grid;
        grid-template-columns: 1fr 1fr; */
        gap:3px;
        overflow-y: scroll;
        height: 100%;
    }

    #fullscreen-btn{
        width: 100%;
        height: 40px;
    }

    .section-header{
        font-size: larger;
        text-align: center;
        opacity: 0.6;
    }

    #left-col{
        padding: 10px;
        overflow-y: scroll;
    }
    #left-col > *{
        margin-bottom:10px;
    }

    #algo-select {
        display: grid;
        gap: 10px;
        align-items: space-evenly;
    }

    #algo-select > *{
        display: grid;
        justify-items: center;
        align-content: center;
        gap: 3px;
    }

    .algo-display{
        height: 150px;
        border-radius: 10px;
    }

    #lfo, #master-controls{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
    }

    .row{
        width: 100%;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: space-evenly;
    }

    .row > div{
        display: grid;
        justify-items: center;
    }

    .connection-led{
        width: 15px;
        height: 15px;
        border-radius: 50%;
        position: absolute;
        left: 6px;
        top: 6px;
        box-shadow: inset 0 -5px 10px -5px black, inset 0 7px 10px -5px rgba(255, 255, 255, 0.5);
    }

    #voice-btn{
        width: 100%;
        background-color: rgba(0, 0, 0, 0.3);
        color: #CCC;
        text-align: left;
    }

</style>

<Fullscreen let:onRequest>
    <div id="main-window-container">
        {#if presets_visible}
            <Presets bind:visible={presets_visible}/>
        {/if}
        <div id="main-window">
            <div class="section-header">
                <div class="connection-led" style="background-color:{CONNECTION_LED_COLORS[connection_status]}"/>
                <div>Main</div>
            </div>
            <div class="section-header">OSCs</div>
            <!-- <div class="section-header">Thing</div> -->
            <div id="left-col" class="osc-panel">
                {#if !_fullscreen}
                <button id="fullscreen-btn" on:click={()=>{onRequest(); _fullscreen=true}}>Fullscreen</button>
                {/if}
                <button id="voice-btn" on:click={()=>{presets_visible=true;}}>{preset_btn_title}</button>
                <div class="osc-section" id="master-controls">
                    <div class="row">
                        <div>
                            <Knob bind:value={tune_val} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/>
                            <div>Tune</div>
                        </div>
                    </div>
                </div>
                <div class="osc-section">
                    <Eg 
                    bind:l1={pl1_val} 
                    bind:l2={pl2_val} 
                    bind:l3={pl3_val} 
                    bind:l4={pl4_val} 
                    bind:r1={pr1_val} 
                    bind:r2={pr2_val} 
                    bind:r3={pr3_val} 
                    bind:r4={pr4_val} 
                    name="Pitch EG"/>
                </div>
                <div class="osc-section" id="algorithm-section">
                    <div style="display: grid; grid-template-columns: auto fit-content(100px);">
                        <div>
                            <img class='algo-display' src="/algorithms/alg{selected_algorithm+1}.png"/>
                        </div>
                        <div class="osc-section" id='algo-select'>
                            <div>
                                <div>Algorithm</div>
                                <div style="display: flex">
                                    <button on:click={()=>{set_algorithm(selected_algorithm-1)}}>-</button>
                                    <select on:change={(ev)=>{set_algorithm(parseInt(ev.target.value)-1)}}>
                                        {#each {length: 32} as _, i}
                                            <option selected={selected_algorithm==i}>{i+1}</option>
                                        {/each}
                                    </select>
                                    <button on:click={()=>{set_algorithm(selected_algorithm+1)}}>+</button>
                                </div>
                            </div>
                            <div>
                                <div>Feedback</div>
                                <Knob size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/>
                            </div>
                        </div>
                    </div>
                    
                </div>
                <div class="osc-section" id="lfo">
                    <div style="width: 100%; text-align: center;">LFO</div>
                    <div class="row">
                        <div>
                            <div>Waveform</div>
                            <select on:change={(ev)=>{set_waveform(parseInt(ev.target.value))}}>
                                {#each WAVEFORMS as name, i}
                                <option value={i}>{name}</option>
                                {/each}
                            </select>
                        </div>
                        <div>
                            <Knob bind:value={lfo_pmod_sens_val} max={7} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/>
                            <div>Pitch Sens</div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div>
                            <Knob bind:value={lfo_rate_val} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/>
                            <div>Rate</div>
                        </div>
                        <div>
                            <Knob bind:value={lfo_delay_val} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/>
                            <div>Delay</div>
                        </div>
                        <div>
                            <Knob bind:value={lfo_pmod_val} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/>
                            <div>Pitch</div>
                        </div>
                        <div>
                            <Knob bind:value={lfo_amod_val} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/>
                            <div>Amp</div>
                        </div>
                    </div>
                </div>
            </div>
            <div id="osc-container">
                {#each {length: 6} as _, i}
                    <Oscillator idx={i}/>
                {/each}
            </div>
        </div>
    </div>
</Fullscreen>
