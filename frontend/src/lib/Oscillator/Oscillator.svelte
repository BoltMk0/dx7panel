<script>
    export let idx=0;
    import Curve from "./src/Curve.svelte";
    import EG from "./src/EG.svelte";
    import Freq from "./src/Freq.svelte";
    import FreqMode from "./src/FreqMode.svelte";
    import Velocity from "./src/Velocity.svelte";
    import Master from "./src/Master.svelte";
    import {getModel} from "$lib/model.js";
    import { onDestroy } from "svelte";

    const model = getModel();

    let tune_val;
    let coarse_val;
    let fine_val;
    let ratio_val;
    let osc_en_val;
    let amod_sens_val;
    let keyvel_val;
    let level_val;
    let breakpoint_val;
    let ldepth_val;
    let rdepth_val;
    let lcurve_val;
    let rcurve_val;
    let ratescaling_val;
    let l1_val;
    let l2_val;
    let l3_val;
    let l4_val;
    let r1_val;
    let r2_val;
    let r3_val;
    let r4_val;
    let mode_val;
    
    let operator_en;

    const unsubscribes = [];
    const osc = model.oscs[idx];
    
    unsubscribes.push(osc.level1.subscribe((val) => {l1_val = val;}));
    unsubscribes.push(osc.level2.subscribe((val) => {l2_val=val}));
    unsubscribes.push(osc.level3.subscribe((val) => {l3_val=val}));
    unsubscribes.push(osc.level4.subscribe((val) => {l4_val=val}));
    unsubscribes.push(osc.rate1.subscribe((val) => {r1_val=val}));
    unsubscribes.push(osc.rate2.subscribe((val) => {r2_val=val}));
    unsubscribes.push(osc.rate3.subscribe((val) => {r3_val=val}));
    unsubscribes.push(osc.rate4.subscribe((val) => {r4_val=val}));
    unsubscribes.push(osc.breakpoint.subscribe((val) => {breakpoint_val=val}));
    unsubscribes.push(osc.ldepth.subscribe((val) => {ldepth_val=val }));
    unsubscribes.push(osc.rdepth.subscribe((val) => {rdepth_val=val}));
    unsubscribes.push(osc.lcurve.subscribe((val) => {lcurve_val=val }));
    unsubscribes.push(osc.rcurve.subscribe((val) => {rcurve_val=val}));
    unsubscribes.push(osc.ratescaling.subscribe((val)=>{ratescaling_val=val}));
    unsubscribes.push(osc.vel_sens.subscribe((val) =>{keyvel_val=val}));
    unsubscribes.push(osc.level.subscribe((val) => {level_val=val}));
    unsubscribes.push(osc.mod_sens_amp.subscribe((val) =>{amod_sens_val=val}));
    unsubscribes.push(osc.freq_coarse.subscribe((val) =>{coarse_val=val}));
    unsubscribes.push(osc.freq_fine.subscribe((val) => {fine_val=val}));
    unsubscribes.push(osc.detune.subscribe((val) => {tune_val=val-7}));
    unsubscribes.push(osc.mode.subscribe((val) => {ratio_val=val}));

    unsubscribes.push(model.operator_en.subscribe((val) => {operator_en=val}));
    unsubscribes.push(model.operator_en.subscribe((val) => {osc_en_val=(val>>(5-idx))&1}));


    $: osc.level1.set(l1_val);
    $: osc.level2.set(l2_val);
    $: osc.level3.set(l3_val);
    $: osc.level4.set(l4_val);
    $: osc.rate1.set(r1_val);
    $: osc.rate2.set(r2_val);
    $: osc.rate3.set(r3_val);
    $: osc.rate4.set(r4_val);
    $: osc.breakpoint.set(breakpoint_val);
    $: osc.ldepth.set(ldepth_val);
    $: osc.rdepth.set(rdepth_val);
    $: osc.lcurve.set(lcurve_val);
    $: osc.rcurve.set(rcurve_val);
    $: osc.ratescaling.set(ratescaling_val);
    $: osc.vel_sens.set(keyvel_val);
    $: osc.level.set(level_val);
    $: osc.mod_sens_amp.set(amod_sens_val);
    $: osc.freq_coarse.set(coarse_val);
    $: osc.freq_fine.set(fine_val);
    $: osc.detune.set(tune_val+7);
    $: osc.mode.set(ratio_val);
    $: model.operator_en.set(operator_en&~(1<<(5-idx)) | (osc_en_val<<(5-idx)));

    onDestroy(()=>{
        for(let u in unsubscribes) unsubscribes[u]();
    });
</script>

<style>
    #main{
        padding: 10px;
        border-radius: 10px;
        /* min-width: 30%; */
        width: fit-content;
        height: fit-content
    }

    #col-container{
        display: grid;
        grid-template-columns: fit-content(180px) 1fr;
        gap: 5px;
    }

    .column{
        display: grid;
        gap: 5px;
    }

    .column > * {
        width: 100%;
    }

    #right-col{
        grid-template-rows: fit-content(50px) fit-content(100px) auto;
    }

    #right-col-upper{
        display: grid;
        grid-template-columns: auto fit-content(50px);
        align-items: end;
        gap:8px;
    }

    #freqmode-container {
        margin-left: -12px;
        z-index: 1;
    }

    :global(.osc-section) {
        z-index: 10;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.3), inset 0 6px 3px -6px rgba(255, 255, 255, 0.3), inset 0 0 3px rgba(255, 255, 255, 0.2);
    }

</style>

<div id="main" class="osc-panel">
    <div id="col-container">
        <div id="left-col" class="column">
            <Freq
            bind:coarse={coarse_val}
            bind:fine={fine_val}
            bind:tune={tune_val}
            />
            <EG
            bind:l1={l1_val}
            bind:l2={l2_val}
            bind:l3={l3_val}
            bind:l4={l4_val}
            bind:r1={r1_val}
            bind:r2={r2_val}
            bind:r3={r3_val}
            bind:r4={r4_val}
            name="Amp EG"/>
        </div>
        <div id="right-col" class="column">
            <div id="right-col-upper">
                <div id="freqmode-container">
                    <FreqMode bind:checked={ratio_val}/>
                </div>
                <Master idx={idx} bind:enabled={osc_en_val}/>
            </div>
            <Velocity
            bind:amodsens={amod_sens_val}
            bind:keyvel={keyvel_val}
            bind:level={level_val}
            />
            <Curve
            bind:lcurve={lcurve_val}
            bind:rcurve={rcurve_val}
            bind:ldepth={ldepth_val}
            bind:rdepth={rdepth_val}
            bind:ratescaling={ratescaling_val}
            bind:breakpoint={breakpoint_val}
            />
        </div>
    </div>
</div>