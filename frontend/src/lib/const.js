const OSC_PARAM = {
    RATE_1: 0,
    RATE_2: 1,
    RATE_3: 2,
    RATE_4: 3,
    LEVEL_1: 4,
    LEVEL_2: 5,
    LEVEL_3: 6,
    LEVEL_4: 7,
    SCALE_BREAKPOINT: 8,
    SCALE_LDEPTH: 9,
    SCALE_RDEPTH: 10,
    SCALE_LCURVE: 11,
    SCALE_RCURVE: 12,
    RATE_SCALING: 13,
    MOD_SENS_AMP: 14,
    VEL_SENS: 15,
    LEVEL: 16,
    MODE: 17,
    FREQ_COARSE: 18,
    FREQ_FINE: 19,
    DETUNE: 20
}

const VOICE_PARAM = {
    PITCH_RATE_1: 126,
    PITCH_RATE_2: 127,
    PITCH_RATE_3: 128,
    PITCH_RATE_4: 129,
    PITCH_LEVEL_1: 130,
    PITCH_LEVEL_2: 131,
    PITCH_LEVEL_3: 132,
    PITCH_LEVEL_4: 133,
    ALGO_SEL: 134,
    FEEDBACK: 135,
    OSC_SYNC: 136,
    LFO_SPEED: 137,
    LFO_DELAY: 138,
    LFO_PITCH_MOD: 139,
    LFO_AMP_MOD: 140,
    LFO_SYNC: 141,
    LFO_WAVE: 142,
    MOD_SENS_PITCH: 143,
    TRANSPOSE: 144,
    OPERATOR_EN: 155
};

const MESSAGE_ID = {
    SUBSCRIBE: 200,
    VOICE_DUMP: 201,
    SET_NAME: 202,

    PRESET_DUMP: 210,
    LOAD_VOICE: 211, // (category, groupname, presetname)
    SET_PRESET_NAME: 212, // (groupname, presetname)
    NEW_PRESET: 213, // (groupname)
    NEW_GROUP: 214, // (groupname)
    DELETE_GROUP: 215, // (groupname)
    DELETE_PRESET: 216, // (groupname, presetname)
    SAVE_PRESET: 217, // (groupname, presetname(optional))

    GET_SETTINGS: 230,
    SET_SETTINGS: 231,
}

export { OSC_PARAM, VOICE_PARAM, MESSAGE_ID };