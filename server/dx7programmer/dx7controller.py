from .dx7voicebank import *
import rtmidi
import os
import json
from enum import Enum
from .util import Signal
from pygame import midi
import queue
from threading import Thread, Lock
from time import sleep

midi.init()


class MIDI_TYPE:
    KEY_ON = 9
    CC = 11
    PROGRAM_CHANGE = 12
    AFTERTOUCH = 13
    PB = 14
    SYSEX = 15


class DX7_CC:
    MOD_WHL = 1
    BRTH_CTL = 2
    FT_CTL = 4
    DATA_ENTRY_KNOB = 6
    SUSTAIN = 64
    PORTAMENTO_FT = 65
    DATA_ENTRY_UP = 96
    DATA_ENTRY_DWN = 97


class _ParamUpdateFlowController(Thread):
    class _EggTimer(Thread):
        def __init__(self, callback, param_id: int, sleep_time: float):
            super(_ParamUpdateFlowController._EggTimer, self).__init__()
            self._sleep_time = sleep_time
            self._param = param_id
            self._callback = callback

        def run(self) -> None:
            sleep(self._sleep_time)
            self._callback(self._param)

    def __init__(self, send_param_cb, send_active_sense_cb=None):
        super(_ParamUpdateFlowController, self).__init__()
        self._running = False
        self._last_submit_time_map = {}
        self._queue = {}
        self._queue_lock = Lock()
        self._queue_wait_lock = Lock()
        self._queue_wait_lock.acquire()
        self._update_threads = {}
        self._send_param = send_param_cb
        self._send_active_sense_cb = send_active_sense_cb
        self._last_param = None

    def run(self) -> None:
        self._running = True
        while self._running:
            if self._queue_wait_lock.acquire(True, 0.1):
                with self._queue_lock:
                    queue_copy = self._queue.copy()
                    self._queue.clear()
                for k in queue_copy:
                    self._last_param = queue_copy[k]
                    self._send_param(self._last_param)
                    
            else:
                if self._send_active_sense_cb is not None:
                    self._send_active_sense_cb()

    def submit(self, param: VoiceParameterValue):
        with self._queue_lock:
            self._queue[param.param_id] = param
            if self._queue_wait_lock.locked():
                self._queue_wait_lock.release()

    def join(self, timeout=None):
        self._running = False
        super(_ParamUpdateFlowController, self).join(timeout)


class DX7Controller:
    def _midi_rcv_cb(self, *args):
        midi_data = args[0][0]
        
        if len(midi_data) == 0:
            return
            
        midi_type = midi_data[0] >> 4

        if midi_type in (MIDI_TYPE.KEY_ON, MIDI_TYPE.PB, MIDI_TYPE.AFTERTOUCH):
            # Ignore
            return

        if midi_type == MIDI_TYPE.CC:
            control_number = midi_data[1]
            control_val = midi_data[2]
            if control_number == DX7_CC.DATA_ENTRY_KNOB:
                self.on_data_entry_slider_change(control_val)
            elif control_number == DX7_CC.DATA_ENTRY_UP:
                self.on_data_entry_nudge(1)
            elif control_number == DX7_CC.DATA_ENTRY_DWN:
                self.on_data_entry_nudge(-1)
        elif midi_type == MIDI_TYPE.PROGRAM_CHANGE:
            self.on_program_change(midi_data[1])

        elif midi_type == MIDI_TYPE.SYSEX:
            if midi_data[0] == 0xFE:
                # Ignore active sens
                return
            if len(midi_data) < 3:
                return

            substatus = midi_data[2] >> 4
            if substatus == 0:
                if midi_data[3] == 9:
                    self.on_bank_data_raw(bytes(midi_data))
                    bank = DX7VoiceBank.from_sysex(bytes(midi_data))
                    self.on_bank_data(bank)
                else:
                    if midi_data[3] != 0:
                        self.on_error(f'Unexpected Format Number: {midi_data[3]}')
                        return
                    try:
                        self.on_voice_raw_received(bytes(midi_data))
                        voice = DX7Voice.from_sysex(bytes(midi_data))
                        self.on_voice_received(voice)
                    except ChecksumFailedError as e:
                        self.on_error(f'Checksum failed: {e}')
                    except AssertionError:
                        self.on_error('Assertion error')
                    except ValueError as e:
                        self.on_error(str(e))
                        
            elif substatus == 1:
                # Param change
                param_group = midi_data[3] >> 2
                param_no = ((midi_data[3] & 0b11) << 7) | (midi_data[4] & 0x7F)
                param_val = midi_data[5]
                if param_group == 0:
                    self.on_param_change(VoiceParameterValue(param_no, param_val))
        else:
            print('Unhandled MIDI:', midi_data)

    def __init__(self):
        self._midi_input = rtmidi.MidiIn()
        self._passthrough_midi_input = rtmidi.MidiIn()
        self._midi_input.ignore_types(sysex=False)

        self._midi_output = None

        self.on_error = Signal()
        self.on_param_change = Signal()
        self.on_voice_received = Signal()
        self.on_voice_raw_received = Signal()
        self.on_data_entry_slider_change = Signal()
        self.on_data_entry_nudge = Signal()
        self.on_bank_data = Signal()
        self.on_bank_data_raw = Signal()
        self.on_program_change = Signal()

        self._param_out_flow_ctl = _ParamUpdateFlowController(self._send_param_update, self._send_active_sense)
        self._param_out_flow_ctl.start()

        self._config = _MidiSettings(self)
        self.set_channel(self._config.dx7_sysex_channel)
        try:
            self.set_device_out(self._config.dx7_device_out)
        except:
            print(f'[ER] Unable to set device out ({self._config.dx7_device_out})')
            raise
            self._config.dx7_device_out = None
            self.set_device_out(None)

        try:
            self.set_device_in(self._config.dx7_device_in)
        except:
            print(f'[ER] Unable to set device in ({self._config.dx7_device_in})')
            self._config.dx7_device_in = None
            self.set_device_in(None)

        try:
            self.set_passthrough_device_in(self._config.passthrough_device_in)
        except ValueError as e:
            print(f'[WN] {str(e)}, disabling passthrough device')
            self._config.passthrough_device_in = None
            self._config.save()

    def _device_name_to_id(self, name: str, input: bool):
        name = name.encode()
        for i in range(midi.get_count()):
            info = midi.get_device_info(i)
            if info[1] == name:
                if info[2] > 0 and input:
                    return i
                elif info[3] > 0:
                    if info[4] > 0:
                        print('[WN] Device is opened - may cause issues')
                    return i
        raise ValueError(name)

    def set_midi_settings(self, input_device, output_device, channel: int):
        self.set_device_in(input_device)
        self.set_device_out(output_device)
        self.set_channel(channel)
        self._config.save()

    def get_device_out(self):
        return self._config.dx7_device_out

    def get_device_in(self):
        return self._config.dx7_device_in

    def set_channel(self, channel: int):
        self._config.dx7_sysex_channel = channel
        self._config.save()

    def get_channel(self):
        return self._config.dx7_sysex_channel

    def set_device_in(self, device: str):
        self._midi_input.close_port()
        self._config.dx7_device_in = device if device in self.get_inports() else None
        if self._config.dx7_device_in is not None:
            self._midi_input.open_port(self.get_inports().index(device))
            self._midi_input.set_callback(self._midi_rcv_cb)
            print(f'Opened MIDI input: {self._config.dx7_device_in}')
        self._config.save()

    def set_device_out(self, device: str):
        self._config.dx7_device_out = device if device in self.get_outports() else None
        if self._config.dx7_device_out is not None:
            try:
                deviceid = self._device_name_to_id(self._config.dx7_device_out, False)
                if self._midi_output is not None:
                    if self._midi_output.device_id != deviceid:
                        self._midi_output.close()
                        self._midi_output = midi.Output(deviceid)
                else:
                    self._midi_output = midi.Output(deviceid)
                print(f'Opened MIDI output: {self._config.dx7_device_out}')
            except:
                raise

        self._config.save()

    def set_program(self, program_number: int):
        assert 0 <= program_number < 32
        cmd = [0b1100 << 4 | (self._config.dx7_sysex_channel - 1), program_number]
        if self._midi_output is not None:
            self._midi_output.write_sys_ex(0, bytes(cmd))

    def update_param(self, param: VoiceParameterValue):
        self._param_out_flow_ctl.submit(param)
    
    def _send_active_sense(self):
        if self._midi_output is not None:
            self._midi_output.write_sys_ex(0, bytes([0xF0, 0x43, 0b11110111]))

    def _send_param_update(self, param: VoiceParameterValue):
        # Select Param
        cmd = [0xF0,
               67,
               16 | (self.get_channel() - 1),
               (param.param_id >> 7) & 0b11,
               param.param_id & 0b01111111,
               param.value,
               0b11110111]
        if self._midi_output is not None:
            self._midi_output.write_sys_ex(0, bytes(cmd))

        # Fake data entry CC
        # cmd = [
        #     (MIDI_TYPE.CC << 4) | (self.get_channel() - 1),
        #     DX7_CC.DATA_ENTRY_KNOB,
        #     param.to_data_slider_val()
        # ]
        # self.midi_output.write(cmd)

    def get_inports(self):
        return self._midi_input.get_ports()

    def get_outports(self):
        return [midi.get_device_info(i)[1].decode() for i in range(midi.get_count()) if midi.get_device_info(i)[3] > 0]

    def update_voice(self, v: DX7Voice):
        cmd = v.to_sysex(self.get_channel())
        if self._midi_output is not None:
            self._midi_output.write_sys_ex(0, cmd)

    def update_bank(self, b: DX7VoiceBank):
        cmd = b.to_sysex(self.get_channel())
        if self._midi_output is not None:
            self._midi_output.write_sys_ex(0, cmd)

    def close(self):
        self._midi_input.close_port()
        if self._midi_output is not None:
            self._midi_output.close()
        self._param_out_flow_ctl.join()

    def _passthrough_in_callback(self, *args):
        if self._midi_output is not None:
            midi_data = args[0][0]
            midi_type = midi_data[0] >> 4
            if self._config.correct_midi_velocities:
                if midi_type == MIDI_TYPE.KEY_ON:
                    midi_data[2] = round(100*midi_data[2]/127)
            if len(midi_data) == 3:
                self._midi_output.write_short(*midi_data)

    def get_velocity_correction(self):
        return self._config.correct_midi_velocities

    def set_velocity_correction(self, correct: bool):
        self._config.correct_midi_velocities = correct
        self._config.save()

    def list_passthrough_devices(self):
        return self._passthrough_midi_input.get_ports()

    def get_passthrough_device_in(self):
        return self._config.passthrough_device_in

    def set_passthrough_device_in(self, device: str):
        if device == self._config.dx7_device_in and device is not None:
            raise ValueError('Passthrough loopback not allowed')
        self._passthrough_midi_input.close_port()
        if device is not None:
            found = False
            for i in range(self._passthrough_midi_input.get_port_count()):
                if self._passthrough_midi_input.get_port_name(i) == device:
                    found = True
                    self._passthrough_midi_input.open_port(i)
                    self._passthrough_midi_input.set_callback(self._passthrough_in_callback)
                    print(f'Opened passthrough input: {device}')
            if not found:
                raise ValueError("Invalid device input")
        self._config.passthrough_device_in = device
        self._config.save()
        pass


class _MidiSettings(dict):
    SETTINGS_FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'midi_settings.json')

    def __init__(self, c: DX7Controller):
        inports = c.get_inports()
        outports = c.get_outports()
        super(_MidiSettings, self).__init__({
            'device_in': inports[0] if len(inports) > 0 else None,
            'device_out': outports[0] if len(outports) > 0 else None,
            'channel': 1,
            'passthrough_device_in': None,
            'correct_midi_vel': True
        })
        self.reload()

    def reload(self):
        if os.path.exists(self.SETTINGS_FILEPATH):
            with open(self.SETTINGS_FILEPATH, 'r') as fp:
                self.update(json.loads(fp.read()))

    def save(self):
        with open(self.SETTINGS_FILEPATH, 'w') as fp:
            fp.write(json.dumps(self))

    @property
    def dx7_device_in(self):
        return self['device_in']

    @property
    def dx7_device_out(self):
        return self['device_out']

    @property
    def dx7_sysex_channel(self):
        return self['channel']

    @dx7_device_in.setter
    def dx7_device_in(self, device: str):
        self['device_in'] = device

    @dx7_device_out.setter
    def dx7_device_out(self, device: str):
        self['device_out'] = device

    @dx7_sysex_channel.setter
    def dx7_sysex_channel(self, c: int):
        self['channel'] = c

    @property
    def passthrough_device_in(self):
        return self['passthrough_device_in']

    @passthrough_device_in.setter
    def passthrough_device_in(self, device):
        self['passthrough_device_in'] = device

    @property
    def correct_midi_velocities(self):
        return self['correct_midi_vel']

    @correct_midi_velocities.setter
    def correct_midi_velocities(self, correct: bool):
        self['correct_midi_vel'] = correct


