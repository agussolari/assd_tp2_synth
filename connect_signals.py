import files_import as fi
import plots as pl

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
