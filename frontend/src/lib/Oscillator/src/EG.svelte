<script>
    export let name="EG";
    export let l1;
    export let l2;
    export let l3;
    export let l4;
    export let r1;
    export let r2;
    export let r3;
    export let r4;

    import Slider from "$lib/Slider.svelte";
    import {OSC_PARAM} from "$lib/const.js";
    import * as util from "$lib/util.js";
    import MyKnob from "../../MyKnob.svelte";
    import ValueDisplay from "../../ValueDisplay.svelte";
    
    const KNOB_SIZE = "40";
    const KNOB_COLOR_PRIMARY = "#55A";
    const KNOB_COLOR_SECONDARY = "#222";
    const KNOB_COLOR_TEXT = "#EEE";
    const KNOB_STROKE_WIDTH = "20";

    let copyBtnText = 'Copy';
    function copyEG(){
        localStorage.setItem('dx7-eg-memory', JSON.stringify({
            l1, l2, l3, l4, r1, r2, r3, r4
        }));
        copyBtnText = 'Copied!';
        setTimeout(()=>{copyBtnText = 'Copy'}, 1000);
    }

    function pasteEG(){
        let data = localStorage.getItem('dx7-eg-memory');
        if(data){
            data = JSON.parse(data);
            l1 = data.l1;
            l2 = data.l2;
            l3 = data.l3;
            l4 = data.l4;
            r1 = data.r1;
            r2 = data.r2;
            r3 = data.r3;
            r4 = data.r4;
        }
    }
</script>
<style>
    #grid{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        text-align: center;
        justify-items: center;
        gap: 8px 3px;
    }

    .sectionLabel{
        grid-column: 1/5;
        text-align: center;
    }
    .buttons-container{
        margin-top: 4px;
        grid-column: 1/5;
        width: 100%;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 5px;
    }

    .buttons-container > button{
        background-color: #444;
        color: #AAA;
        font-size: small;
    }
</style>


<div id="main" class="osc-section">
    <div id="grid">
        <div class="sectionLabel">{name} Level</div>
        <Slider bind:value={l1} vertical size=70 max={util.get_param_max(OSC_PARAM.LEVEL_1)}/>
        <Slider bind:value={l2} vertical size=70 max={util.get_param_max(OSC_PARAM.LEVEL_2)}/>
        <Slider bind:value={l3} vertical size=70 max={util.get_param_max(OSC_PARAM.LEVEL_3)}/>
        <Slider bind:value={l4} vertical size=70 max={util.get_param_max(OSC_PARAM.LEVEL_4)}/>
        <ValueDisplay bind:value={l1}/>
        <ValueDisplay bind:value={l2}/>
        <ValueDisplay bind:value={l3}/>
        <ValueDisplay bind:value={l4}/>
        <!-- <Knob bind:value={r1} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH} max={util.get_param_max(OSC_PARAM.RATE_1)}/>
        <Knob bind:value={r2} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH} max={util.get_param_max(OSC_PARAM.RATE_2)}/>
        <Knob bind:value={r3} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH} max={util.get_param_max(OSC_PARAM.RATE_3)}/>
        <Knob bind:value={r4} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH} max={util.get_param_max(OSC_PARAM.RATE_4)}/> -->
        
        <div class="sectionLabel">{name} Rate</div>
        <MyKnob bind:value={r1} size={KNOB_SIZE}/>
        <MyKnob bind:value={r2} size={KNOB_SIZE}/>
        <MyKnob bind:value={r3} size={KNOB_SIZE}/>
        <MyKnob bind:value={r4} size={KNOB_SIZE}/>
        <div class="buttons-container">
            <button on:click={copyEG}>{copyBtnText}</button>
            <button on:click={pasteEG}>Paste</button>
        </div>
    </div>
</div>