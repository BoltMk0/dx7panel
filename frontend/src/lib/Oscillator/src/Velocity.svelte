<script>
    export let amodsens;
    export let keyvel;
    export let level;

    import Knob from "svelte-knob";

    const KNOB_SIZE = "50";
    const KNOB_COLOR_PRIMARY = "#55A";
    const KNOB_COLOR_SECONDARY = "#222";
    const KNOB_COLOR_TEXT = "#EEE";
    const KNOB_STROKE_WIDTH = "20";

</script>
<style>
#main{
    display: grid;
    grid-template-columns: auto auto auto;
    align-items: center;
    justify-items: center;
    gap: 10px;
}
</style>


<div class="osc-section" id="main">
    <div>A Mod Sens</div>
    <div>Key Vel</div>
    <div>Level</div>
    <Knob bind:value={amodsens} size={KNOB_SIZE} max={3} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/>
    <Knob bind:value={keyvel} max={7} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/>
    <Knob bind:value={level} size={KNOB_SIZE} primaryColor={KNOB_COLOR_PRIMARY} secondaryColor={KNOB_COLOR_SECONDARY} textColor={KNOB_COLOR_TEXT} strokeWidth={KNOB_STROKE_WIDTH}/>
</div>