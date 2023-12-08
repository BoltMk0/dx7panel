import { writable } from "svelte/store";
import { MESSAGE_ID, OSC_PARAM, VOICE_PARAM } from "./const";
import * as util from "./util.js";
import { getConnection } from "./connection";
import { showMessage } from "./errorMessage.js";

var msg_enable = true;

function send_message(mid, val) {
    if (msg_enable) {
        getConnection().send(JSON.stringify([mid, val]));
    }
    
}


class AlgorithmModel {
    selection;
    feedback;

    constructor(sel, fdbk) {
        this.selection = writable(sel);
        this.feedback = writable(fdbk);
    }
}

class OscModel {
    _idx;
    level1;
    level2;
    level3;
    level4;
    rate1;
    rate2;
    rate3;
    rate4;

    breakpoint;
    ldepth;
    rdepth;
    lcurve;
    rcurve;
    ratescaling;

    mod_sens_amp;
    vel_sens;
    level;
    mode;
    freq_coarse;
    freq_fine;
    detune;

    _unsubscribes = [];


    constructor(idx, messages) {
        this._idx = idx;

        this.level1 = writable(0);
        this.level2 = writable(0);
        this.level3 = writable(0);
        this.level4 = writable(0);
        this.rate1 = writable(0);
        this.rate2 = writable(0);
        this.rate3 = writable(0);
        this.rate4 = writable(0);

        this.breakpoint = writable(0);
        this.ldepth = writable(0);
        this.rdepth = writable(0);
        this.lcurve = writable(0);
        this.rcurve = writable(0);
        this.ratescaling = writable(0);

        this.mod_sens_amp = writable(0);
        this.vel_sens = writable(0);
        this.level = writable(0);
        this.mode = writable(0);
        this.freq_coarse = writable(0);
        this.freq_fine = writable(0);
        this.detune = writable(0);

        if (messages) this.update(messages);
        this._unsubscribes.push(this.level1.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.LEVEL_1, val); }));
        this._unsubscribes.push(this.level2.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.LEVEL_2, val); }));
        this._unsubscribes.push(this.level3.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.LEVEL_3, val); }));
        this._unsubscribes.push(this.level4.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.LEVEL_4, val); }));
        this._unsubscribes.push(this.rate1.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.RATE_1, val); }));
        this._unsubscribes.push(this.rate2.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.RATE_2, val); }));
        this._unsubscribes.push(this.rate3.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.RATE_3, val); }));
        this._unsubscribes.push(this.rate4.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.RATE_4, val); }));
        this._unsubscribes.push(this.breakpoint.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.SCALE_BREAKPOINT, val); }));
        this._unsubscribes.push(this.ldepth.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.SCALE_LDEPTH, val); }));
        this._unsubscribes.push(this.rdepth.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.SCALE_RDEPTH, val); }));
        this._unsubscribes.push(this.lcurve.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.SCALE_LCURVE, val); }));
        this._unsubscribes.push(this.rcurve.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.SCALE_RCURVE, val); }));
        this._unsubscribes.push(this.ratescaling.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.RATE_SCALING, val); }));
        this._unsubscribes.push(this.vel_sens.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.VEL_SENS, val); }));
        this._unsubscribes.push(this.level.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.LEVEL, val); }));
        this._unsubscribes.push(this.mod_sens_amp.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.MOD_SENS_AMP, val); }));
        this._unsubscribes.push(this.freq_coarse.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.FREQ_COARSE, val); }));
        this._unsubscribes.push(this.freq_fine.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.FREQ_FINE, val); }));
        this._unsubscribes.push(this.detune.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.DETUNE, val); }));
        this._unsubscribes.push(this.detune.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.DETUNE, val); }));
        this._unsubscribes.push(this.mode.subscribe((val) => { send_message(21 * (5 - this._idx) + OSC_PARAM.MODE, val); }));
    }

    update(messages) {
        if (typeof(messages[0]) !== Object) messages = [messages, ];
        for (let i in messages) {
            const [oscidx, osc_param_id] = util.to_osc_param(messages[i][0]);
            if (oscidx === this._idx) {
                switch (osc_param_id) {
                    case OSC_PARAM.RATE_1:
                        this.rate1.set(messages[i][1]);
                        break;
                    case OSC_PARAM.RATE_2:
                        this.rate2.set(messages[i][1]);
                        break;
                    case OSC_PARAM.RATE_3:
                        this.rate3.set(messages[i][1]);
                        break;
                    case OSC_PARAM.RATE_4:
                        this.rate4.set(messages[i][1]);
                        break;
                    case OSC_PARAM.LEVEL_1:
                        this.level1.set(messages[i][1]);
                        break;
                    case OSC_PARAM.LEVEL_2:
                        this.level2.set(messages[i][1]);
                        break;
                    case OSC_PARAM.LEVEL_3:
                        this.level3.set(messages[i][1]);
                        break;
                    case OSC_PARAM.LEVEL_4:
                        this.level4.set(messages[i][1]);
                        break;
                    case OSC_PARAM.SCALE_BREAKPOINT:
                        this.breakpoint.set(messages[i][1]);
                        break;
                    case OSC_PARAM.SCALE_LDEPTH:
                        this.ldepth.set(messages[i][1]);
                        break;
                    case OSC_PARAM.SCALE_RDEPTH:
                        this.rdepth.set(messages[i][1]);
                        break;
                    case OSC_PARAM.SCALE_LCURVE:
                        this.lcurve.set(messages[i][1]);
                        break;
                    case OSC_PARAM.SCALE_RCURVE:
                        this.rcurve.set(messages[i][1]);
                        break;
                    case OSC_PARAM.RATE_SCALING:
                        this.ratescaling.set(messages[i][1]);
                        break;
                    case OSC_PARAM.MOD_SENS_AMP:
                        this.mod_sens_amp.set(messages[i][1]);
                        break;
                    case OSC_PARAM.VEL_SENS:
                        this.vel_sens.set(messages[i][1]);
                        break;
                    case OSC_PARAM.LEVEL:
                        this.level.set(messages[i][1]);
                        break;
                    case OSC_PARAM.MODE:
                        this.mode.set(messages[i][1]);
                        break;
                    case OSC_PARAM.FREQ_COARSE:
                        this.freq_coarse.set(messages[i][1]);
                        break;
                    case OSC_PARAM.FREQ_FINE:
                        this.freq_fine.set(messages[i][1]);
                        break;
                    case OSC_PARAM.DETUNE:
                        this.detune.set(messages[i][1]);
                        break;
                }
            }
        }
    }
}

class SettingsModel {
    _data;
    _changes;

    constructor(data) {
        this._data = data;
        this._changes = {};
    }

    initialized() { return this._data !== undefined }

    get_input_devices() {
        if (!this.initialized()) return Array(0);
        return [...this._data["midi_in"]["choices"], null];
    }

    get_input_device() {
        if (!this.initialized()) return undefined;
        return this._data["midi_in"]["value"];
    }

    set_input_device(device) {
        if (!this.initialized()) return;
        if (device !== null && !this.get_input_devices().includes(device)) {
            throw new TypeError("Not a valid device: " + String(device));
        }
        this._data["midi_in"]["value"] = device;
        this._changes["midi_in"] = { "value": device };
    }

    get_output_devices() {
        if (!this.initialized()) return Array(0);
        return [...this._data["midi_out"]["choices"], null];
    }

    get_output_device() {
        if (!this.initialized()) return undefined;
        return this._data["midi_out"]["value"];
    }

    set_output_device(device) {
        if (!this.initialized()) return;
        if (device !== null && !this.get_output_devices().includes(device)) {
            throw new TypeError("Not a valid device: " + String(device));
        }
        this._data["midi_out"]["value"] = device;
        this._changes["midi_out"] = { "value": device };
    }

    get_thru_devices() {
        if (!this.initialized()) return [];
        return [...this._data["midi_thru"]["choices"], null];
    }

    get_thru_device() {
        if (!this.initialized()) return [];
        return this._data["midi_thru"]["value"];
    }

    set_thru_device(device) {
        if (!this.initialized()) return;
        if (device !== null && !this.get_thru_devices().includes(device)) {
            throw new TypeError("Not a valid device: " + String(device));
        }
        this._data["midi_thru"]["value"] = device;
        this._changes["midi_thru"] = { "value": device };
    }

    get_vel_correction() {
        if (!this.initialized()) return;
        return this._data['vel_correction']
    }
    set_vel_correction(c) {
        if (!this.initialized()) return;
        console.log(c);
        this._data['vel_correction'] = Boolean(c);
        this._changes['vel_correction'] = Boolean(c);
        console.log(this._changes);
    }

    save() {
        console.log(this._changes);
        getConnection().send(JSON.stringify([MESSAGE_ID.SET_SETTINGS, this._changes]));
    }
}

class Model {
    algo = new AlgorithmModel();
    oscs = [];

    pitch_level1 = writable(0);
    pitch_level2 = writable(0);
    pitch_level3 = writable(0);
    pitch_level4 = writable(0);
    pitch_rate1 = writable(0);
    pitch_rate2 = writable(0);
    pitch_rate3 = writable(0);
    pitch_rate4 = writable(0);
    algo_sel = writable(0);
    feedback = writable(0);
    osc_sync = writable(0);
    lfo_speed = writable(0);
    lfo_delay = writable(0);
    lfo_pitch_mod = writable(0);
    lfo_amp_mod = writable(0);
    lfo_sync = writable(0);
    lfo_wave = writable(0);
    mod_sens_pitch = writable(0);
    transpose = writable(0);
    operator_en = writable(0);

    voice_name = writable('');

    _unsubscribes = [];

    settings = writable(new SettingsModel());

    preset_banks = writable([]);
    user_banks = writable([]);

    cur_bank_cat = writable('preset');
    cur_bank_idx = writable(0);
    cur_voice_idx = writable(0);

    constructor(messages) {
        for (let i = 0; i < 6; i++) {
            this.oscs.push(new OscModel(i));
        }
        this.update(messages);
        this._unsubscribes.push(this.pitch_level1.subscribe((val) => { send_message(VOICE_PARAM.PITCH_LEVEL_1, val); }));
        this._unsubscribes.push(this.pitch_level2.subscribe((val) => { send_message(VOICE_PARAM.PITCH_LEVEL_2, val); }));
        this._unsubscribes.push(this.pitch_level3.subscribe((val) => { send_message(VOICE_PARAM.PITCH_LEVEL_3, val); }));
        this._unsubscribes.push(this.pitch_level4.subscribe((val) => { send_message(VOICE_PARAM.PITCH_LEVEL_4, val); }));
        this._unsubscribes.push(this.pitch_rate1.subscribe((val) => { send_message(VOICE_PARAM.PITCH_RATE_1, val); }));
        this._unsubscribes.push(this.pitch_rate2.subscribe((val) => { send_message(VOICE_PARAM.PITCH_RATE_2, val); }));
        this._unsubscribes.push(this.pitch_rate3.subscribe((val) => { send_message(VOICE_PARAM.PITCH_RATE_3, val); }));
        this._unsubscribes.push(this.pitch_rate4.subscribe((val) => { send_message(VOICE_PARAM.PITCH_RATE_4, val); }));
        this._unsubscribes.push(this.algo_sel.subscribe((val) => { send_message(VOICE_PARAM.ALGO_SEL, val); }));
        this._unsubscribes.push(this.feedback.subscribe((val) => { send_message(VOICE_PARAM.FEEDBACK, val); }));
        this._unsubscribes.push(this.osc_sync.subscribe((val) => { send_message(VOICE_PARAM.OSC_SYNC, val); }));
        this._unsubscribes.push(this.lfo_speed.subscribe((val) => { send_message(VOICE_PARAM.LFO_SPEED, val); }));
        this._unsubscribes.push(this.lfo_delay.subscribe((val) => { send_message(VOICE_PARAM.LFO_DELAY, val); }));
        this._unsubscribes.push(this.lfo_pitch_mod.subscribe((val) => { send_message(VOICE_PARAM.LFO_PITCH_MOD, val); }));
        this._unsubscribes.push(this.lfo_amp_mod.subscribe((val) => { send_message(VOICE_PARAM.LFO_AMP_MOD, val); }));
        this._unsubscribes.push(this.lfo_sync.subscribe((val) => { send_message(VOICE_PARAM.LFO_SYNC, val); }));
        this._unsubscribes.push(this.lfo_wave.subscribe((val) => { send_message(VOICE_PARAM.LFO_WAVE, val); }));
        this._unsubscribes.push(this.mod_sens_pitch.subscribe((val) => { send_message(VOICE_PARAM.MOD_SENS_PITCH, val); }));
        this._unsubscribes.push(this.transpose.subscribe((val) => { send_message(VOICE_PARAM.TRANSPOSE, val); }));
        this._unsubscribes.push(this.operator_en.subscribe((val) => { send_message(VOICE_PARAM.OPERATOR_EN, val); }));
        this._unsubscribes.push(this.voice_name.subscribe((val) => { send_message(MESSAGE_ID.VOICE_NAME, val); }));
    }

    load_voice(category, groupname, voicename) {
        getConnection().send(JSON.stringify([MESSAGE_ID.LOAD_VOICE, [category, groupname, voicename]]));
    }

    update(messages) {
        if (!messages) return;
        if (!Array.isArray(messages[0])) messages = [messages, ];

        for (let msg of messages) {
            if (msg[0] <= 125) {
                let [idx, _] = util.to_osc_param(msg[0]);
                this.oscs[idx].update(msg);
            } else {
                switch (msg[0]) {
                    case VOICE_PARAM.PITCH_RATE_1:
                        this.pitch_rate1.set(msg[1]);
                        break;
                    case VOICE_PARAM.PITCH_RATE_2:
                        this.pitch_rate2.set(msg[1]);
                        break;
                    case VOICE_PARAM.PITCH_RATE_3:
                        this.pitch_rate3.set(msg[1]);
                        break;
                    case VOICE_PARAM.PITCH_RATE_4:
                        this.pitch_rate4.set(msg[1]);
                        break;
                    case VOICE_PARAM.PITCH_LEVEL_1:
                        this.pitch_level1.set(msg[1]);
                        break;
                    case VOICE_PARAM.PITCH_LEVEL_2:
                        this.pitch_level2.set(msg[1]);
                        break;
                    case VOICE_PARAM.PITCH_LEVEL_3:
                        this.pitch_level3.set(msg[1]);
                        break;
                    case VOICE_PARAM.PITCH_LEVEL_4:
                        this.pitch_level4.set(msg[1]);
                        break;
                    case VOICE_PARAM.ALGO_SEL:
                        this.algo_sel.set(msg[1]);
                        break;
                    case VOICE_PARAM.FEEDBACK:
                        this.feedback.set(msg[1]);
                        break;
                    case VOICE_PARAM.OSC_SYNC:
                        this.osc_sync.set(msg[1]);
                        break;
                    case VOICE_PARAM.LFO_SPEED:
                        this.lfo_speed.set(msg[1]);
                        break;
                    case VOICE_PARAM.LFO_DELAY:
                        this.lfo_delay.set(msg[1]);
                        break;
                    case VOICE_PARAM.LFO_PITCH_MOD:
                        this.lfo_pitch_mod.set(msg[1]);
                        break;
                    case VOICE_PARAM.LFO_AMP_MOD:
                        this.lfo_amp_mod.set(msg[1]);
                        break;
                    case VOICE_PARAM.LFO_SYNC:
                        this.lfo_sync.set(msg[1]);
                        break;
                    case VOICE_PARAM.LFO_WAVE:
                        this.lfo_wave.set(msg[1]);
                        break;
                    case VOICE_PARAM.MOD_SENS_PITCH:
                        this.mod_sens_pitch.set(msg[1]);
                        break;
                    case VOICE_PARAM.TRANSPOSE:
                        this.transpose.set(msg[1]);
                        break;
                    case VOICE_PARAM.OPERATOR_EN:
                        this.operator_en.set(msg[1]);
                        break;
                    case MESSAGE_ID.SET_SETTINGS:
                        this.settings.set(new SettingsModel(msg[1]));
                        break;
                    case MESSAGE_ID.BANK_DUMP:
                        this.preset_banks.set(msg[1].preset);
                        this.user_banks.set(msg[1].user);
                        break;
                    case MESSAGE_ID.VOICE_NAME:
                        this.voice_name.set(msg[1]);
                        break;
                    case MESSAGE_ID.VOICE_LOAD:
                        const [cat, bi, vi] = msg[1];
                        this.cur_bank_cat.set(cat);
                        this.cur_bank_idx.set(bi);
                        this.cur_voice_idx.set(vi);
                        break;
                    case MESSAGE_ID.ERROR_MESSAGE:
                        showMessage(msg[1]);
                        break;
                    default:
                        console.log("ERROR: Unhandled message", msg);
                }
            }
        }
    }
}


var modelInstance;

function getModel() {
    if (modelInstance === undefined) {
        modelInstance = new Model();
    }
    return modelInstance;
}

export { getModel }