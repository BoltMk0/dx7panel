<script>
    export let checked = false;
    export let color = "#2196F3";
  </script>
  
  <style>
    .switch {
      position: relative;
      display: inline-block;
      width: 23px;
      height: 40px;
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
  
    input:checked + .slider {
      background-color: #2196f3;
    }
  
    input:checked + .slider {
      box-shadow: 0 0 1px #2196f3;
    }
  
    input:checked + .slider:before {
      -webkit-transform: translateY(-17px);
      -ms-transform: translateY(-17px);
      transform: translateY(-17px);
    }
  </style>
  
  <label class="switch">
    <input type="checkbox" bind:checked />
    <span class="slider" />
  </label>