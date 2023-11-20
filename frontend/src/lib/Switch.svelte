<script>
    export let checked = false;
    export let inverted = false;
    export let color = "#2196F3";


    let c;
    $: c = inverted ? !checked : checked;
  </script>
  
  <style>
    .switch {
      position: relative;
      display: inline-block;
      width: 40px;
      height: 23px;
    }
  
    .switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }
  
    .slider {
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: #ccc;
      -webkit-transition: 0.4s;
      transition: 0.4s;
      border-radius: 23px;
    }
  
    .slider:before {
      position: absolute;
      content: "";
      height: 17px;
      width: 17px;
      left: 3px;
      bottom: 3px;
      background-color: white;
      -webkit-transition: 0.2s;
      transition: 0.2s;
      border-radius: 50%;
    }
  
    .color_on > * {
      background-color: #2196f3;
      box-shadow: 0 0 1px #2196f3;
    }
  
    input:checked + .slider:before {
      -webkit-transform: translateX(17px);
      -ms-transform: translateX(17px);
      transform: translateX(17px);
    }
  </style>
  
  <label class="switch {c ? "color_on" : ""}">
    <input type="checkbox" bind:checked/>
    <span class="slider" />
  </label>