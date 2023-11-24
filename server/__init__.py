import asyncio
from typing import Any, List
from websockets.server import serve
from websockets.legacy.protocol import broadcast
from websockets.exceptions import *
import json
from typing import Dict
import os
import sys
import shutil

from .dx7programmer import DX7Controller, DX7Voice, VoiceParameterValue, DX7VoiceBank

VERSION = "1.0-beta"

from .message import *


VOICES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dx7programmer', 'voices')
VOICES_PRESETS_DIR = os.path.join(VOICES_DIR, 'preset')
VOICES_USER_DIR = os.path.join(VOICES_DIR, 'user')


class CategoryManager:
    def __init__(self, name: str) -> None:
        self._name = name
        assert os.path.exists(self.dirpath())
    @property
    def name(self):
        return self._name
    
    def dirpath(self):
        return os.path.join(VOICES_DIR, self._name)
    
    def __getitem__(self, v: int):
        return BankManager.fromDir(os.path.join(self.dirpath(), self.listBankDirs(self.dirpath())[v]))

    def __len__(self):
        return len(self.listBankDirs(self.dirpath()))
    
    def initBank(self, bankName: str):
        bankDirname = f'{bankName}'
        bankDirpath = os.path.join(VOICES_DIR, self.name, bankDirname)
        assert not os.path.exists(bankDirpath)

        os.mkdir(bankDirpath)
        for i in range(32):
            name = f'{bankName[:7]:7s} {i:02}'
            vpath = os.path.join(bankDirpath, f'{i:02}_{name.replace(" ", "_")}.syx')
            DX7Voice2(name).save(vpath)

        return BankManager.fromDir(bankDirpath)
    
    @staticmethod
    def listBankDirs(dirpath) -> List[str]:
        to_ret = [i for i in os.listdir(dirpath) if BankManager.IsBankDir(os.path.join(dirpath, i))]
        to_ret.sort()
        return to_ret
    

    def newBankFrom(self, name: str, bank: DX7VoiceBank):
        name = name.strip()
        if name in self.listBankDirs(self.dirpath()):
            raise FileExistsError('User bank with name {name} already exists')
        bdpath = os.path.join(self.dirpath(), name)
        os.mkdir(bdpath)
        for i in range(len(bank)):
            bank[i].save(os.path.join(bdpath, f'{i:02}_{bank[i].name.value}:10.syx'.replace(' ', '_')))

class BankManager:
    def __init__(self, category: str, index: int, name: str):
        self._category = category
        self._index = index
        self._name = name
        assert os.path.exists(self.dirpath()), f'Bank dir not found: {self.dirpath()}'

    @property
    def category(self):
        return self._category
    
    @property
    def index(self) -> int:
        return self._index
    
    @property
    def name(self):
        return self._name
    
    def dirpath(self):
        return os.path.join(VOICES_DIR, self.category, self.name)

    @staticmethod
    def listVoiceFiles(dirpath):
        to_ret = [i for i in os.listdir(dirpath) if VoiceManager.IsVoiceFile(os.path.join(dirpath, i))]
        to_ret.sort()
        return to_ret
    
    def voices(self):
        return [VoiceManager.fromFile(os.path.join(self.dirpath(), f)) for f in self.listVoiceFiles(self.dirpath())]
    
    def __getitem__(self, v: int):
        return VoiceManager.fromFile(os.path.join(self.dirpath(), self.listVoiceFiles(self.dirpath())[v]))

    def __len__(self):
        return len(self.listVoiceFiles(self.dirpath()))
    
    @classmethod
    def fromDir(cls, dirpath: str):
        catDirpath = os.path.dirname(dirpath)
        category = os.path.basename(catDirpath)
        bankName = os.path.basename(dirpath)
        i = CategoryManager.listBankDirs(catDirpath).index(bankName)
        return cls(category, i, bankName)
    
    @staticmethod
    def IsBankDir(dirpath: str):
        if not os.path.isdir(dirpath): return False

        return True
    
    def delete(self):
        shutil.rmtree(self.dirpath())


class VoiceManager:
    def __init__(self, category: str, bank: int, index: int) -> None:
        self._category = category
        self._bank = bank
        self._index = index

    @property
    def category(self):
        return self._category
    
    @property
    def bankIndex(self):
        return self._bank
    
    @property
    def index(self):
        return self._index
    
    def name(self):
        return self.voice().name.value
    
    def bank(self):
        return CategoryManager(self.category)[self.bankIndex]
    
    def filepath(self):
        b = self.bank()
        return os.path.join(b.dirpath(), BankManager.listVoiceFiles(b.dirpath())[self.index])

    def voice(self):
        return DX7Voice2.from_file(self.filepath())

    @classmethod
    def fromFile(cls, filepath: str):
        assert filepath.startswith(VOICES_DIR)
        relpath = filepath[len(VOICES_DIR):]
        relpath = relpath.lstrip(os.path.sep)
        assert len(relpath.split('/')) == 3, f'unexpected voice filepath: {relpath}'
        cat, bd, vf = relpath.split('/', 3)
        bi = CategoryManager.listBankDirs(os.path.join(VOICES_DIR, cat)).index(bd)
        vi, vname = vf.split('_', 1)
        vi = int(vi)

        return cls(cat, bi, vi)

    @staticmethod
    def IsVoiceFile(filepath: str):
        if not os.path.isfile(filepath): return False
        if not filepath.endswith('.syx'): return False
        return True
    

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

    @classmethod
    def from_file(cls, filepath):
        i = os.path.basename(filepath).split('_')[0]
        i = int(i)
        with open(filepath, 'rb') as fp:
            to_ret = cls.from_sysex(fp.read())
        to_ret.index = i
        return to_ret

def get_voice_as_messages(voice: DX7Voice2=None):
    global current_voice
    if voice is None:
        voice = current_voice

    print(current_voice_path)
    return [[k, voice[k].value] for k in voice.keys()] + [[MessageIDs.VOICE_NAME, voice.name.value],]

async def broadcast(msg):
    for c in connections.copy():
        try:
            await c.send(msg)
        except ConnectionClosed:
            connections.remove(c)

async def handle_voice_init():
    global current_voice
    current_voice = DX7Voice2(current_voice.name.value)
    print('INIT')
    await broadcast(json.dumps(get_voice_as_messages(current_voice)))

async def handle_voice_load_messge(msg: VoiceLoadMessage):
    global current_voice, current_voice_path
    try:
        vm = CategoryManager(msg.category())[msg.bankIndex()][msg.voiceIndex()]
        current_voice = vm.voice()
        current_voice_path = [msg.category(), msg.bankIndex(), msg.voiceIndex()]

        print(f'Loaded voice: {vm.filepath()}')
        dx7.update_voice(current_voice)
        await broadcast(json.dumps(get_voice_as_messages(current_voice)))
        await broadcast(json.dumps(msg))
    except ValueError as e:
        print(f'[ER] {e}')
        
async def handle_voice_store_messge(msg: VoiceStoreMessage):
    global current_voice, current_voice_path
    old_filepath = CategoryManager(msg.category())[msg.bankIndex()][msg.voiceIndex()].filepath()
    new_filepath = os.path.join(os.path.dirname(old_filepath), f'{msg.voiceIndex():02}_{current_voice.name.value.replace(" ", "_")}.syx')
    if old_filepath != new_filepath:
        os.remove(old_filepath)
    current_voice.save(new_filepath)
    current_voice_path = [msg.category(), msg.bankIndex(), msg.voiceIndex()]
    await broadcast(json.dumps([MessageIDs.BANK_DUMP, dump_presets()]))
    await broadcast(json.dumps([MessageIDs.VOICE_LOAD, current_voice_path]))

def dump_presets():
    pm = CategoryManager('preset')
    um = CategoryManager('user')
    return {
        'preset': [{"name": pm[i].name, 'voices': [v.name() for v in pm[i].voices()]} for i in range(len(pm))],
        'user': [{'name': um[i].name, 'voices': [v.name() for v in um[i].voices()]} for i in range(len(um))]
    }  

connections = []
dx7 = DX7Controller()
dx7.set_passthrough_device_in

current_voice_path = ['preset', 0, 0]
current_voice = CategoryManager('preset')[0][0].voice()


async def handle(websocket):
    global connections, current_voice
    async for message in websocket:
        msgs = json.loads(message)
        if not isinstance(msgs[0], list):
            msgs = [msgs]
        for msg in msgs:
            msgId = Message.getId(msg)
            if msgId < 156:
                p = current_voice[msg[0]]
                p.value = msg[1]
                dx7.update_param(p)
            elif msgId == SubscribeMessage.id():
                if websocket not in connections:
                    connections.append(websocket)
            elif msgId == MessageIDs.VOICE_DUMP:
                await websocket.send(json.dumps(get_voice_as_messages(current_voice)))
                await websocket.send(json.dumps([MessageIDs.VOICE_LOAD, current_voice_path]))
            elif msgId == MessageIDs.BANK_DUMP:
                await websocket.send(json.dumps([MessageIDs.BANK_DUMP, dump_presets()]))
            elif msgId == GetSettingsMessage.id():
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
            elif msgId == SetSettingsMessage.id():
                msg = SetSettingsMessage(msg)
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
            elif msgId == MessageIDs.VOICE_DUMP:
                await websocket.send(json.dumps([MessageIDs.VOICE_DUMP, get_voice_as_messages(current_voice)]))
                await websocket.send(json.dumps([MessageIDs.VOICE_LOAD, current_voice_path]))
            elif msgId == VoiceLoadMessage.id():
                msg = VoiceLoadMessage(msg)
                await handle_voice_load_messge(msg)
            elif msgId == VoiceNameMessage.id():
                msg = VoiceNameMessage(msg)
                current_voice.name.value = msg.voiceName()
                for p in current_voice.name.toParameterValues():
                    dx7.update_param(p)
                await broadcast(json.dumps([MessageIDs.VOICE_NAME, current_voice.name.value]))
            elif msgId == VoiceStoreMessage.id():
                msg = VoiceStoreMessage(msg)
                if(msg.category() != 'user'):
                    await websocket.send(json.dumps([MessageIDs.ERROR_MESSAGE, 'Cannot overwrite non-user bank']))
                else:
                    await handle_voice_store_messge(msg)
            elif msgId == MessageIDs.VOICE_INIT:
                await handle_voice_init()
            elif msgId == NewUserBankMessage.id():
                msg = NewUserBankMessage(msg)
                # New group
                print(f'Creating new bank: {msg.bankName()}')
                try:
                    bm = CategoryManager('user').initBank(msg.bankName())
                    await broadcast(json.dumps([MessageIDs.BANK_DUMP, dump_presets()]))
                except Exception as e:
                    await websocket.send(json.dumps([MessageIDs.ERROR_MESSAGE, str(e)]))

            elif msgId == DeleteUserBankMessage.id():
                msg = DeleteUserBankMessage(msg)
                if msg.bankCategory() != 'user':
                    await websocket.send(json.dumps([MessageIDs.ERROR_MESSAGE, 'Cannot delete non-user bank']))
                else:
                    try:
                        CategoryManager('user')[msg.bankIndex()].delete()
                        print(f'[OK] Bank deleted')
                        await broadcast(json.dumps([MessageIDs.BANK_DUMP, dump_presets()]))
                    except Exception as e:
                        await websocket.send(json.dumps([MessageIDs.ERROR_MESSAGE, str(e)]))
            elif msgId == MessageIDs.BANK_UPLOAD:
                newBankName = msg[1][0]
                msgData = msg[1][1].encode()
                newBankHeader = msgData[:3]
                if not newBankHeader.startswith(bytes([0xEF, 0xBF, 0xBD])):
                    raise ValueError('Unexpected starting bytes: ', newBankHeader)
                msgData = bytes([240]) + msgData[3:]
                newBank = DX7VoiceBank.from_sysex(msgData)
                CategoryManager('user').newBankFrom(newBankName, newBank)
                await broadcast(json.dumps([MessageIDs.BANK_DUMP, dump_presets()]))
            else:
                print('[WN] Unhandled message: ')
                print(msg)

async def main(args = None):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', default='0.0.0.0', help='Host on which to run the server (default 0.0.0.0)')
    ap.add_argument('--port', '-p', default=5000, type=int, help='Port on which to run the server (default 5000)')

    pargs = ap.parse_args(args)

    async with serve(handle, pargs.host, pargs.port):

        print(f'[OK] Serving  {pargs.host}:{pargs.port}')
        await asyncio.Future()  # run forever

asyncio.run(main())
