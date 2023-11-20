function to_osc_param(param_id) {
    const osc_idx = 5 - Math.floor(param_id / 21);
    const osc_param_id = param_id % 21;
    return [osc_idx, osc_param_id];
}

function get_param_max(param_id) {
    if (param_id < 126) {
        const tmp = param_id % 21;
        if (tmp === 11 || tmp === 12 || tmp == 14)
            return 3;
        if (tmp === 13 || tmp === 15)
            return 7;
        if (tmp == 17)
            return 1;
        if (tmp == 18)
            return 31;
        if (tmp == 20)
            return 14;
    } else if (param_id == 134)
        return 31;
    else if (param_id in (135, 143))
        return 7;
    else if (param_id in (136, 141))
        return 1;
    else if (param_id == 142)
        return 4;
    else if (param_id == 144)
        return 48;
    else if (145 <= param_id < 155)
        return 127;
    else if (param_id == 155)
        return 0b01111111;

    return 99
}

export { to_osc_param, get_param_max }