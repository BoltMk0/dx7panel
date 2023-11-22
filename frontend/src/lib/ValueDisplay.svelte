<script lang="ts">
    import { createEventDispatcher, tick } from "svelte";

    export let value;
    export let min = undefined;
    export let max = undefined;
    export let integer = false;
    export let width = 35;

    const dispatcher = createEventDispatcher();

    let editMode = false;

    function apply(ev){
        function reject(reason){
            dispatcher('error', reason);
            editMode = false;
        }
        if(ev.target.value.length > 0){
            let newVal = integer ? parseInt(ev.target.value) : parseFloat(ev.target.value);
            if(isNaN(newVal)){
                return reject(`Invalid value - not a number: ${ev.target.value}`);
            }
            if(min !== undefined){
                if(newVal < min) return reject(`Invalid value - expected higher than ${min}, got ${ev.target.value}`);
            }
            if(max !== undefined){
                if(newVal > max) return reject(`Invalid value - expected lower than ${max}, got ${ev.target.value}`);
            }
            value = newVal;
        }
        editMode = false;
    }

    let editArm = false;
    let editArmTimeout;
    function onMouseDown(){
        editArm = true;
        editArmTimeout = setTimeout(()=>{editArm = false;}, 200);
    }

    function onMouseUp(){
        clearTimeout(editArmTimeout);
        if(editArm) edit();
    }

    let inputEle;
    function edit(){
        editMode = true;
        tick().then(()=>{
            inputEle.value = value;
            inputEle.select();
        });
    }
</script>


<style>

    .value-display-main{
        text-align: center;
    }

    .value-display-main > *{
        width: 100%;
        text-align: center;
        box-sizing: border-box;
    }
</style>
<div class='value-display-main' style="width: {width}px;">
    <input bind:this={inputEle} type="text" value="{value}" placeholder="{value}" on:change={apply} style="display: {editMode ? 'block' : 'none'};" on:focusout={()=>{editMode=false;}}/>
    <div on:mousedown={onMouseDown} on:mouseup={onMouseUp} style="display: {editMode ? 'none' : 'block'};">{value}</div>
</div>