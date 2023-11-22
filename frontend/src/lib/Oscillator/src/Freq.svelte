<script>
    export let tune;
    export let coarse;
    export let fine;
    import Knob from "svelte-knob";
    import MyKnob from "../../MyKnob.svelte";

    const KNOB_SIZE = "50";
    const KNOB_COLOR_PRIMARY = "#55A";
    const KNOB_COLOR_SECONDARY = "#222";
    const KNOB_COLOR_TEXT = "#EEE";
    const KNOB_STROKE_WIDTH = "20";
    
</script>

<style>
    #knobs-container{
        display: flex;
        align-content: center;
        justify-content: space-evenly;
        gap: 5px;
    }

    .knob-container{
        display: grid;
        justify-items: center;
        gap: 2px;
    }

    .knob-container > .label {
        font-size: smaller;
    }
</style>


<div class="osc-section">
    <div id="knobs-container">
        <div class="knob-container">
            <!-- <Knob bind:value={tune} size={KNOB_SIZE} min={-7} max={7} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/> -->
            <MyKnob bind:value={tune} size={KNOB_SIZE} min={-7} max={7}/>
            <div class="label">Tune</div>
        </div>
        <div class="knob-container">
            <!-- <Knob bind:value={coarse} max={31} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/> -->
            <MyKnob bind:value={coarse} size={KNOB_SIZE} min={0} max={31}/>


            <div class="label">Coarse</div>
        </div>
        <div class="knob-container">
            <!-- <Knob bind:value={fine} max={99} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/> -->
            <MyKnob bind:value={fine} size={KNOB_SIZE} min={0} max={99}/>
            <div class="label">Fine</div>
        </div>
    </div>
</div>