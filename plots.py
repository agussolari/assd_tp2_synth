import numpy as np
from scipy import signal
import pyqtgraph as pg
import matplotlib.cm
import mido


import pyqtgraph as pg


def parse_data(data):
    types = []
    times = []
    notes = []
    velocities = []
    

    for message in data:
        # current_time += message.time  # Actualizamos el tiempo actual
        types.append(message.type)
        times.append(message.time)
        notes.append(message.note)
        velocities.append(message.velocity)

    return np.array (types), np.array(times), np.array(notes), np.array(velocities)

def calcular_espectrograma(t, y):
    # Calcular la frecuencia de muestreo
    fs = 1 / (t[1] - t[0])

    # Calcular el espectrograma
    f, t, sxx = signal.spectrogram(y, fs, nperseg=256, noverlap=128, nfft=1024, window='hann', scaling='spectrum')

    return t, f, sxx

def plot_spectrogram(mid_data ,self, i):
    node_plots = [self.track_1_spectrum, self.track_2_spectrum, self.track_3_spectrum]
    
    print("plot spectrogram: ", i)
    
    int_tiempos, int_velocities = procesar_midi_messages(mid_data)
    t, y = temporal(int_tiempos, int_velocities)
    
    tt, f, sxx = calcular_espectrograma(t, y)
    
    img = pg.ImageItem()
    sxx = sxx.T
    
    #color to sxx
    colormap = matplotlib.cm.get_cmap('viridis')  # Puedes cambiar 'viridis' a cualquier colormap que te guste
    amplitude_color = colormap(sxx)
    
    img.setImage(amplitude_color, xvals=tt/10, yvals=f)  # Divide el eje horizontal por 10
    
    #plot
    node_plots[i-1].clear()
    node_plots[i-1].addItem(img)
    node_plots[i-1].setLabel('left', 'Frequency', units='Hz')
    node_plots[i-1].setLabel('bottom', 'Time', units='s/10')

def midi_to_freq(midi_note):
    return 440.0 * np.power(2.0, (midi_note - 69) / 12.0)

def temporal(int_tiempos, int_velocities):
    t = np.linspace(0, 4, 5000)
    y = np.zeros_like(t)

    for note, times in int_tiempos.items():
        freq = midi_to_freq(note)
        for time in times:
            start, end = time
            mask = (t >= start) & (t < end)
            y[mask] += np.sin(2 * np.pi * freq * t[mask]) * int_velocities[note][0][1] / 128.0

    return t, y


def plot_temporal(mid_data, self, i):
    node_plots = [self.track_1_temporal, self.track_2_temporal, self.track_3_temporal]

    print("plot temporal: ", i)
    
    int_tiempos, int_velocities = procesar_midi_messages(mid_data)

    time, signal = temporal(int_tiempos, int_velocities)
    
    node_plots[i-1].clear()
    node_plots[i-1].plot(time, signal)
    node_plots[i-1].setLabel('left', 'Amplitude', units='')

    
    



def plot_scatter(mid_data, self, i):
    
    node_filenames = [self.track_data.track_1_filename, self.track_data.track_2_filename, self.track_data.track_3_filename]
    node_plots = [self.track_1_scatter, self.track_2_scatter, self.track_3_scatter]
   
    print("plot scatter: ", i)

    int_tiempos, int_velocities = procesar_midi_messages(mid_data)
    
    #plot scatter
    node_plots[i-1].clear()
    for note, intervals in int_tiempos.items():
        for interval in intervals:
            node_plots[i-1].plot(interval, [note, note], color='blue')
            
    node_plots[i-1].setLabel('left', 'Note', units='')
    node_plots[i-1].setLabel('bottom', 'Time', units='s')
    
    
            
from collections import defaultdict


def procesar_midi_messages(midi_messages):
    notas = defaultdict(list)
    velocities = defaultdict(list)
    current_notes = {}
    current_time = 0
    current_velocity = 0  # Initialize current_velocity

    for message in midi_messages:
        current_time += message.time
        if message.type == 'note_on':
            current_notes[message.note] = current_time
        elif message.type == 'note_off':
            note = message.note
            start_time = current_notes.pop(note, None)
            if start_time is not None:
                notas[note].append([start_time, current_time])
                velocities[note].append([current_velocity, message.velocity])
        elif message.type == 'control_change' and message.control == 7:
            current_velocity = message.value

    int_tiempos = {note: notas[note] for note in notas}
    int_velocities = {note: velocities[note] for note in velocities}

    return int_tiempos, int_velocities





