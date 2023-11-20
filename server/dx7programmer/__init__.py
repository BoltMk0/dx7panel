import shutil

# import wx
# import wx.lib.agw.knobctrl as kc
from .dx7controller import *

midi.init()

# _dx7_voice_bank_instance = None
# _dx7_model_instance = None
# _dx7_controller_instance = None
# _bank_manager_instance = None

# _dx7_param_update_en = True
# _dx7_active_param = None

# _received_bank = None

# BACKGROUND_COLOUR = wx.Colour(70, 72, 74)
# BACKGROUND_COLOUR_LGIHTER = wx.Colour(70, 72, 74)
# FOREGROUND_COLOR_BASE = wx.Colour(50, 150, 150)
# FOREGROUND_COLOR_HIGHLIGHT = wx.Colour(100, 200, 200)
# TEXT_COLOUR = wx.Colour(200, 200, 200)

# TEST_PALETTE = wx.Palette()
# TEST_PALETTE.Create([20, 50, 100, 200], [45, 150, 200, 200], [53, 150, 200, 200])


# def get_active_param() -> Union[VoiceParameterValue, None]:
#     return _dx7_active_param


# def get_voice_bank() -> DX7VoiceBank:
#     global _dx7_voice_bank_instance
#     if _dx7_voice_bank_instance is None:
#         _dx7_voice_bank_instance = DX7VoiceBank()
#     return _dx7_voice_bank_instance


# def get_model() -> DX7Voice:
#     global _dx7_model_instance
#     if _dx7_model_instance is None:
#         _dx7_model_instance = DX7Voice()
#     return _dx7_model_instance


# def get_controller() -> DX7Controller:
#     global _dx7_controller_instance
#     if _dx7_controller_instance is None:
#         _dx7_controller_instance = DX7Controller()
#     return _dx7_controller_instance


# class BankManager(Dict[str, DX7VoiceBank]):
#     BANK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'banks')
#     USER_DIRNAME = 'user'
#     PRESET_DIRNAME = 'preset'

#     @staticmethod
#     def preset_dirpath():
#         return os.path.join(BankManager.BANK_DIR, BankManager.PRESET_DIRNAME)

#     @staticmethod
#     def user_dirpath():
#         return os.path.join(BankManager.BANK_DIR, BankManager.USER_DIRNAME)

#     def __init__(self):
#         super(BankManager, self).__init__()
#         if not os.path.exists(self.preset_dirpath()):
#             os.makedirs(self.preset_dirpath())
#         if not os.path.exists(self.user_dirpath()):
#             os.makedirs(self.user_dirpath())
#         self._filepath_map = {}

#         self.on_new_bank = Signal()
#         self.on_bank_deleted = Signal()
#         self._preset_banks = []

#         self.refresh()

#     def refresh(self):
#         self._filepath_map.clear()
#         self.clear()

#         file_list = {self.USER_DIRNAME: [], self.PRESET_DIRNAME: []}
#         for i in os.listdir(self.BANK_DIR):
#             ipath = os.path.join(self.BANK_DIR, i)
#             if os.path.isdir(ipath):
#                 file_list[i] = []
#                 for f in os.listdir(ipath):
#                     fpath = os.path.join(ipath, f)
#                     if DX7VoiceBank.is_dx7_bank_sysex(fpath):
#                         file_list[i].append((os.path.basename(fpath), fpath, i))

#         for k in file_list:
#             file_list[k].sort(key=lambda x: x[0])

#         for key in file_list:
#             if key == self.PRESET_DIRNAME:
#                 continue
#             for idata in file_list[key]:
#                 bank = self.load_from_file(idata[1])

#         for idata in file_list[self.PRESET_DIRNAME]:
#             bank = self.load_from_file(idata[1])

#     def append(self, __object: DX7VoiceBank, group_name: str) -> None:
#         if __object.get_source_filepath() is None:
#             raise ValueError('Bank must come from a file')
#         if group_name not in self:
#             self[group_name] = []
#         if __object in self[group_name]:
#             raise ValueError('Duplicate')
#         self[group_name].append(__object)
#         self.on_new_bank(__object, group_name)

#     def load_from_file(self, filepath):
#         if not os.path.dirname(filepath).startswith(self.BANK_DIR):
#             original_filepath = filepath
#             filepath = os.path.join(self.user_dirpath(), os.path.basename(filepath))
#             shutil.copy(original_filepath, filepath)
#         b = DX7VoiceBank.from_file(filepath)
#         self.append(b, os.path.basename(os.path.dirname(filepath)))
#         return b

#     def new_bank(self, bankname: str):
#         b = DX7VoiceBank()
#         bpath = os.path.join(self.user_dirpath(), f'{bankname.replace(" ", "_")}.syx')
#         if os.path.exists(bpath):
#             raise FileExistsError(bpath)
#         b.save(bpath)
#         self.load_from_file(bpath)

#     def clear(self) -> None:
#         c = self.copy()
#         super(BankManager, self).clear()
#         for k in c:
#             for b in c[k]:
#                 self.on_bank_deleted(b)

#     def remove(self, bank: DX7VoiceBank) -> None:
#         for k in self:
#             if bank in self[k]:
#                 self[k].remove(bank)
#                 self.on_bank_deleted(bank, k)

#     @staticmethod
#     def get_instance():
#         global _bank_manager_instance
#         if _bank_manager_instance is None:
#             _bank_manager_instance = BankManager()
#         return _bank_manager_instance

#     @staticmethod
#     def bank_name(b: DX7VoiceBank):
#         return os.path.basename(b.get_source_filepath()[:-4]) if b.get_source_filepath() is not None else None

#     def from_bank_name(self, name: str):
#         for b in self:
#             if self.bank_name(b) == name:
#                 return b
#         raise KeyError(name)

#     @staticmethod
#     def bank_name_to_filepath(bank_name: str):
#         return os.path.join(BankManager.BANK_DIR, f'{bank_name}.syx')

#     def is_a_preset_bank(self, bank: DX7VoiceBank):
#         return bank in self[self.PRESET_DIRNAME]


# class _DX7GUIPanelBase(wx.BoxSizer):
#     _arm = True


# class _MainWindowBase(wx.Frame):
#     pass


# class RadioMenu(wx.Menu):
#     def __init__(self, title: str, options=None, init_val=None):
#         super(RadioMenu, self).__init__()
#         self._title_base = title
#         if options is not None:
#             self.set_options(options)
#             if init_val is not None:
#                 self.select(init_val)

#         self.Bind(wx.EVT_MENU, self._on_selected)
#         self.on_selected_cb = None

#     def get_label(self):
#         return f'{self._title_base}: {self.get_selection()}'

#     def set_options(self, opts):
#         for item in self.GetMenuItems():
#             self.Remove(item)
#         for o in opts:
#             o_ele = self.AppendRadioItem(wx.ID_ANY, str(o))

#     def _on_selected(self, e: wx.CommandEvent):
#         for opt in self.GetMenuItems():
#             if opt.Id == e.Id:
#                 if self.on_selected_cb is not None:
#                     self.on_selected_cb(opt.ItemLabelText)

#     def get_selection(self):
#         for opt in self.GetMenuItems():
#             if opt.IsChecked():
#                 return opt.ItemLabelText

#     def clear_selection(self):
#         for opt in self.GetMenuItems():
#             if opt.IsChecked():
#                 opt.Check(False)
#                 return

#     def select(self, sel):
#         for opt in self.GetMenuItems():
#             if opt.ItemLabelText == sel:
#                 self.clear_selection()
#                 opt.Check()
#                 return
#         raise KeyError(sel)


# class MidiMenu(wx.Menu):
#     def __init__(self):
#         super(MidiMenu, self).__init__()
#         self._midiinmenu = RadioMenu('MIDI Device In', get_controller().get_inports(), get_controller()._config.dx7_device_in)
#         self._midioutmenu = RadioMenu('MIDI Device Out', get_controller().get_outports(), get_controller()._config.dx7_device_out)
#         self._midichanmenu = RadioMenu('MIDI Channel', [str(i+1) for i in range(16)], str(get_controller().get_channel()))

#         self._midiinmenu.on_selected_cb = self._on_midi_change
#         self._midioutmenu.on_selected_cb = self._on_midi_change
#         self._midichanmenu.on_selected_cb = self._on_midi_change

#         self.AppendSubMenu(self._midiinmenu, self._midiinmenu.get_label())
#         self.AppendSubMenu(self._midioutmenu, self._midioutmenu.get_label())
#         self.AppendSubMenu(self._midichanmenu, self._midichanmenu.get_label())

#         self.on_midi_settings_change_cb = None

#     def _on_midi_change(self, *args):
#         for c in self.GetMenuItems():
#             self.SetLabel(c.GetId(), c.SubMenu.get_label())
#         get_controller().set_midi_settings(self._midiinmenu.get_selection(), self._midioutmenu.get_selection(), int(self._midichanmenu.get_selection()))


# class FileMenu(wx.Menu):
#     def __init__(self, main_window: _MainWindowBase):
#         super(FileMenu, self).__init__()

#         load_item = wx.MenuItem(self, wx.ID_ANY, 'Load Patch...')
#         saveasbtn = wx.MenuItem(self, wx.ID_ANY, 'Save Patch As...')
#         upload_item = wx.MenuItem(self, wx.ID_ANY, 'Upload Bank...')

#         self.Append(load_item)
#         self.Bind(wx.EVT_MENU, self._on_load_patch, load_item)
#         self.Append(saveasbtn)
#         self.Bind(wx.EVT_MENU, self._on_saveas, saveasbtn)
#         self.Append(upload_item)
#         self.Bind(wx.EVT_MENU, self._on_upload, upload_item)

#         self._active_filepath = None
#         self._main_window = main_window

#     # def _on_save(self, ev):
#     #     try:
#     #         get_voice_bank().save(self._active_filepath)
#     #     except IOError:
#     #         wx.LogError(f'Cannot save to {self._active_filepath}')
#     #
#     def _on_load_patch(self, ev):
#         with wx.FileDialog(self._main_window, "Load Patch", wildcard="SYX files (*.syx)|*.syx",
#                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

#             if fileDialog.ShowModal() == wx.ID_CANCEL:
#                 return  # the user changed their mind

#             # Proceed loading the file chosen by the user
#             pathname = fileDialog.GetPath()
#             try:
#                 with open(pathname, 'rb') as fp:
#                     get_controller().update_voice(DX7Voice.from_sysex(fp.read()))
#             except Exception as e:
#                 dlg = wx.MessageDialog(self.GetParent(), f'ERROR: Unable to load patch\n{str(e)}')
#                 dlg.ShowModal()
#                 dlg.Destroy()

#     def _on_saveas(self, ev):
#         default_name = get_model().name.value.strip().replace(' ', '_')
#         with wx.FileDialog(self._main_window, "Save Patch As...", wildcard="SYX files (*.syx)|*.syx", defaultFile=default_name,
#                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

#             if fileDialog.ShowModal() == wx.ID_CANCEL:
#                 return  # the user changed their mind

#             # Proceed loading the file chosen by the user
#             pathname = fileDialog.GetPath()
#             try:
#                 get_model().save(pathname)
#             except IOError:
#                 wx.LogError(f'Cannot save to {pathname}')

#     def _on_upload(self, ev):
#         with wx.FileDialog(self._main_window, "Upload to DX7", wildcard="SYX files (*.syx)|*.syx",
#                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

#             if fileDialog.ShowModal() == wx.ID_CANCEL:
#                 return  # the user changed their mind

#             # Proceed loading the file chosen by the user
#             pathname = fileDialog.GetPath()
#             try:
#                 get_controller().update_bank(DX7VoiceBank.from_file(pathname))
#             except Exception as e:
#                 er_msg = 'ERROR: Unable to load voice bank'
#                 if DX7Voice.is_dx7_voice_sysex(pathname):
#                     er_msg += '\nFile is for a single voice. Use File->Load Patch instead'
#                 else:
#                     er_msg += f'\n{str(e)}'
#                 dlg = wx.MessageDialog(self.GetParent(), er_msg)
#                 dlg.ShowModal()
#                 dlg.Destroy()


# class EnvelopeEditPanel(_DX7GUIPanelBase):
#     class RatesContainer(_DX7GUIPanelBase):
#         def __init__(self, parent, rates: List[VoiceParameterValue]):
#             super(EnvelopeEditPanel.RatesContainer, self).__init__(wx.HORIZONTAL)
#             for i in range(len(rates)):
#                 self.Add(DX7ParamKnob(parent, rates[i], str(i+1)), 0)

#     class LevelsContainer(_DX7GUIPanelBase):
#         def __init__(self, parent, rates: List[VoiceParameterValue]):
#             super(EnvelopeEditPanel.LevelsContainer, self).__init__(wx.HORIZONTAL)
#             for i in range(len(rates)):
#                 self.Add(DX7ParamSlider(parent, rates[i], str(i+1)))

#     def __init__(self, parent, env: Envelope):
#         super(EnvelopeEditPanel, self).__init__(wx.VERTICAL)

#         rate_panel = self.RatesContainer(parent, [p[0] for p in env.points()])
#         level_panel = self.LevelsContainer(parent, [p[1] for p in env.points()])
#         text_1 = wx.StaticText(parent, label='Rate')
#         text_1.SetForegroundColour(TEXT_COLOUR)
#         self.Add(text_1, 0, wx.ALIGN_CENTER_HORIZONTAL)
#         self.Add(rate_panel, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 5)
#         text2 = wx.StaticText(parent, label='Level')
#         text2.SetForegroundColour(TEXT_COLOUR)
#         self.Add(text2, 0, wx.ALIGN_CENTER_HORIZONTAL)
#         self.Add(level_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)


# class DX7ParamKnob(_DX7GUIPanelBase):
#     def __init__(self, parent, param: VoiceParameterValue, label: Union[str, None]=None, size=(30, 30)):
#         super(DX7ParamKnob, self).__init__(wx.VERTICAL)
#         self.param = param
#         self.knob = kc.KnobCtrl(parent, size=size)
#         self.knob.SetAngularRange(-45, 225)
#         self.knob.SetValue(param.value)
#         self.knob.SetTags((param.min, param.max))
#         self.knob.SetTagsColour(wx.Colour(255, 255, 255, wx.ALPHA_TRANSPARENT))
#         self.knob.SetBackgroundColour(BACKGROUND_COLOUR)
#         self.knob.SetForegroundColour(FOREGROUND_COLOR_BASE)

#         param.on_change.connect(self._on_param_change)
#         self.knob.Bind(kc.EVT_KC_ANGLE_CHANGED, self._on_knob_change, self.knob)

#         if label is not None:
#             text = wx.StaticText(parent, label=label)
#             text.SetForegroundColour(TEXT_COLOUR)
#             self.Add(text, 0, wx.ALIGN_CENTER_HORIZONTAL)
#         self.Add(self.knob, 0, wx.ALIGN_CENTER_HORIZONTAL)

#     def _on_param_change(self, param: VoiceParameterValue):
#         if self._arm:
#             self._arm = False
#             self.knob.SetValue(param.value)
#             self._arm = True

#     def _on_knob_change(self, ev):
#         if self._arm:
#             self._arm = False
#             self.param.value = int(self.knob.GetValue())
#             self._arm = True


# class DX7ParamSlider(_DX7GUIPanelBase):
#     def __init__(self, parent, param: VoiceParameterValue, label: Union[str, None]=None, vertical: bool=True):
#         super(DX7ParamSlider, self).__init__(wx.VERTICAL)
#         self.param = param
#         self._vert = vertical
#         self.slider = wx.Slider(parent, value=param.value, minValue=param.min, maxValue=param.max,
#                            style=wx.SL_VERTICAL if vertical else wx.SL_HORIZONTAL)

#         self.slider.Bind(wx.EVT_SLIDER, self._on_slider_change, self.slider)
#         param.on_change.connect(self._on_param_change)

#         if label is not None:
#             label = wx.StaticText(parent, label=label)
#             label.SetForegroundColour(TEXT_COLOUR)
#             self.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL)

#         self.Add(self.slider, 0, wx.EXPAND)

#     def _on_param_change(self, param: VoiceParameterValue):
#         if self._arm:
#             self._arm = False
#             self.slider.SetValue(param.max - param.value if self._vert else param.value)
#             self._arm = True

#     def _on_slider_change(self, ev):
#         if self._arm:
#             self._arm = False
#             self.param.value = self.param.max - self.slider.GetValue() if self._vert else self.slider.GetValue()
#             self._arm = True


# class DX7ParamCombobox(_DX7GUIPanelBase):
#     def __init__(self, parent, param: VoiceParameterValue, label: str, choices: List[str] = None):
#         super(DX7ParamCombobox, self).__init__(wx.HORIZONTAL)
#         if choices is None:
#             choices = [str(i) for i in range(param.max + 1)]
#         self.choices = choices
#         self.param = param
#         param.on_change.connect(self._on_val_change)
#         self.combobox = wx.ComboBox(parent, value=choices[param.value], choices=[str(c) for c in choices])

#         self.combobox.Bind(wx.EVT_TEXT, self._on_cbox_select, self.combobox)

#         # self.combobox.SetBackgroundColour(FOREGROUND_COLOR_BASE)
#         # self.combobox.SetForegroundColour(TEXT_COLOUR)

#         self.label = wx.StaticText(parent, label=label)
#         self.label.SetForegroundColour(TEXT_COLOUR)
#         self.label.SetForegroundColour(TEXT_COLOUR)
#         self.Add(self.label, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
#         self.Add(self.combobox, 0, wx.EXPAND)

#     def _on_val_change(self, param):
#         if self._arm:
#             self._arm = False
#             self.combobox.SetValue(self.choices[param.value])
#             self._arm = True

#     def _on_cbox_select(self, ev):
#         if self._arm:
#             self._arm = False
#             self.param.value = self.combobox.GetSelection()
#             self._arm = True

#     def switch_out_param(self, new_param: VoiceParameterValue, choices=None, init_choice=None, new_label=None):
#         if choices is None:
#             choices = [str(i) for i in range(new_param.max)]
#         if init_choice is None:
#             init_choice = choices[0]

#         self.combobox.Clear()
#         for choice in choices:
#             self.combobox.Append(str(choice))

#         self.param.on_change.clear()
#         del self.param
#         self.param = new_param

#         self.combobox.SetValue(str(init_choice))

#         self.param.on_change.connect(self._on_val_change)

#         if new_label is not None:
#             self.label.SetLabelText(new_label)


# class DX7ParamCheckbox(_DX7GUIPanelBase):
#     def __init__(self, parent, param: VoiceParameterValue, label: str):
#         super(DX7ParamCheckbox, self).__init__(wx.HORIZONTAL)

#         self.param = param
#         param.on_change.connect(self._on_val_change)

#         self.checkbox = wx.CheckBox(parent)
#         self.checkbox.SetValue(param.value)
#         self.checkbox.Bind(wx.EVT_CHECKBOX, self._on_cbox_select, self.checkbox)
#         self.checkbox.SetForegroundColour(TEXT_COLOUR)
#         label = wx.StaticText(parent, label=label)
#         label.SetForegroundColour(TEXT_COLOUR)
#         self.Add(label, 0, wx.LEFT | wx.RIGHT, 5)
#         self.Add(self.checkbox)

#     def _on_val_change(self, param):
#         if self._arm:
#             self._arm = False
#             self.checkbox.SetValue(param.value)
#             self._arm = True

#     def _on_cbox_select(self, ev):
#         if self._arm:
#             self._arm = False
#             self.param.value = int(self.checkbox.IsChecked())
#             self._arm = True


# class DX7AlgorithmViewCombobox(_DX7GUIPanelBase):
#     def __init__(self, parent):
#         super(DX7AlgorithmViewCombobox, self).__init__(wx.VERTICAL)

#         self.param = get_model().algorithm_sel
#         self.param.on_change.connect(self._on_val_change)

#         self.bitmap = wx.StaticBitmap(parent, bitmap=wx.Bitmap(self.alg_no_to_png_filepath(1)), size=(155, 155))
#         self.combocontainer = DX7ParamCombobox(parent, self.param, 'Algorithm', choices=[str(i + 1) for i in range(32)])
#         self.Add(self.combocontainer, 0, wx.ALIGN_RIGHT)
#         self.Add(self.bitmap)
#         self.Add(DX7ParamCombobox(parent, get_model().feedback, 'Feedback'), 0, wx.ALIGN_RIGHT | wx.TOP, 3)

#     @staticmethod
#     def alg_no_to_png_filepath(algno: int):
#         return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res', 'algorithms', f'alg{algno}.png')

#     def _on_val_change(self, param):
#         self.bitmap.SetBitmap(wx.Bitmap(self.alg_no_to_png_filepath(self.param.value + 1)))


# class OPEditorPanel(_DX7GUIPanelBase):
#     class EnableNLevelPanel(_DX7GUIPanelBase):
#         class EnCheckbox(_DX7GUIPanelBase):
#             def __init__(self, parent, op_number: int):
#                 super(OPEditorPanel.EnableNLevelPanel.EnCheckbox, self).__init__(wx.VERTICAL)
#                 self._op_number = op_number
#                 self.checkbox = wx.CheckBox(parent)
#                 self.checkbox.Bind(wx.EVT_CHECKBOX, self._on_check, self.checkbox)

#                 get_model().op_enable.on_change.connect(self._on_op_en_change)
#                 text = wx.StaticText(parent, wx.ID_ANY, 'En')
#                 text.SetForegroundColour(TEXT_COLOUR)
#                 self.Add(text, 0, wx.ALL | wx.EXPAND)
#                 self.Add(self.checkbox, 0, wx.ALL | wx.EXPAND)

#             def _on_op_en_change(self, param):
#                 if self._arm:
#                     self._arm = False
#                     self.checkbox.SetValue(get_model().op_enable.osc_enabled(self._op_number))
#                     self._arm = True

#             def _on_check(self, ev):
#                 if self._arm:
#                     self._arm = False
#                     get_model().op_enable.set_osc_enable(self._op_number, self.checkbox.IsChecked())
#                     self._arm = True

#         def __init__(self, parent, operator: Operator):
#             super(OPEditorPanel.EnableNLevelPanel, self).__init__(wx.HORIZONTAL)
#             self._operator = operator
#             self.en_checkbox = self.EnCheckbox(parent, get_model().op_bank.index(operator))
#             self.output_level_slider = DX7ParamSlider(parent, operator.output_level, 'Output Level', False)

#             self.Add(self.en_checkbox)
#             self.Add(self.output_level_slider)

#     def __init__(self, parent, op_model:Operator):
#         super(OPEditorPanel, self).__init__(wx.VERTICAL)
#         self._models = op_model
#         self.env_edit_panel = EnvelopeEditPanel(parent, op_model.envelope)
#         text_1 = wx.StaticText(parent, label=f'OP{op_model.op_number+1}')
#         text_1.SetForegroundColour(TEXT_COLOUR)
#         self.Add(text_1, 0, wx.ALIGN_LEFT | wx.LEFT | wx.TOP, 5)
#         self.Add(self.EnableNLevelPanel(parent, op_model), 0, wx.ALIGN_CENTER_HORIZONTAL)
#         self.Add(wx.StaticLine(parent, -1), 0, wx.ALL | wx.EXPAND, 5)
#         text_2 = wx.StaticText(parent, label='EG Envelope')
#         text_2.SetForegroundColour(TEXT_COLOUR)
#         self.Add(text_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 5)
#         self.Add(self.env_edit_panel, 0, wx.ALIGN_CENTER_HORIZONTAL)
#         self.Add(wx.StaticLine(parent, -1), 0, wx.ALL | wx.EXPAND, 5)
#         text_3 = wx.StaticText(parent, label='Kbd Level Scaling')
#         text_3.SetForegroundColour(TEXT_COLOUR)
#         self.Add(text_3, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 5)

#         breakpoint_choices = ['A -1', 'A#-1', 'B -1']
#         for octave in range(8):
#             for note in ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'):
#                 breakpoint_choices.append(f'{note:2}{octave}')
#         breakpoint_choices.append('C 8')

#         self.Add(DX7ParamCombobox(parent, op_model.keyboard_level_scale.break_point, 'Break Point', breakpoint_choices), 0, wx.BOTTOM | wx.ALIGN_RIGHT, 3)
#         self.Add(DX7ParamCombobox(parent, op_model.keyboard_level_scale.left_depth, 'Left Depth'), 0, wx.BOTTOM | wx.ALIGN_RIGHT, 3)
#         self.Add(DX7ParamCombobox(parent, op_model.keyboard_level_scale.right_depth, 'Right Depth'), 0, wx.BOTTOM | wx.ALIGN_RIGHT, 3)
#         self.Add(DX7ParamCombobox(parent, op_model.keyboard_level_scale.left_curve, 'Left Curve', ['-LIN', '-EXP', '+EXP', '+LIN']), 0, wx.BOTTOM | wx.ALIGN_RIGHT, 3)
#         self.Add(DX7ParamCombobox(parent, op_model.keyboard_level_scale.right_curve, 'Right Curve', ['-LIN', '-EXP', '+EXP', '+LIN']), 0, wx.BOTTOM | wx.ALIGN_RIGHT, 3)
#         self.Add(wx.StaticLine(parent, -1), 0, wx.ALL |wx.EXPAND, 5)
#         self.Add(DX7ParamCombobox(parent, op_model.keyboard_rate_scaling, 'Kbd Rate Scaling'), 0, wx.BOTTOM | wx.ALIGN_RIGHT, 3)
#         self.Add(DX7ParamCombobox(parent, op_model.mod_sens_amplitude, 'Mod Sens Amp'), 0, wx.BOTTOM | wx.ALIGN_RIGHT, 3)
#         self.Add(DX7ParamCombobox(parent, op_model.key_vel_sens, 'Vel Sensitivity'), 0, wx.BOTTOM | wx.ALIGN_RIGHT, 3)
#         self.Add(wx.StaticLine(parent, -1), 0, wx.ALL | wx.EXPAND, 5)
#         self.Add(DX7ParamCombobox(parent, op_model.freq_coarse, 'Freq Coarse', ['0.5'] + [str(i+1) for i in range(op_model.freq_coarse.max)]), 0, wx.BOTTOM | wx.ALIGN_RIGHT, 3)
#         self.Add(DX7ParamCombobox(parent, op_model.freq_fine, 'Freq Fine'), 0, wx.BOTTOM | wx.ALIGN_RIGHT, 3)
#         self.Add(DX7ParamCombobox(parent, op_model.detune, 'Detune', [str(i-7) for i in range(op_model.detune.max+1)]), 0, wx.BOTTOM | wx.ALIGN_RIGHT, 3)


# class HeaderBar(_DX7GUIPanelBase):
#     def __init__(self, parent):
#         super(HeaderBar, self).__init__(wx.HORIZONTAL)

#         # self.voice_sel_param = VoiceParameterValue(0, 31)
#         # self.voice_sel = DX7ParamCombobox(parent, self.voice_sel_param, 'Voice', choices=[str(i+1) for i in range(32)])
#         # self.voice_sel.combobox.Bind(wx.EVT_TEXT, self._on_voice_sel_change, self.voice_sel.combobox)
#         # self.Add(wx.StaticText(parent, label='Voice #'), 0, wx.RIGHT, 5)
#         # self.Add(self.voice_sel)

#         text = wx.StaticText(parent, label='Patch Name')
#         text.SetForegroundColour(TEXT_COLOUR)
#         self.Add(text, 0, wx.ALIGN_CENTRE_VERTICAL | wx.RIGHT | wx.LEFT, 5)
#         self.tc = wx.TextCtrl(parent, size=(200,25))
#         self.Add(self.tc, 0, wx.EXPAND)

#         self.voice_label_param_group = get_model().name
#         self.voice_label_param_group.on_change.connect(self._on_name_param_change)
#         self.tc.Bind(wx.EVT_TEXT, self._on_name_textbox_change, self.tc)

#     def _on_name_param_change(self, param):
#         if self._arm:
#             self._arm = False
#             self.tc.SetValue(param.value)
#             self._arm = True

#     def _on_name_textbox_change(self, ev):
#         if self._arm:
#             self._arm = False
#             self.voice_label_param_group.value = self.tc.GetValue()
#             self._arm = True


# class OPEditPanelGroup(_DX7GUIPanelBase):
#     def __init__(self, parent):
#         super(OPEditPanelGroup, self).__init__(wx.HORIZONTAL)
#         self.operator_editors = [OPEditorPanel(parent, op) for op in get_model().op_bank]
#         for oe in self.operator_editors:
#             self.Add(oe, 0, wx.RIGHT | wx.LEFT, 5)
#             if self.operator_editors.index(oe) != 5:
#                 self.Add(wx.StaticLine(parent, -1, style=wx.LI_VERTICAL), 0, wx.ALL | wx.EXPAND, 5)


# class LFOEditPanel(_DX7GUIPanelBase):
#     def __init__(self, parent):
#         super(LFOEditPanel, self).__init__(wx.VERTICAL)
#         lfo = get_model().lfo
#         text = wx.StaticText(parent, wx.ID_ANY, 'LFO')
#         text.SetForegroundColour(TEXT_COLOUR)
#         self.Add(text, 0, wx.ALIGN_CENTER_HORIZONTAL)
#         self.Add(DX7ParamCombobox(parent, lfo.wave, 'Waveform', ['Triangle', 'Saw Down', 'Saw Up', 'Square', 'Sine', 'S/Hold']), 0, wx.ALIGN_RIGHT)
#         self.Add(DX7ParamCombobox(parent, lfo.speed, 'Speed'), 0, wx.ALIGN_RIGHT)
#         self.Add(DX7ParamCombobox(parent, lfo.delay, 'Delay'), 0, wx.ALIGN_RIGHT)
#         self.Add(DX7ParamCombobox(parent, lfo.amd, 'Amp Modulation Depth'), 0, wx.ALIGN_RIGHT)
#         self.Add(DX7ParamCombobox(parent, lfo.pmd, 'Pitch Modulation Depth'), 0, wx.ALIGN_RIGHT)
#         self.Add(DX7ParamCheckbox(parent, lfo.sync, 'Synchronize'), 0, wx.ALIGN_RIGHT)


# class OtherVoiceParameterEditPanel(_DX7GUIPanelBase):
#     def __init__(self, parent):
#         super(OtherVoiceParameterEditPanel, self).__init__(wx.VERTICAL)

#         model = get_model()

#         self.Add(DX7AlgorithmViewCombobox(parent))
#         self.Add(wx.StaticLine(parent, -1), 0, wx.ALL | wx.EXPAND, 5)
#         text = wx.StaticText(parent, label='Pitch Envelope')
#         text.SetForegroundColour(TEXT_COLOUR)
#         self.Add(text, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 5)
#         self.Add(EnvelopeEditPanel(parent, model.pitch_env), 0, wx.ALIGN_CENTER_HORIZONTAL)
#         reset_btn = wx.Button(parent, label='Reset Levels')
#         reset_btn.Bind(wx.EVT_BUTTON, self._on_reset_levels, reset_btn)
#         self.Add(reset_btn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 3)
#         self.Add(wx.StaticLine(parent, -1), 0, wx.ALL | wx.EXPAND, 5)
#         self.Add(LFOEditPanel(parent))
#         self.Add(wx.StaticLine(parent, -1), 0, wx.ALL | wx.EXPAND, 5)
#         self.Add(DX7ParamCombobox(parent, model.mod_sens_pitch, 'Pitch Modulation Sens'), 0, wx.ALIGN_RIGHT)
#         self.Add(DX7ParamCombobox(parent, model.transpose, 'Transpose', [str(i-24) for i in range(model.transpose.max + 1)]), 0, wx.ALIGN_RIGHT)
#         self.Add(DX7ParamCheckbox(parent, model.osc_sync, 'Oscillator Sync'), 0, wx.ALIGN_RIGHT)

#     def _on_reset_levels(self, ev):
#         get_model().pitch_env.level1.value = 50
#         get_model().pitch_env.level2.value = 50
#         get_model().pitch_env.level3.value = 50
#         get_model().pitch_env.level4.value = 50


# class PatchNavigatorPanel(_DX7GUIPanelBase):
#     class _VoiceContextMenu(wx.Menu):
#         def __init__(self, parent, bank: DX7VoiceBank, voice: DX7Voice, tree: wx.TreeCtrl, leaf):
#             super(PatchNavigatorPanel._VoiceContextMenu, self).__init__()
#             self.voice = voice
#             self.bank = bank
#             self.leaf = leaf
#             self.tree = tree
#             self.parent = parent

#             save_into = wx.MenuItem(self, wx.ID_NEW, f'Save current settings into {BankManager.bank_name(bank)}[{bank.index(voice)}] ({voice.name.value})')
#             self.Bind(wx.EVT_MENU, self._on_save_into, save_into)
#             self.Append(save_into)

#         def _on_save_into(self, ev):
#             if BankManager.get_instance().is_a_preset_bank(self.bank):
#                 dlg = wx.MessageDialog(self.parent,
#                                        f'Modifying preset banks is not allowed.\nClone the bank before editing!',
#                                        f'Not allowed')
#                 dlg.ShowModal()
#                 dlg.Destroy()
#                 return
#             self.bank[self.bank.index(self.voice)].update(get_model().vals())
#             self.bank.save(self.bank.get_source_filepath())
#             self.tree.SetItemText(self.leaf, get_model().name.value)
#             print(f'[OK] Saved voice into {BankManager.bank_name(self.bank)}')

#     class _BankContextMenu(wx.Menu):
#         def __init__(self, parent, bank: DX7VoiceBank, tree: wx.TreeCtrl, branch):
#             super(PatchNavigatorPanel._BankContextMenu, self).__init__()
#             self.bank = bank
#             self.branch = branch
#             self.tree = tree
#             self.parent = parent

#             del_item = wx.MenuItem(self, wx.ID_ANY, f'Delete {BankManager.bank_name(self.bank)}')
#             self.Bind(wx.EVT_MENU, self._on_del, del_item)
#             upload_item = wx.MenuItem(self, wx.ID_ANY, f'Upload {BankManager.bank_name(self.bank)} to DX7...')
#             self.Bind(wx.EVT_MENU, self._on_upload, upload_item)
#             duplicate = wx.MenuItem(self, wx.ID_ANY, f'Clone {BankManager.bank_name(self.bank)}...')
#             self.Bind(wx.EVT_MENU, self._on_clone, duplicate)
#             rename_item = wx.MenuItem(self, wx.ID_ANY, f'Rename {BankManager.bank_name(self.bank)}...')
#             self.Bind(wx.EVT_MENU, self._on_rename, rename_item)

#             if BankManager.get_instance().is_a_preset_bank(bank):
#                 del_item.Enable(False)
#                 rename_item.Enable(False)

#             self.Append(upload_item)
#             self.Append(duplicate)
#             self.Append(rename_item)
#             self.AppendSeparator()
#             self.Append(del_item)

#         def _on_del(self, ev):
#             if BankManager.get_instance().is_a_preset_bank(self.bank):
#                 dlg = wx.MessageDialog(self.parent,
#                                        f'Modifying preset banks is not allowed.\nClone the bank before editing!',
#                                        f'Not allowed')
#                 dlg.ShowModal()
#                 dlg.Destroy()
#                 return

#             if wx.MessageDialog(
#                 self.parent, f'Delete {BankManager.bank_name(self.bank)}?', 'This action cannot be undone',
#                 wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
#             ).ShowModal() != wx.ID_YES:
#                 return

#             os.remove(self.bank.get_source_filepath())
#             BankManager.get_instance().remove(self.bank)

#         def _on_rename(self, ev):
#             if BankManager.get_instance().is_a_preset_bank(self.bank):
#                 dlg = wx.MessageDialog(self.parent,
#                                        f'Modifying preset banks is not allowed.\nClone the bank before editing!',
#                                        f'Not allowed')
#                 dlg.ShowModal()
#                 dlg.Destroy()
#                 return

#             with wx.TextEntryDialog(self.parent, 'Enter New Patch Name') as dialog:
#                 dialog.SetValue(BankManager.bank_name(self.bank))
#                 if dialog.ShowModal() == wx.ID_CANCEL:
#                     return  # the user changed their mind

#                 bank_filepath = os.path.join(os.path.dirname(self.bank.get_source_filepath()), f'{dialog.GetValue()}.syx')
#                 if os.path.exists(bank_filepath):
#                     dlg = wx.MessageDialog(self.parent, f'A bank with the name "{dialog.GetValue()}" already exists')
#                     dlg.ShowModal()
#                     dlg.Destroy()
#                     return

#                 shutil.move(self.bank.get_source_filepath(), bank_filepath)
#                 BankManager.get_instance().refresh()
#                 self.tree.Expand(self.tree.GetRootItem())

#         def _on_upload(self, ev):
#             if wx.MessageDialog(
#                 self.parent, f'Upload {BankManager.bank_name(self.bank)} to DX7?',
#                     'This will overwrite the current data ',
#                 wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
#             ).ShowModal() != wx.ID_YES:
#                 return
#             get_controller().update_bank(self.bank)

#         def _on_clone(self, ev):
#             with wx.TextEntryDialog(self.parent, 'Enter New Patch Name') as dialog:
#                 suggested_basename = f'{BankManager.bank_name(self.bank)}_clone'
#                 if os.path.exists(BankManager.bank_name_to_filepath(suggested_basename)):
#                     i = 1
#                     while os.path.exists(BankManager.bank_name_to_filepath(f'{suggested_basename}_{i:02}')):
#                         i += 1
#                     suggested_basename += f'_{i:02}'

#                 dialog.SetValue(suggested_basename)
#                 if dialog.ShowModal() == wx.ID_CANCEL:
#                     return  # the user changed their mind

#                 bank_filepath = os.path.join(BankManager.get_instance().user_dirpath(), f'{dialog.GetValue()}.syx')
#                 if os.path.exists(bank_filepath):
#                     dlg = wx.MessageDialog(self.parent, f'A bank with the name "{dialog.GetValue()}" already exists')
#                     dlg.ShowModal()
#                     dlg.Destroy()
#                     return

#                 shutil.copy(self.bank.get_source_filepath(), bank_filepath)
#                 BankManager.get_instance().load_from_file(bank_filepath)

#     class _ButtonBank(_DX7GUIPanelBase):
#         def __init__(self, parent, tree: wx.TreeCtrl, on_refresh_cb):
#             super(PatchNavigatorPanel._ButtonBank, self).__init__(wx.VERTICAL)
#             self.parent = parent
#             self.tree = tree
#             self._on_refresh = on_refresh_cb

#             new_bank_btn = wx.Button(parent, label='New Bank')
#             bank_import_btn = wx.Button(parent, label='Import Bank From File...')
#             bank_download_btn = wx.Button(parent, label='Download Bank From DX7...')
#             refresh_btn = wx.Button(parent, label='Refresh List')
#             expand_all_btn = wx.Button(parent, label='Expand All')

#             self.Add(new_bank_btn, 0, wx.EXPAND)
#             self.Add(bank_import_btn, 0, wx.EXPAND)
#             self.Add(bank_download_btn, 0, wx.EXPAND)
#             self.Add(refresh_btn, 0, wx.EXPAND)
#             self.Add(expand_all_btn, 0, wx.EXPAND)

#             bank_import_btn.Bind(wx.EVT_BUTTON, self._on_import, bank_import_btn)
#             new_bank_btn.Bind(wx.EVT_BUTTON, self._on_new_bank, new_bank_btn)
#             bank_download_btn.Bind(wx.EVT_BUTTON, self._on_download_bank, bank_download_btn)
#             refresh_btn.Bind(wx.EVT_BUTTON, self._on_refresh, refresh_btn)
#             expand_all_btn.Bind(wx.EVT_BUTTON, self._on_expand_all, expand_all_btn)

#         def _on_download_bank(self, ev):
#             global _received_bank
#             dialog = wx.ProgressDialog('Downloading Bank From DX7', 'Waiting for sysex from DX7...', 100, style=wx.PD_CAN_ABORT)

#             keep_going = True
#             _received_bank = None

#             def on_bank(bank: DX7VoiceBank):
#                 global _received_bank
#                 _received_bank = bank

#             get_controller().on_bank_data.connect(on_bank)

#             while keep_going and _received_bank is None:
#                 wx.Sleep(1)
#                 keep_going = dialog.Update(0 if _received_bank is None else 100)[0]

#             get_controller().on_bank_data.disconnect(on_bank)
#             dialog.Destroy()

#             if _received_bank is not None:
#                 with wx.TextEntryDialog(self.parent, 'Enter New Patch Name') as dialog:
#                     i = 1
#                     while os.path.exists(os.path.join(BankManager.BANK_DIR, f'DX7_Bak_{i:02}.syx')):
#                         i += 1
#                     dialog.SetValue(f'DX7_Bak_{i:02}')
#                     if dialog.ShowModal() == wx.ID_CANCEL:
#                         return  # the user changed their mind

#                     bank_filepath = os.path.join(BankManager.get_instance().user_dirpath(), f'{dialog.GetValue()}.syx')
#                     if os.path.exists(bank_filepath):
#                         dlg = wx.MessageDialog(self.parent,
#                                                f'A bank with the name "{dialog.GetValue()}" already exists')
#                         dlg.ShowModal()
#                         dlg.Destroy()
#                         return

#                     DX7VoiceBank.save(_received_bank, bank_filepath)
#                     BankManager.get_instance().load_from_file(bank_filepath)

#         def _on_expand_all(self, ev):
#             self.tree.ExpandAll()

#         def _on_new_bank(self, ev):
#             with wx.TextEntryDialog(self.parent, 'Enter New Patch Name') as dialog:
#                 i=1
#                 while os.path.exists(os.path.join(BankManager.BANK_DIR, f'Bank{i:02}.syx')):
#                     i += 1
#                 dialog.SetValue(f'Bank{i:02}')
#                 if dialog.ShowModal() == wx.ID_CANCEL:
#                     return  # the user changed their mind

#                 bank_filepath = os.path.join(BankManager.BANK_DIR, f'{dialog.GetValue()}.syx')
#                 if os.path.exists(bank_filepath):
#                     dlg = wx.MessageDialog(self.parent, f'A bank with the name "{dialog.GetValue()}" already exists')
#                     dlg.ShowModal()
#                     dlg.Destroy()
#                     return

#                 BankManager.get_instance().new_bank(dialog.GetValue())

#         def _on_import(self, ev):
#             with wx.FileDialog(self.parent, "Import bank", wildcard="SYX files (*.syx)|*.syx",
#                                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fileDialog:

#                 if fileDialog.ShowModal() == wx.ID_CANCEL:
#                     return  # the user changed their mind

#                 # Proceed loading the file chosen by the user
#                 for filepath in fileDialog.GetPaths():
#                     try:
#                         if not DX7VoiceBank.is_dx7_bank_sysex(filepath):
#                             raise ValueError('File is not a DX7 bank sysex')
#                         BankManager.get_instance().load_from_file(filepath)
#                     except Exception as e:
#                         er_msg = 'ERROR: Unable to load voice bank'
#                         if DX7Voice.is_dx7_voice_sysex(filepath):
#                             er_msg += '\nFile is for a single voice. Use File->Load Patch instead'
#                         else:
#                             er_msg += f'\n{str(e)}'
#                         dlg = wx.MessageDialog(self.parent, er_msg)
#                         dlg.ShowModal()
#                         dlg.Destroy()

#     def __init__(self, parent: _MainWindowBase):
#         super(PatchNavigatorPanel, self).__init__(wx.VERTICAL)
#         self._loaded = False
#         self.parent = parent
#         self.SetMinSize(200, 200)

#         self.bank_group_roots = {}
#         self._bank_to_branch = {}

#         self.treectl = wx.TreeCtrl(parent)
#         self.treectl.SetBackgroundColour(BACKGROUND_COLOUR_LGIHTER)
#         self.treectl.SetForegroundColour(TEXT_COLOUR)
#         self.root = self.treectl.AddRoot('Banks')

#         for groupname in BankManager.get_instance():
#             self._add_bank_group(BankManager.get_instance()[groupname], groupname)

#         BankManager.get_instance().on_new_bank.connect(self._add_bank)
#         BankManager.get_instance().on_bank_deleted.connect(self._on_remove_bank)

#         self._buttons = self._ButtonBank(parent, self.treectl, self._on_refresh)
#         text = wx.StaticText(parent, label='Patch Browser')
#         text.SetForegroundColour(TEXT_COLOUR)
#         self.Add(text, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.TOP, 5)
#         self.Add(self.treectl, 1, wx.EXPAND)
#         self.Add(self._buttons, 0, wx.EXPAND | wx.BOTTOM, 20)

#         self.treectl.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self._on_item_right_click)
#         self.treectl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self._on_item_click)

#         self.treectl.Expand(self.root)

#         self._loaded = True

#     def _on_refresh(self, ev):
#         self._loaded = False
#         BankManager.get_instance().refresh()
#         self._loaded = True

#     def _on_item_right_click(self, ev):
#         data = self.treectl.GetItemData(ev.GetItem())
#         if data is None:
#             return
#         if data['type'] == 'bank':
#             bank = data['bank']
#             self.parent.PopupMenu(self._BankContextMenu(self.parent, bank, self.treectl, ev.GetItem()), ev.GetPoint())
#         elif data['type'] == 'voice':
#             bank = data['bank']
#             voice = data['bank'][data['index']]
#             self.parent.PopupMenu(self._VoiceContextMenu(self.parent, bank, voice, self.treectl, ev.GetItem()), ev.GetPoint())

#     def _on_item_click(self, ev):
#         data = self.treectl.GetItemData(ev.GetItem())
#         if data is None:
#             return
#         if data['type'] == 'voice':
#             voice = data['bank'][data['index']]
#             global _dx7_param_update_en
#             _dx7_param_update_en = False
#             get_model().update(voice.vals())
#             _dx7_param_update_en = True
#             get_controller().update_voice(voice)
#         elif data['type'] in ('bank', 'group'):
#             item = ev.GetItem()
#             if self.treectl.IsExpanded(item):
#                 self.treectl.Collapse(item)
#             else:
#                 self.treectl.Expand(item)

#     def _on_bank_sel(self, ev):
#         pass

#     def _on_patch_sel(self, ev):
#         pass

#     def _add_bank_group(self, banks: List[DX7VoiceBank], groupname: str):
#         if groupname in self.bank_group_roots:
#             raise KeyError(f'Bank group {groupname} already exists')
#         self.bank_group_roots[groupname] = self.treectl.AppendItem(self.root, groupname)
#         self.treectl.SetItemData(self.bank_group_roots[groupname], {'type': 'group', 'group': groupname})
#         for bank in banks:
#             self._add_bank(bank, groupname)

#     def _add_bank(self, bank: DX7VoiceBank, bank_group: str):
#         if bank_group not in self.bank_group_roots:
#             self._add_bank_group([], bank_group)

#         if not self.treectl.IsExpanded(self.bank_group_roots[bank_group]) and (self._loaded or bank_group != BankManager.PRESET_DIRNAME):
#             self.treectl.Expand(self.bank_group_roots[bank_group])

#         if bank.get_source_filepath() in self._bank_to_branch:
#             raise KeyError('bank is already present')

#         bank_name = BankManager.get_instance().bank_name(bank)
#         if bank_name is None:
#             raise FileNotFoundError('Bank did not come from file?')

#         root = self.bank_group_roots[bank_group]
#         branch = self.treectl.AppendItem(root, bank_name)
#         self._bank_to_branch[bank.get_source_filepath()] = branch
#         self.treectl.SetItemData(branch, {'type': 'bank', 'bank': bank, 'group': bank_group})

#         for voice in bank:
#             leaf = self.treectl.AppendItem(branch, f'{bank.index(voice) + 1:>2}: {voice.name.value}')
#             self.treectl.SetItemData(leaf, {'type': 'voice', 'bank': bank, 'index': bank.index(voice)})

#         if self._loaded:
#             self.treectl.SelectItem(branch)

#     def _on_remove_bank(self, bank: DX7VoiceBank, *other):
#         self.treectl.Delete(self._bank_to_branch[bank.get_source_filepath()])
#         del self._bank_to_branch[bank.get_source_filepath()]


# class FooterBar(_DX7GUIPanelBase):
#     def __init__(self, parent):
#         super(FooterBar, self).__init__(wx.HORIZONTAL)
#         self._devices_in = ['None']
#         self._devices_out = ['None']

#         self.parent = parent

#         devices_in_param = VoiceParameterValue(max=1)
#         devices_out_param = VoiceParameterValue(max=1)
#         devices_passthrough_param = VoiceParameterValue(max=1)

#         self.devices_in_combo = DX7ParamCombobox(parent, devices_in_param, 'DX7 MIDI In', self._devices_in)
#         self.devices_out_combo = DX7ParamCombobox(parent, devices_out_param, 'DX7 MIDI Out', self._devices_out)
#         self.device_passthrough_combo = DX7ParamCombobox(parent, devices_passthrough_param, 'MIDI Passthrough (To DX7)', self._devices_in)

#         vel_correction_param = VoiceParameterValue(max=1)
#         vel_correction_param.value = int(get_controller().get_velocity_correction())
#         vel_correction_param.on_change.connect(self._on_velocity_correction_changed)
#         vel_correction_check = DX7ParamCheckbox(parent, vel_correction_param, 'Velocity Correction')

#         refresh_btn = wx.Button(parent, label='Refresh')
#         refresh_btn.Bind(wx.EVT_BUTTON, self.repopulate, refresh_btn)

#         self.Add(refresh_btn, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)
#         self.Add(self.devices_in_combo, 0, wx.RIGHT, 10)
#         self.Add(self.devices_out_combo, 0, wx.RIGHT, 10)

#         self.Add(wx.StaticLine(parent, -1, style=wx.LI_VERTICAL), 0, wx.ALL | wx.EXPAND, 5)
#         self.Add(self.device_passthrough_combo)
#         self.Add(vel_correction_check, 0, wx.ALIGN_CENTRE_VERTICAL)

#         self.repopulate()

#     def repopulate(self, *args):
#         self._devices_in = [None] + get_controller().get_inports()
#         self._devices_out = [None] + get_controller().get_outports()

#         pin = VoiceParameterValue(max=len(self._devices_in))
#         pout = VoiceParameterValue(max=len(self._devices_out))
#         ppass = VoiceParameterValue(max=len(self._devices_in))

#         self.devices_in_combo.switch_out_param(pin, self._devices_in, init_choice=get_controller().get_device_in())
#         self.devices_out_combo.switch_out_param(pout, self._devices_out, init_choice=get_controller().get_device_out())
#         self.device_passthrough_combo.switch_out_param(ppass, self._devices_in, init_choice=get_controller().get_passthrough_device_in())

#         pin.on_change.connect(self._on_device_in_changed)
#         pout.on_change.connect(self._on_device_out_changed)
#         ppass.on_change.connect(self._on_device_passthrough_changed)

#     def _on_device_in_changed(self, param):
#         get_controller().set_device_in(self._devices_in[param.value])

#     def _on_device_out_changed(self, param):
#         get_controller().set_device_out(self._devices_out[param.value])

#     def _on_device_passthrough_changed(self, param):
#         get_controller().set_passthrough_device_in(self._devices_in[param.value])

#     def _on_velocity_correction_changed(self, param: VoiceParameterValue):
#         get_controller().set_velocity_correction(bool(param.value))


# class MainWindow(_MainWindowBase):
#     def __init__(self, title='DX7 Programmer'):
#         # super().__init__(None, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX, title=title)
#         super(MainWindow, self).__init__(
#             None, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX, title=title, size=(1000, 700))

#         self._title_base = title
#         menubar = wx.MenuBar()
#         self._filemenu = FileMenu(self)
#         self._midimenu = MidiMenu()
#         menubar.Append(self._filemenu, 'File')
#         menubar.Append(self._midimenu, 'Midi')

#         self.SetMenuBar(menubar)

#         self.header_bar = HeaderBar(self)
#         self.op_edit_panel = OPEditPanelGroup(self)

#         left_vbox = wx.BoxSizer(wx.VERTICAL)
#         left_vbox.Add(self.header_bar, 0, wx.ALIGN_CENTRE_HORIZONTAL | wx.TOP, 10)
#         left_vbox.Add(self.op_edit_panel)
#         self.footer_bar = FooterBar(self)
#         left_vbox.Add(self.footer_bar, 0, wx.ALIGN_CENTRE_HORIZONTAL | wx.TOP | wx.BOTTOM, 10)

#         mid_hbox = wx.BoxSizer(wx.HORIZONTAL)

#         self.browser = PatchNavigatorPanel(self)
#         mid_hbox.Add(wx.StaticLine(self, -1, style=wx.LI_VERTICAL), 0, wx.ALL | wx.EXPAND, 5)
#         mid_hbox.Add(self.browser, 0, wx.BI_EXPAND)
#         mid_hbox.Add(wx.StaticLine(self, -1, style=wx.LI_VERTICAL), 0, wx.ALL | wx.EXPAND, 5)
#         mid_hbox.Add(left_vbox)
#         line = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
#         line.SetBackgroundColour(FOREGROUND_COLOR_BASE)
#         line.SetForegroundColour(FOREGROUND_COLOR_HIGHLIGHT)
#         mid_hbox.Add(line, 0, wx.ALL | wx.EXPAND, 5)
#         mid_hbox.Add(OtherVoiceParameterEditPanel(self), 0, wx.ALL | wx.ALIGN_CENTRE_VERTICAL, 5)

#         # layout_vbox.Add(self.op_edit_panel)
#         self.SetSizer(mid_hbox)
#         self.Fit()

#         self.SetBackgroundColour(BACKGROUND_COLOUR)
#         self.SetForegroundColour(TEXT_COLOUR)


# def main_gui(*args):
#     app = wx.App()

#     # Changes to the voice parameter will be forwarded to the DX7
#     def _param_change_cb(param: VoiceParameterValue):
#         global _dx7_param_update_en
#         if _dx7_param_update_en:
#             get_controller().update_param(param)

#     def _param_rcv_cb(param: VoiceParameterValue):
#         global _dx7_param_update_en, _dx7_active_param
#         _dx7_active_param = get_model().val_map()[param.param_id]
#         _dx7_param_update_en = False
#         get_model().value = param.value
#         _dx7_param_update_en = True

#     def _data_slider_cb(val):
#         global _dx7_param_update_en
#         if get_active_param() is not None:
#             _dx7_param_update_en = False
#             get_active_param().set_from_data_slider(val)
#             _dx7_param_update_en = True

#     def _data_nudge_cb(val):
#         if get_active_param() is not None:
#             get_active_param().value += val

#     def _error_cb(*args):
#         print(*args)

#     def _voice_data_cb(voice: DX7Voice):
#         global _dx7_param_update_en
#         _dx7_param_update_en = False
#         get_model().update(voice.vals())
#         _dx7_param_update_en = True

#     main_frame = MainWindow()
#     main_frame.Show()

#     for p in get_model().vals():
#         p.on_change.connect(_param_change_cb)

#     get_controller().on_voice_received.connect(_voice_data_cb)
#     get_controller().on_param_change.connect(_param_rcv_cb)
#     get_controller().on_error.connect(_error_cb)
#     get_controller().on_data_entry_nudge.connect(_data_nudge_cb)
#     get_controller().on_data_entry_slider_change.connect(_data_slider_cb)

#     app.MainLoop()

#     get_controller().close()


# if __name__ == '__main__':
#     main_gui()
