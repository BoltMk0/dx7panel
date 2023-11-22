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
    
    const KNOB_SIZE = "40";
    const KNOB_COLOR_PRIMARY = "#55A";
    const KNOB_COLOR_SECONDARY = "#222";
    const KNOB_COLOR_TEXT = "#EEE";
    const KNOB_STROKE_WIDTH = "20";
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
</style>


<div id="main" class="osc-section">
    <div id="grid">
        <div class="sectionLabel">{name} Level</div>
        <Slider bind:value={l1} vertical size=70 max={util.get_param_max(OSC_PARAM.LEVEL_1)}/>
        <Slider bind:value={l2} vertical size=70 max={util.get_param_max(OSC_PARAM.LEVEL_2)}/>
        <Slider bind:value={l3} vertical size=70 max={util.get_param_max(OSC_PARAM.LEVEL_3)}/>
        <Slider bind:value={l4} vertical size=70 max={util.get_param_max(OSC_PARAM.LEVEL_4)}/>
        <div>1</div>
        <div>2</div>
        <div>3</div>
        <div>4</div>
        <!-- <Knob bind:value={r1} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH} max={util.get_param_max(OSC_PARAM.RATE_1)}/>
        <Knob bind:value={r2} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH} max={util.get_param_max(OSC_PARAM.RATE_2)}/>
        <Knob bind:value={r3} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH} max={util.get_param_max(OSC_PARAM.RATE_3)}/>
        <Knob bind:value={r4} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH} max={util.get_param_max(OSC_PARAM.RATE_4)}/> -->
        <MyKnob bind:value={r1} size={KNOB_SIZE}/>
        <MyKnob bind:value={r2} size={KNOB_SIZE}/>
        <MyKnob bind:value={r3} size={KNOB_SIZE}/>
        <MyKnob bind:value={r4} size={KNOB_SIZE}/>
        <div class="sectionLabel">{name} Rate</div>
    </div>
</div>