import subprocess

import connect_signals as cs
import numpy as np
import files_import as fi

subprocess.run(["pyuic5", "-x", "qt_gui.ui", "-o", "py_gui.py"])

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from py_gui import Ui_MainWindow
from pyqtgraph import PlotWidget
from PyQt5.QtCore import pyqtSignal, QThread

# import pyqtgraph as pg

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

class track_data:
    track_1_filename = []
    track_1_mid = []
    track_1_samples = []
    track_1_effects = []

    track_2_filename = []
    track_2_mid = []
    track_2_samples = []
    track_2_effects = []

    track_3_filename = []
    track_3_mid = []
    track_3_samples = []
    track_3_effects = []

    track_4_filename = []
    track_4_mid = []
    track_4_samples = []
    track_4_effects = []

    

    
class MainWindow(QMainWindow, Ui_MainWindow):
    

    
    def __init__(self):
        
        super().__init__()        
        
        self.setupUi(self)
        
        self.setWindowTitle('ASSD - GUI - DAW')
        # self.setWindowIcon(QIcon('logo.jpg'))
        
        
        
        self.show()
        self.track_data = track_data()
        
        
        
        cs.connect_import_files(self)
        cs.connect_enable_buttons(self)
        cs.connect_proccess_notes(self)
        cs.connect_play_buttons(self)
        cs.connect_stop_buttons(self)
        cs.connect_plot_buttons(self)
        cs.connect_synth_data(self)
        cs.connect_effects_params(self)
        self.prev_r_dataset = 0
        self.input_file_data = []
        

    # def connect_signals(self):


def main():
    app = QApplication([])
    window = MainWindow()
    app.exec_()
    
if __name__ == '__main__':
    main()
    