<script lang="ts">
    import ValueDisplay from "./ValueDisplay.svelte";

    export let value;
    export let min = 0;
    export let max = 99;
    export const size = 40;
    export let label = undefined;

    const valRange = max-min;

    const ROTATION_MIN = -145;
    const ROTATION_MAX = 145;
    const ROTATION_RANGE = ROTATION_MAX - ROTATION_MIN;

    $: knob_rotation = ROTATION_MIN + ROTATION_RANGE*(value-min)/valRange;

    let clicked = false;

    let valFloat;
    let _touchmem;

    function onMouseDown(ev){
        valFloat = value;
        clicked = true;
    }

    function onMouseMove(ev){
        if(!clicked) return;
        if(ev.movementY === 0) return;
        valFloat = Math.min(max, Math.max(min, valFloat - valRange*(ev.movementY)/100));
        value = Math.round(valFloat);
    }

    function onMouseUp(){
        clicked = false;
    }


    function onTouchDown(ev){
        _touchmem = ev.changedTouches[0].pageY;
        clicked = true;
    }

    function onTouchMove(ev){
        if(clicked){
            ev.stopPropagation();
            const touch = ev.changedTouches[0].pageY;
            const d = (_touchmem - touch)*max/size/4;
            const new_value = Math.min(max, Math.max(0, valFloat + d));
            if(!isNaN(new_value)){
                valFloat = new_value;
                value = Math.round(valFloat);
            }
            _touchmem = touch;
        }   
    }

</script>
<style>
    .my-knob-main{
        position: relative;
    }

    .my-knob-img{
        cursor: pointer;
        position: relative;
        background-color: #222;
        border-radius: 50%;
        border: 2px solid black;
        overflow: hidden;
        user-select: none;
        -webkit-user-drag: none;
    }

    .my-knob-line{
        border-radius: 50%;
        top: 2px;
        left: 50%;
        background-color: #0f8465;
        position: absolute;
        transform: translateX(-50%);
    }

    .my-knob-label{
        text-align: center;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        z-index: 2;
        user-select: none;
    }

    .my-knob-container{
        position: relative;
    }

    .my-knob-marker-container{
        position: absolute;
        top: -5px;
        left: -5px;
    }

    .my-knob-marker-container > .my-knob-line {
        background-color: black;
        width: 2px;
        height: 4px;
    }
</style>
<div class='my-knob-main'>
    <div class='my-knob-container' on:mousedown={onMouseDown} on:touchstart={onTouchDown} style="cursor: pointer; width: fit-content; height: fit-content;">
        <div class="my-knob-img" style="width: {size}px; height: {size}px; transform: rotate({knob_rotation}deg)">
            <div class="my-knob-line" style="width: {size/6}px; height: {size/6}px;"/>
        </div>
        <div class='my-knob-label'>
            <ValueDisplay bind:value={value} min={min} max={max} integer/>
        </div>
        <div class='my-knob-marker-container' style="width: {size+14}px; height: {size+14}px; transform: rotate({ROTATION_MIN}deg)">
            <div class="my-knob-line" />
        </div>
        <div class='my-knob-marker-container' style="width: {size+14}px; height: {size+14}px; transform: rotate({ROTATION_MAX}deg)">
            <div class="my-knob-line" />
        </div>
        <div class='my-knob-marker-container' style="width: {size+14}px; height: {size+14}px; transform: rotate({0}deg)">
            <div class="my-knob-line" />
        </div>
    </div>
    {#if label !== undefined}
    <div style="text-align: center;">{label}</div>
    {/if}
</div>
<svelte:body on:mousemove={onMouseMove} on:mouseup={onMouseUp} />
<svelte:window on:touchmove={onTouchMove} on:touchend={onMouseUp}/>