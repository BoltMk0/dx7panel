<script>
    export let size=100;
    export let vertical=false;
    export let thumbsize=20;
    export let bgwidth=3;
    export let max=100;
    export let value;

    const d_multiplier = max/size;

    let _value = 0;
    let _moving = false;
    let _touchmem;

    let x = 0;
    $:value=Math.round(_value)
    $:x=size*value/max;

    function onMouseDown(ev){
        _moving = true;
    }
    function onMouseUp(){
        _moving = false;
    }
    function onMouseMove(ev){
        if(_moving){
            const d = (vertical ? -ev.movementY : ev.mouvementX)*d_multiplier;

            const new_value = Math.min(100, Math.max(0, _value + d));
            if(!isNaN(new_value)) _value = new_value;
        }   
    }

    function onTouchDown(ev){
        _touchmem = vertical ? ev.changedTouches[0].pageY : -ev.changedTouches[0].pageX;
        _moving = true;
    }
    function onTouchMove(ev){
        if(_moving){
            const touch = vertical ? ev.changedTouches[0].pageY : -ev.changedTouches[0].pageX;
            const d = (_touchmem - touch)*d_multiplier;
            const new_value = Math.min(100, Math.max(0, _value + d));
            if(!isNaN(new_value)) _value = new_value;
            _touchmem = touch;
        }   
    }

</script>
<style>
    .slider-main{
        position: relative;
    }
    .slider-bg{
        position: absolute;
        background-color: rgb(27, 146, 130);
    }
    .slider-thumb{
        position: absolute;
        border-radius: 50%;
        background-color: #0f8465;
    }
    .draggable{
        user-select: none;
        cursor: move;
        border: solid 1px black;
        transform: translate(-50%, -50%);
    }
    .centered{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 10px;
    }
</style>
<div class='centered' on:touchstart|preventDefault={onTouchDown} style="transform: translateX(-{bgwidth/2}px);">
{#if vertical}
    <div class="slider-main" style="height: {size}px;">
        <div class="slider-bg" style="bottom: 0; top: 0; width: {bgwidth}px; background-color: #777;"></div>
        <div class="slider-bg" style="bottom: 0; top: {size-x}px; width: {bgwidth}px;"></div>
        <div class="slider-thumb draggable" style="width: {thumbsize}px; height: {thumbsize}px; left: {bgwidth/2}px; top: {size-x}px" on:mousedown={onMouseDown}></div>
    </div>
{:else}
    <div class="slider-main" style="width: {size}px;">
        <div class="slider-bg" style="left: 0; right: 0; height: {bgwidth}px; background-color: #777;"></div>
        <div class="slider-bg" style="left: 0; right: {size-x}px; height: {bgwidth}px;"></div>
        <div class="slider-thumb draggable" style="width: {thumbsize}px; height: {thumbsize}px; top: {bgwidth/2}px; left: {x}px" on:mousedown={onMouseDown}></div>
    </div>
{/if}
</div>
<svelte:window on:touchend={onMouseUp} on:touchmove={onTouchMove} on:mousemove={onMouseMove} on:mouseup={onMouseUp}/>