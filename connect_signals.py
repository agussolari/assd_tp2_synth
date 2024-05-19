import files_import as fi
import plots as pl
import effects

def connect_import_files(self):
    self.track_1_import.clicked.connect(lambda: fi.import_track_files(self,1))
    self.track_2_import.clicked.connect(lambda: fi.import_track_files(self,2))
    self.track_3_import.clicked.connect(lambda: fi.import_track_files(self,3))
    
    
def connect_proccess_notes(self):
    self.channel_1_box.valueChanged.connect(lambda: fi.notes_proccessing(self, 1))
    self.channel_2_box.valueChanged.connect(lambda: fi.notes_proccessing(self, 2))
    self.channel_3_box.valueChanged.connect(lambda: fi.notes_proccessing(self, 3))
    
def connect_synth_data(self):
    self.track_1_box.currentIndexChanged.connect(lambda: fi.thread_synth_data_1(self))
    self.track_2_box.currentIndexChanged.connect(lambda: fi.thread_synth_data_2(self))
    self.track_3_box.currentIndexChanged.connect(lambda: fi.thread_synth_data_3(self))
    
    self.track_1_import.clicked.connect(lambda: fi.thread_synth_data_1(self))
    self.track_2_import.clicked.connect(lambda: fi.thread_synth_data_2(self))
    self.track_3_import.clicked.connect(lambda: fi.thread_synth_data_3(self))
    
    
    

    
def connect_plot_buttons(self):
    self.track_1_import.clicked.connect(lambda: fi.plot_data(self,1))
    self.track_2_import.clicked.connect(lambda: fi.plot_data(self,2))
    self.track_3_import.clicked.connect(lambda: fi.plot_data(self,3))
    
    self.channel_1_box.valueChanged.connect(lambda: fi.plot_data(self, 1))
    self.channel_2_box.valueChanged.connect(lambda: fi.plot_data(self, 2))
    self.channel_3_box.valueChanged.connect(lambda: fi.plot_data(self, 3))
    
def connect_play_buttons(self):
    self.play_track_1.clicked.connect(lambda: fi.thread_play_samples(self, 1))
    self.play_track_2.clicked.connect(lambda: fi.thread_play_samples(self, 2))
    self.play_track_3.clicked.connect(lambda: fi.thread_play_samples(self, 3))
    self.play_button.clicked.connect(lambda: fi.thread_play_samples(self, 4))
    # self.play_button.clicked.connect(lambda: pl.plot_spectrogram_from_samples(self))
    
def connect_stop_buttons(self):
    self.stop_track_1.clicked.connect(lambda: fi.stop_playback())
    self.stop_track_2.clicked.connect(lambda: fi.stop_playback())
    self.stop_track_3.clicked.connect(lambda: fi.stop_playback())
    self.stop_button.clicked.connect(lambda: fi.stop_playback())

def enable_buttons(self):
    if self.track_1_enable.isChecked():
        self.track_1_import.setEnabled(True)
    elif not self.track_1_enable.isChecked():
        self.track_1_import.setEnabled(False)
        
    if self.track_2_enable.isChecked():
        self.track_2_import.setEnabled(True)
    elif not self.track_2_enable.isChecked():
        self.track_2_import.setEnabled(False)
        
    if self.track_3_enable.isChecked():
        self.track_3_import.setEnabled(True)
    elif not self.track_3_enable.isChecked():
        self.track_3_import.setEnabled(False)
        


def connect_enable_buttons(self):
    self.track_1_enable.clicked.connect(lambda: enable_buttons(self))
    self.track_2_enable.clicked.connect(lambda: enable_buttons(self))
    self.track_3_enable.clicked.connect(lambda: enable_buttons(self))



######## Effects Control ########

def connect_effects_params(self):
    self.tabEffects.currentChanged.connect(lambda: effects.update(self))
    self.pushButton_select_file.clicked.connect(lambda: effects.importWAVFile(self))
    self.pushButton_apply_effects.clicked.connect(lambda: effects.apply(self))
    self.pushButton_reset.clicked.connect(lambda: effects.reset(self))

    # Reverberation

    self.dial_r_room_size.valueChanged.connect(lambda: effects.update(self))
    self.dial_r_dry_wet.valueChanged.connect(lambda: effects.update(self))
    self.dial_r_damping.valueChanged.connect(lambda: effects.update(self))
    self.dial_r_width.valueChanged.connect(lambda: effects.update(self))
    self.dial_r_pre_delay.valueChanged.connect(lambda: effects.update(self))
    self.dial_r_idg.valueChanged.connect(lambda: effects.update(self))
    self.dial_r_reverberance.valueChanged.connect(lambda: effects.update(self))
    self.dial_r_wet_gain.valueChanged.connect(lambda: effects.update(self))
    self.dial_r_echoes.valueChanged.connect(lambda: effects.update(self))
    self.dial_r_delay.valueChanged.connect(lambda: effects.update(self))

    self.comboBox_r_type.currentIndexChanged.connect(lambda: effects.update(self))
    self.comboBox_r_dataset.currentIndexChanged.connect(lambda: effects.update(self))
    self.comboBox_r_preset.currentIndexChanged.connect(lambda: effects.update(self))

    self.checkBox_r_stereo.clicked.connect(lambda: effects.update(self))
    # self.checkBox_r_convolution.clicked.connect(lambda: effects.update(self))

    # Delay Line

    self.dial_dl_feedback.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_dry_gain.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_lfo_freq.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_lfo_width.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_lfo_delay.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_lfo_depth.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_lfo_freq_2.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_lfo_width_2.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_lfo_delay_2.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_lfo_depth_2.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_lfo_freq_3.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_lfo_width_3.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_lfo_delay_3.valueChanged.connect(lambda: effects.update(self))
    self.dial_dl_lfo_depth_3.valueChanged.connect(lambda: effects.update(self))
    self.horizontalSlider_dl_voices.valueChanged.connect(lambda: effects.update(self))

    self.comboBox_dl_lfo_type.currentIndexChanged.connect(lambda: effects.update(self))
    self.comboBox_dl_interpolation.currentIndexChanged.connect(lambda: effects.update(self))
    self.comboBox_dl_lfo_type_2.currentIndexChanged.connect(lambda: effects.update(self))
    self.comboBox_dl_interpolation_2.currentIndexChanged.connect(lambda: effects.update(self))
    self.comboBox_dl_lfo_type_3.currentIndexChanged.connect(lambda: effects.update(self))
    self.comboBox_dl_interpolation_3.currentIndexChanged.connect(lambda: effects.update(self))
    self.comboBox_dl_type.currentIndexChanged.connect(lambda: effects.update(self))

    # self.checkBox_dl_convolution.clicked.connect(lambda: effects.update(self))

    # Filtering

    # self.spinBox_f_nfilters.valueChanged.connect(lambda: effects.update(self))
    # self.dial_f_center_freq.valueChanged.connect(lambda: effects.update(self))
    # self.dial_f_Q.valueChanged.connect(lambda: effects.update(self))
    # self.dial_f_gain.valueChanged.connect(lambda: effects.update(self))
    # self.dial_f_dry_wet.valueChanged.connect(lambda: effects.update(self))
    # self.dial_f_feedback.valueChanged.connect(lambda: effects.update(self))
    # self.dial_f_lfo_freq.valueChanged.connect(lambda: effects.update(self))
    # self.dial_f_lfo_width.valueChanged.connect(lambda: effects.update(self))
    # self.dial_f_lfo_delay.valueChanged.connect(lambda: effects.update(self))

    # self.comboBox_am_lfo_type.currentIndexChanged.connect(lambda: effects.update(self))
    # self.comboBox_am_lfo_interpolation.currentIndexChanged.connect(lambda: effects.update(self))
    # self.comboBox_f_type.currentIndexChanged.connect(lambda: effects.update(self))

    # Amplitude Modulation

    # self.dial_am_lfo_freq.valueChanged.connect(lambda: effects.update(self))
    # self.dial_am_lfo_width.valueChanged.connect(lambda: effects.update(self))
    # self.dial_am_lfo_delay.valueChanged.connect(lambda: effects.update(self))

    # self.comboBox_am_lfo_type.currentIndexChanged.connect(lambda: effects.update(self))
    # self.comboBox_am_lfo_interpolation.currentIndexChanged.connect(lambda: effects.update(self))

#################################