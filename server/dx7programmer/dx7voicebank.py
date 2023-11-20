import os
from typing import List, Union, Dict, Tuple
from . import util

USE_VALUE_CLIPPING = True


class ChecksumFailedError(ValueError):
    pass


def _id_to_max(param_id: int):
    if param_id < 126:
        tmp = param_id % 21
        if tmp in (11, 12, 14):
            return 3
        if tmp in (13, 15):
            return 7
        if tmp == 17:
            return 1
        if tmp == 18:
            return 31
        if tmp == 20:
            return 14
    elif param_id == 134:
        return 31
    elif param_id in (135, 143):
        return 7
    elif param_id in (136, 141):
        return 1
    elif param_id == 142:
        return 4
    elif param_id == 144:
        return 48
    elif 145 <= param_id < 155:
        return 127
    elif param_id == 155:
        return 0b01111111
    return 99


class VoiceParameterValue:
    def __init__(self, id=None, val=0, max=None):
        self._value = val
        self._min = 0
        self._max = max if max is not None else _id_to_max(id) if id is not None else 99
        self.param_id = id
        self.on_change = util.Signal()

    def encode(self, batch_mode=False):
        return bytes([self.value])

    def set_from_data_slider(self, val: int):
        self.value = round(self._max*(val/127))

    def to_data_slider_val(self):
        return round(127*self.value/self._max)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v: int):
        global USE_VALUE_CLIPPING
        self._value = int(v)
        if self._value > self._max:
            if not USE_VALUE_CLIPPING:
                raise ValueError(v)
            self._value = self._max
        elif self._value < self._min:
            if not USE_VALUE_CLIPPING:
                raise ValueError(v)
            self._value = self._min
        self.on_change(self)

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    def __int__(self):
        return self.value
    
    def to_param_change_sysex(self, midi_channel: int):
        return bytes([
            0b11110000,
            67,
            0b00010000 + (midi_channel & 0b1111),
            0b00000000 + (self.param_id >> 7) & 0b11,
            self.param_id & 0b01111111,
            self.value & 0b01111111,
            0b11110111
        ])


class ParameterGroupBase:
    def vals(self) -> List[VoiceParameterValue]:
        to_ret = []
        vars_tmp = vars(self)
        for k, v in vars_tmp.items():
            if type(v) is VoiceParameterValue or issubclass(type(v), VoiceParameterValue):
                to_ret.append(v)
            elif issubclass(type(v), ParameterGroupBase):
                to_ret += v.vals()
        to_ret.sort(key=lambda v: v.param_id)
        return to_ret

    def val_map(self) -> Dict[int, VoiceParameterValue]:
        return {v.param_id: v for v in self.vals()}

    def update(self, data: Union[bytes, List[VoiceParameterValue]], throw_errors=False):
        map = self.val_map()
        if type(data) is bytes:
            for b1, b2 in zip((data[i], data[i+1]) for i in range(0, len(data), 2)):
                if b1 in map:
                    map[b1].value = b2
                elif throw_errors:
                    raise KeyError(b1)
        elif type(data[0]) is VoiceParameterValue:
            for param in data:
                if param.param_id in map:
                    map[param.param_id].value = param.value
                elif throw_errors:
                    raise KeyError(param.param_id)
        else:
            raise TypeError(type(data))

    def encode(self, batch_mode=False):
        return b''.join([v.encode(batch_mode=batch_mode) for v in self.vals()])


class Envelope(ParameterGroupBase):
    def __init__(self, id_start: int):
        super(Envelope, self).__init__()
        self.id_start = id_start
        self.rate1 = VoiceParameterValue(id_start)
        self.rate2 = VoiceParameterValue(id_start+1)
        self.rate3 = VoiceParameterValue(id_start+2)
        self.rate4 = VoiceParameterValue(id_start+3)
        self.level1 = VoiceParameterValue(id_start+4)
        self.level2 = VoiceParameterValue(id_start+5)
        self.level3 = VoiceParameterValue(id_start+6)
        self.level4 = VoiceParameterValue(id_start+7)

    def points(self):
        return [(self.rate1, self.level1),
                (self.rate2, self.level2),
                (self.rate3, self.level3),
                (self.rate4, self.level4)]

    def __bytes__(self):
        return bytes([
            self.rate1.value,
            self.rate2.value,
            self.rate3.value,
            self.rate4.value,
            self.level1.value,
            self.level2.value,
            self.level3.value,
            self.level4.value
        ])

    @classmethod
    def decode(cls, data: bytes, id_start: int):
        if not len(data) == 8:
            raise ValueError(f'Invalid envelope data length: {len(data)} - {data.hex()}')
        e = Envelope(id_start)
        e.rate1.value = data[0]
        e.rate2.value = data[1]
        e.rate3.value = data[2]
        e.rate4.value = data[3]
        e.level1.value = data[4]
        e.level2.value = data[5]
        e.level3.value = data[6]
        e.level4.value = data[7]
        return e


class KeyboardLevelScale(ParameterGroupBase):
    def __init__(self, op_number: int):
        super(KeyboardLevelScale, self).__init__()
        self.break_point = VoiceParameterValue((5-op_number) * 21 + 8)
        self.left_depth = VoiceParameterValue((5-op_number) * 21 + 9)
        self.right_depth = VoiceParameterValue((5-op_number) * 21 + 10)
        self.left_curve = VoiceParameterValue((5-op_number) * 21 + 11)
        self.right_curve = VoiceParameterValue((5-op_number) * 21 + 12)


class Operator(ParameterGroupBase):
    def __init__(self, op_number: int):
        super().__init__()
        if not op_number <= 6:
            raise ValueError(f'Invalid OP number: {op_number}')
        self.op_number = op_number

        param_id_start = 21*(5-op_number)

        self.envelope = Envelope(param_id_start)
        self.keyboard_level_scale = KeyboardLevelScale(op_number)
        self.keyboard_rate_scaling = VoiceParameterValue(param_id_start + 13)
        self.mod_sens_amplitude = VoiceParameterValue(param_id_start + 14)
        self.key_vel_sens = VoiceParameterValue(param_id_start + 15)
        self.output_level = VoiceParameterValue(param_id_start + 16)
        self.osc_mode = VoiceParameterValue(param_id_start + 17)
        self.freq_coarse = VoiceParameterValue(param_id_start + 18)
        self.freq_fine = VoiceParameterValue(param_id_start + 19)
        self.detune = VoiceParameterValue(param_id_start + 20)

    def __bytes__(self):
        return self.encode(True)

    def encode(self, batch_mode=False):
        if batch_mode:
            return bytes([
                self.envelope.rate1.value,
                self.envelope.rate2.value,
                self.envelope.rate3.value,
                self.envelope.rate4.value,
                self.envelope.level1.value,
                self.envelope.level2.value,
                self.envelope.level3.value,
                self.envelope.level4.value,
                self.keyboard_level_scale.break_point.value,
                self.keyboard_level_scale.left_depth.value,
                self.keyboard_level_scale.right_depth.value,
                (self.keyboard_level_scale.right_curve.value << 2) | self.keyboard_level_scale.left_depth.value,
                (self.detune.value << 3) | self.keyboard_rate_scaling.value,
                (self.key_vel_sens.value << 2) | self.mod_sens_amplitude.value,
                self.output_level.value,
                (self.freq_coarse.value << 1) | self.osc_mode.value,
                self.freq_fine.value
            ])
        else:
            return bytes([
                self.envelope.rate1.value,
                self.envelope.rate2.value,
                self.envelope.rate3.value,
                self.envelope.rate4.value,
                self.envelope.level1.value,
                self.envelope.level2.value,
                self.envelope.level3.value,
                self.envelope.level4.value,
                self.keyboard_level_scale.break_point.value,
                self.keyboard_level_scale.left_depth.value,
                self.keyboard_level_scale.right_depth.value,
                self.keyboard_level_scale.left_curve.value,
                self.keyboard_level_scale.right_curve.value,
                self.keyboard_rate_scaling.value,
                self.mod_sens_amplitude.value,
                self.key_vel_sens.value,
                self.output_level.value,
                self.osc_mode.value,
                self.freq_coarse.value,
                self.freq_fine.value,
                self.detune.value
            ])

    @classmethod
    def decode(cls, data: bytes, op_number):
        if not len(data) in (17, 21):
            raise ValueError(f'Unexpected Data Length for Operator: {len(data)} (Expected 17 or 21)')
        v = cls(op_number)
        v.envelope.rate1.value = data[0]
        v.envelope.rate2.value = data[1]
        v.envelope.rate3.value = data[2]
        v.envelope.rate4.value = data[3]
        v.envelope.level1.value = data[4]
        v.envelope.level2.value = data[5]
        v.envelope.level3.value = data[6]
        v.envelope.level4.value = data[7]
        v.keyboard_level_scale.break_point.value = data[8]
        v.keyboard_level_scale.left_depth.value = data[9]
        v.keyboard_level_scale.right_depth.value = data[10]
        if len(data) == 17:
            v.keyboard_level_scale.right_curve.value = data[11] >> 2
            v.keyboard_level_scale.left_curve.value = data[11] & 0x3
            v.detune.value = data[12] >> 3
            v.keyboard_rate_scaling.value = data[12] & 0x7
            v.key_vel_sens.value = data[13] >> 2
            v.mod_sens_amplitude.value = data[13] & 0x3
            v.output_level.value = data[14]
            v.freq_coarse.value = data[15] >> 1
            v.osc_mode.value = data[15] & 1
            v.freq_fine.value = data[16]
        else:
            v.keyboard_level_scale.left_curve.value = data[11]
            v.keyboard_level_scale.right_curve.value = data[12]
            v.keyboard_rate_scaling.value = data[13]
            v.mod_sens_amplitude.value = data[14]
            v.key_vel_sens.value = data[15]
            v.output_level.value = data[16]
            v.osc_mode.value = data[17]
            v.freq_coarse.value = data[18]
            v.freq_fine.value = data[19]
            v.detune.value = data[20]
        return v


class OperatorBank(ParameterGroupBase, List[Operator]):
    def __init__(self, operators: List[Operator] = None):
        super(OperatorBank, self).__init__([Operator(i) for i in range(6)] if operators is None else operators)

    def __bytes__(self):
        return b''.join([bytes(op) for op in self[::-1]])

    def vals(self) -> List[VoiceParameterValue]:
        to_ret = []
        for op in self:
            to_ret += op.vals()
        return to_ret

    def encode(self, batch_mode=False):
        return b''.join(op.encode(batch_mode=batch_mode) for op in self[::-1])

    @classmethod
    def decode(cls, data: bytes):
        nbytes_per_osc = len(data)//6
        if not nbytes_per_osc in (21, 17):
            raise ValueError(f'Unexpected data length for OP bank: {len(data)}')
        return OperatorBank([Operator.decode(data[(5-i)*nbytes_per_osc:(6-i)*nbytes_per_osc], i) for i in range(6)])


class LFO(ParameterGroupBase):
    def __init__(self):
        super(LFO, self).__init__()
        self.speed = VoiceParameterValue(137)
        self.delay = VoiceParameterValue(138)
        self.pmd = VoiceParameterValue(139)
        self.amd = VoiceParameterValue(140)
        self.sync = VoiceParameterValue(141)
        self.wave = VoiceParameterValue(142)

    def encode(self, batch_mode=False):
        if batch_mode:
            return bytes([

            ])


class OperatorEnable(VoiceParameterValue):
    def __init__(self):
        super(OperatorEnable, self).__init__(155)
        self.value = 0b111111

    def osc_enabled(self, osc_number):
        return self.value & (1 << (5-osc_number)) != 0

    def set_osc_enable(self, osc_number, en: bool):
        if en:
            self.value |= (1 << (5-osc_number))
        else:
            self.value &= (-(1 << (5-osc_number)) - 1)


class NameParam(ParameterGroupBase):
    def __init__(self, name=None):
        super(NameParam, self).__init__()
        self.c0 = VoiceParameterValue( 145)
        self.c1 = VoiceParameterValue(146)
        self.c2 = VoiceParameterValue(147)
        self.c3 = VoiceParameterValue(148)
        self.c4 = VoiceParameterValue(149)
        self.c5 = VoiceParameterValue(150)
        self.c6 = VoiceParameterValue(151)
        self.c7 = VoiceParameterValue(152)
        self.c8 = VoiceParameterValue(153)
        self.c9 = VoiceParameterValue(154)

        self.on_change = util.Signal()

        if name is None:
            name = ''

        self.value = name

    def update(self, data: List[VoiceParameterValue], throw_errors=False):
        map = self.val_map()
        changed = False
        for d in data:
            if d.param_id in map:
                map[d.param_id].value = d.value
                changed = True
        if changed:
            self.on_change.emit(self)

    @property
    def value(self):
        return bytes([c.value for c in self.vals()]).decode()

    @value.setter
    def value(self, v: str):
        v_bytes = f'{v:10}'.encode()
        cs = self.vals()
        for vb, c in zip(v_bytes, cs):
            c.value = vb
        self.on_change.emit(self)

    def __bytes__(self):
        return bytes([c.value for c in self.vals()])


class DX7Voice(ParameterGroupBase):
    def __init__(self, name=None):
        self.op_bank = OperatorBank()
        self.pitch_env = Envelope(126)
        self.algorithm_sel = VoiceParameterValue(134)
        self.feedback = VoiceParameterValue(135)
        self.osc_sync = VoiceParameterValue(136)
        self.lfo = LFO()
        self.mod_sens_pitch = VoiceParameterValue(143)
        self.transpose = VoiceParameterValue(144)
        self.name = NameParam(name=name)
        self.op_enable = OperatorEnable()

        self._change_cb = None
        super(DX7Voice, self).__init__()

    def update(self, data: Union[bytes, List[VoiceParameterValue]], throw_errors=False):
        if type(data) is DX7Voice:
            data = DX7Voice.vals(data)
        super(DX7Voice, self).update(data)
        # Trigger name update
        self.name.value = self.name.value

    def __bytes__(self):
        return self.encode(True)

    def encode(self, batch_mode=False):
        to_ret = self.op_bank.encode(batch_mode=batch_mode)
        to_ret += self.pitch_env.encode(batch_mode=batch_mode)
        if batch_mode:
            to_ret += bytes([
                self.algorithm_sel.value,
                (self.osc_sync.value << 3) | self.feedback.value,
                self.lfo.speed.value,
                self.lfo.delay.value,
                self.lfo.pmd.value,
                self.lfo.amd.value,
                (self.mod_sens_pitch.value << 4) | (self.lfo.wave.value << 1) | self.lfo.sync.value,
                self.transpose.value
            ])
        else:
            to_ret += bytes([
                self.algorithm_sel.value,
                self.feedback.value,
                self.osc_sync.value,
                self.lfo.speed.value,
                self.lfo.delay.value,
                self.lfo.pmd.value,
                self.lfo.amd.value,
                self.lfo.sync.value,
                self.lfo.wave.value,
                self.mod_sens_pitch.value,
                self.transpose.value,
            ])

        to_ret += bytes(self.name)
        return to_ret

    @classmethod
    def decode(cls, data: bytes):
        if len(data) not in (128, 155):
            raise ValueError(f'Unexpected Voice Data Length: {len(data)} (Expected 128 or 155)')
        v = cls()
        if len(data) == 128:
            v.op_bank = OperatorBank.decode(data[:102])
            v.pitch_env = Envelope.decode(data[102:110], 126)
            v.algorithm_sel.value = data[110]
            v.osc_sync.value = data[111] >> 3
            v.feedback.value = data[111] & 0x7
            v.lfo.speed.value = data[112]
            v.lfo.delay.value = data[113]
            v.lfo.pmd.value = data[114]
            v.lfo.amd.value = data[115]
            v.lfo.sync.value = data[116] & 0x1
            v.lfo.wave.value = (data[116] >> 1 & 0x7)
            v.mod_sens_pitch.value = data[116] >> 4
            v.transpose.value = data[117]
            v.name.value = data[118:].decode()
        else:
            v.op_bank = OperatorBank.decode(data[:126])
            v.pitch_env = Envelope.decode(data[126:134], 126)
            v.algorithm_sel.value = data[134]
            v.feedback.value = data[135]
            v.osc_sync.value = data[136]
            v.lfo.speed.value = data[137]
            v.lfo.delay.value = data[138]
            v.lfo.pmd.value = data[139]
            v.lfo.amd.value = data[140]
            v.lfo.sync.value = data[141]
            v.lfo.wave.value = data[142]
            v.mod_sens_pitch.value = data[143]
            v.transpose.value = data[144]
            v.name.value = bytes(data[145:155]).decode()
        return v

    @classmethod
    def from_sysex(cls, data: bytes, ignore_checksum=False):
        if len(data) != 163:
            raise ValueError(f'Incomplete sysex data - expected 163 bytes, got {len(data)}')
        if not data[0] == 0b11110000:
            raise ValueError('Is not sysex data')
        if not data[3] == 0:
            if data[3] == 9:
                raise ValueError('Data is a voice bank, not a voice')
            else:
                raise ValueError(f'Invalid format: {data[3]}')

        data_size = (data[4] << 7) | data[5]

        if not ignore_checksum:
            checksum = data[161]
            if checksum != util.generate_checksum(data[6:161]):
                raise ChecksumFailedError(f'{checksum} != {util.generate_checksum(data[6:161])}')

        if data_size != 155:
            raise ValueError(f'Invalid data size: {data_size}')

        return cls.decode(data[6:161])

    def to_sysex(self, midi_channel=1):
        data = bytes([
            0b11110000,
            67,
            midi_channel-1,
            0
        ])

        data += bytes([1, 0x1b])

        data += self.op_bank.encode()
        data += self.pitch_env.encode()
        data += bytes([
            self.algorithm_sel.value,
            self.feedback.value,
            self.osc_sync.value,
            self.lfo.speed.value,
            self.lfo.delay.value,
            self.lfo.pmd.value,
            self.lfo.amd.value,
            self.lfo.sync.value,
            self.lfo.wave.value,
            self.mod_sens_pitch.value,
            self.transpose.value
        ])
        data += bytes(self.name)

        data += bytes([util.generate_checksum(data[6:])])
        data += bytes([0b11110111])

        return data

    def save(self, filepath):
        with open(filepath, 'wb') as fp:
            fp.write(self.to_sysex())

    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'rb') as fp:
            return cls.from_sysex(fp.read())

    @staticmethod
    def is_dx7_voice_sysex(filepath):
        with open(filepath, 'rb') as fp:
            header_data = fp.read(6)
            if any([
                    header_data[0] != 0b11110000,
                    header_data[1] != 47,
                    header_data[3] != 0
            ]):
                return False
            return True


class DX7VoiceBank(List[DX7Voice]):
    def __init__(self, voices: List[DX7Voice] = None, source_filepath=None):
        super(DX7VoiceBank, self).__init__([DX7Voice(name=f'Voice {i+1:02}') for i in range(32)] if voices is None else voices)
        self._source_filepath = source_filepath

    def get_source_filepath(self):
        return self._source_filepath

    def __bytes__(self):
        return b''.join([v.encode(True) for v in self])

    @classmethod
    def decode(cls, data: bytes):
        if not len(data) == 128*32:
            raise ValueError(f'Unexpected Voice Bank Data Length: {len(data)} (Expected {128*32})')
        return cls([DX7Voice.decode(data[i * 128:(i + 1) * 128]) for i in range(32)])

    def to_sysex(self, midi_channel=1):
        if not 1 <= midi_channel <= 16:
            raise ValueError(f'Invalid MIDI channel: {midi_channel}')
        data = bytes([
            0b11110000,
            67,
            midi_channel-1,
            9
        ])

        data += bytes([4096 >> 7, 4096 & 0x7F])
        voice_data = b''.join([v.encode(True) for v in self])
        data += voice_data
        data += bytes([util.generate_checksum(voice_data)])
        data += bytes([0b11110111])

        return data

    @classmethod
    def from_sysex(cls, data: bytes):
        if not data[0] == 0b11110000:
            raise ValueError(f'Invalid SYSEX Header: {data[0]:08b}')
        if not data[3] == 9:
            raise ValueError(f'Invalid Format for Voice Bank: {data[3]} (Expected 9)')

        data_size = (data[4] << 7) | data[5]
        if not data_size == 4096:
            raise ValueError(f'Invalid Data Size for Voice Bank: {data_size}')
        checksum = data[4102]
        if not checksum == util.generate_checksum(data[6:4102]):
            raise ChecksumFailedError(f'{checksum} != {util.generate_checksum(data[6:4102])}')
        return cls.decode(data[6:4102])

    def save(self, filepath):
        with open(filepath, 'wb') as fp:
            fp.write(self.to_sysex())

    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'rb') as fp:
            to_ret = cls.from_sysex(fp.read())
            to_ret._source_filepath = filepath
            return to_ret

    @staticmethod
    def is_dx7_bank_sysex(filepath: str):
        if not os.path.isfile(filepath) or not filepath.endswith('.syx'):
            return False

        with open(filepath, 'rb') as fp:
            header_data = fp.read(6)
            if any([
                    header_data[0] != 0b11110000,
                    header_data[1] != 67,
                    header_data[3] != 9
            ]):
                return False
            return True
