import asyncio
from typing import Any
from websockets.server import serve
from websockets.legacy.protocol import broadcast
from websockets.exceptions import *
import json
from typing import Dict
import os
import sys
import shutil

from .dx7programmer import DX7Controller, DX7Voice, VoiceParameterValue

VERSION = "1.0-beta"

class MessageIDs:
    SUBSCRIBE = 200
    VOICE_DUMP = 201
    SET_NAME = 202

    PRESET_DUMP = 210
    LOAD_VOICE = 211
    SET_PRESET_NAME = 212
    NEW_PRESET = 213
    NEW_GROUP = 214
    DELETE_GROUP = 215
    DELETE_PRESET = 216
    SAVE_PRESET = 217

    GET_SETTINGS = 230
    SET_SETTINGS = 231


VOICES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dx7programmer', 'voices')
VOICES_PRESETS_DIR = os.path.join(VOICES_DIR, 'preset')
VOICES_USER_DIR = os.path.join(VOICES_DIR, 'user')


class DX7Voice2(DX7Voice):
    def __init__(self, name=None):
        super().__init__(name)
        self._param_map = None
    
    def param_map(self) -> Dict[int, VoiceParameterValue]:
        if self._param_map is None:
            self._param_map = {}
            for i in range(6):
                self._param_map[21*(5-i) + 0] = self.op_bank[i].envelope.rate1
                self._param_map[21*(5-i) + 1] = self.op_bank[i].envelope.rate2
                self._param_map[21*(5-i) + 2] = self.op_bank[i].envelope.rate3
                self._param_map[21*(5-i) + 3] = self.op_bank[i].envelope.rate4
                self._param_map[21*(5-i) + 4] = self.op_bank[i].envelope.level1
                self._param_map[21*(5-i) + 5] = self.op_bank[i].envelope.level2
                self._param_map[21*(5-i) + 6] = self.op_bank[i].envelope.level3
                self._param_map[21*(5-i) + 7] = self.op_bank[i].envelope.level4
                self._param_map[21*(5-i) + 8] = self.op_bank[i].keyboard_level_scale.break_point
                self._param_map[21*(5-i) + 9] = self.op_bank[i].keyboard_level_scale.left_depth
                self._param_map[21*(5-i) + 10] = self.op_bank[i].keyboard_level_scale.right_depth
                self._param_map[21*(5-i) + 11] = self.op_bank[i].keyboard_level_scale.left_curve
                self._param_map[21*(5-i) + 12] = self.op_bank[i].keyboard_level_scale.right_curve
                self._param_map[21*(5-i) + 13] = self.op_bank[i].keyboard_rate_scaling
                self._param_map[21*(5-i) + 14] = self.op_bank[i].mod_sens_amplitude
                self._param_map[21*(5-i) + 15] = self.op_bank[i].key_vel_sens
                self._param_map[21*(5-i) + 16] = self.op_bank[i].output_level
                self._param_map[21*(5-i) + 17] = self.op_bank[i].osc_mode
                self._param_map[21*(5-i) + 18] = self.op_bank[i].freq_coarse
                self._param_map[21*(5-i) + 19] = self.op_bank[i].freq_fine
                self._param_map[21*(5-i) + 20] = self.op_bank[i].detune

            self._param_map[126] = self.pitch_env.rate1
            self._param_map[127] = self.pitch_env.rate2
            self._param_map[128] = self.pitch_env.rate3
            self._param_map[129] = self.pitch_env.rate4
            self._param_map[130] = self.pitch_env.level1
            self._param_map[131] = self.pitch_env.level2
            self._param_map[132] = self.pitch_env.level3
            self._param_map[133] = self.pitch_env.level4
            self._param_map[134] = self.algorithm_sel
            self._param_map[135] = self.feedback
            self._param_map[136] = self.osc_sync
            self._param_map[137] = self.lfo.speed
            self._param_map[138] = self.lfo.delay
            self._param_map[139] = self.lfo.pmd
            self._param_map[140] = self.lfo.amd
            self._param_map[141] = self.lfo.sync
            self._param_map[142] = self.lfo.wave
            self._param_map[143] = self.mod_sens_pitch
            self._param_map[144] = self.transpose
            self._param_map[155] = self.op_enable
                    
        return self._param_map
    
    def keys(self):
        return self.param_map().keys()
    
    def __setitem__(self, k: int, __value: int) -> None:
        p = self.param_map()[k]
        assert __value >= p.min and __value <= p.max
        p.value = __value
    
    def __getitem__(self, k: int):
        return self.param_map()[k]
    

def get_voice_as_messages(voice: DX7Voice2=None):
    global current_voice
    if voice is None:
        voice = current_voice
    return [[k, voice[k].value] for k in voice.keys()]

async def broadcast(msg):
    for c in connections.copy():
        try:
            await c.send(msg)
        except ConnectionClosed:
            connections.remove(c)

def _list_groups(basedir):
    return [i for i in os.listdir(basedir) if os.path.isdir(os.path.join(basedir, i))]

def list_user_groups():
    return _list_groups(VOICES_USER_DIR)

def list_preset_groups():
    return _list_groups(VOICES_PRESETS_DIR)

def list_voices(groupname: str):
    if groupname in list_user_groups():
        return [i for i in os.listdir(os.path.join(VOICES_USER_DIR, groupname)) if i.endswith('.syx')]
    elif groupname in list_preset_groups():
        return [i for i in os.listdir(os.path.join(VOICES_PRESETS_DIR, groupname)) if i.endswith('.syx')] 

async def load_voice(category: str, groupname: str, filename: str):
    global current_voice, current_voice_path
    vpath = os.path.join(VOICES_DIR, category, groupname, filename)
    if(os.path.exists(vpath)):
        current_voice = DX7Voice2.from_file(vpath)
        current_voice_path = [category, groupname, filename]
        dx7.update_voice(current_voice)
        await broadcast(json.dumps(get_voice_as_messages()))
        await broadcast(json.dumps([MessageIDs.LOAD_VOICE, current_voice_path]))
    else:
        print('[ER] Voice not found')

def dump_presets():
    return {
        'preset': {g: list_voices(g) for g in list_preset_groups()},
        'user': {g: list_voices(g) for g in list_user_groups()}
    }  

connections = []
dx7 = DX7Controller()
dx7.set_passthrough_device_in

current_voice_path = []
current_voice = DX7Voice2()

asyncio.run(load_voice('preset', list_preset_groups()[0], (list_voices(list_preset_groups()[0])[0])))


async def handle(websocket):
    global connections, current_voice
    async for message in websocket:
        msgs = json.loads(message)
        if not isinstance(msgs[0], list):
            msgs = [msgs]
        for msg in msgs:
            if msg[0] < 156:
                p = current_voice[msg[0]]
                p.value = msg[1]
                dx7.update_param(p)
            if msg[0] == MessageIDs.SUBSCRIBE:
                if websocket not in connections:
                    connections.append(websocket)
            elif msg[0] == MessageIDs.VOICE_DUMP:
                await websocket.send(json.dumps(get_voice_as_messages()))
            elif msg[0] == MessageIDs.GET_SETTINGS:
                # Get settings
                await websocket.send(json.dumps([MessageIDs.SET_SETTINGS, {
                    'midi_in': {
                        'choices': dx7.get_inports(),
                        'value': dx7.get_device_in()
                    },
                    'midi_out': {
                        'choices': dx7.get_outports(),
                        'value': dx7.get_device_out()
                    },
                    'midi_thru': {
                        'choices': dx7.get_inports(),
                        'value': dx7.get_passthrough_device_in()
                    },
                    'vel_correction':  dx7.get_velocity_correction()
                }]))
            elif msg[0] == MessageIDs.SET_SETTINGS:
                # Set settings
                print(f"Updating settings: {msg[1]}")
                if 'midi_out' in msg[1]:
                    dx7.set_device_out(msg[1]['midi_out']['value'])
                if 'midi_in' in msg[1]:
                    dx7.set_device_in(msg[1]['midi_in']['value'])
                if 'midi_thru' in msg[1]:
                    dx7.set_passthrough_device_in(msg[1]['midi_thru']['value'])
                if 'vel_correction' in msg[1]:
                    dx7.set_velocity_correction(msg[1]['vel_correction'])
            elif msg[0] == MessageIDs.PRESET_DUMP:
                await websocket.send(json.dumps([MessageIDs.PRESET_DUMP, dump_presets()]))
                await websocket.send(json.dumps([MessageIDs.LOAD_VOICE, current_voice_path]))
            elif msg[0] == MessageIDs.LOAD_VOICE:
                print(f'Loading voice: {"/".join(msg[1])}')
                await load_voice(*msg[1])
            elif msg[0] == MessageIDs.NEW_GROUP:
                # New group
                print(f'Creating new group: {msg[1]}')
                os.mkdir(os.path.join(VOICES_DIR, msg[1]))
                await broadcast(json.dumps([MessageIDs.PRESET_DUMP, dump_presets()]))

async def main():
    async with serve(handle, "0.0.0.0", 5000):
        await asyncio.Future()  # run forever

asyncio.run(main())
