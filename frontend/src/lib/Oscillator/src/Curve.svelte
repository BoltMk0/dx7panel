<script>
    import Slider from "$lib/Slider.svelte";
    import Knob from "svelte-knob";
    import MyKnob from "../../MyKnob.svelte";
    import ValueDisplay from "../../ValueDisplay.svelte";
    export let ldepth;
    export let rdepth;
    export let breakpoint;
    export let lcurve;
    export let rcurve;
    export let ratescaling;
    
    const KNOB_SIZE = "40";
    const KNOB_COLOR_PRIMARY = "#55A";
    const KNOB_COLOR_SECONDARY = "#222";
    const KNOB_COLOR_TEXT = "#EEE";
    const KNOB_STROKE_WIDTH = "20";

</script>
<style>
    .row{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap:3px;
    }

    .row > *{
        display: grid;
        justify-items: center;
        gap:4px;
    }
    #main{
        font-size: small;
        display: grid;
        align-items: center;
    }

    select{
        background-color: #333;
        color: white;
        padding: 2px;
    }
</style>

<div class="osc-section" id="main">
    <div class="row">
        <div>
            <!-- <Knob bind:value={ldepth} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/> -->
            <MyKnob bind:value={ldepth} size={KNOB_SIZE}/>
            <div>L Depth</div>
        </div>
        <div>
            <div>Break Point</div>
            <Slider bind:value={breakpoint} max=99 size={60}/>
            <ValueDisplay bind:value={breakpoint} max=99 />
        </div>
        <div>
            <!-- <Knob bind:value={rdepth} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/> -->
            <MyKnob bind:value={rdepth} size={KNOB_SIZE}/>

            <div>R Depth</div>
        </div>
    </div>
    <div class="row">
        <div>
            <select on:change={(ev)=>{lcurve=parseInt(ev.target.value);}}>
                <option value="0" selected={lcurve==0}>-Lin</option>
                <option value="1" selected={lcurve==1}>-Exp</option>
                <option value="2" selected={lcurve==2}>+Lin</option>
                <option value="3" selected={lcurve==3}>+Exp</option>
            </select>
            <div>L Curve</div>
        </div>
        <div>
            <!-- <Knob bind:value={ratescaling} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} max={7} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/> -->
            <MyKnob bind:value={ratescaling} size={KNOB_SIZE} max={7} />

            <div style="text-align: center;">Rate<br/>Scaling</div>
        </div>
        <div>
            <select on:change={(ev)=>{rcurve=parseInt(ev.target.value);}}>
                <option value="0" selected={rcurve==0}>-Lin</option>
                <option value="1" selected={rcurve==1}>-Exp</option>
                <option value="2" selected={rcurve==2}>+Lin</option>
                <option value="3" selected={rcurve==3}>+Exp</option>
            </select>
            <div>R Curve</div>
        </div>
    </div>
</div>