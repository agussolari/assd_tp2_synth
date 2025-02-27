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

def calcular_espectrograma(tt, y):

    # Calcular el espectrograma
    f, t, sxx = signal.spectrogram(y)

    return t, f, sxx

def plot_spectrogram_from_samples(self, samples):
    
    
    f, t, Sxx = signal.spectrogram(samples)
    img = pg.ImageItem()
    Sxx = Sxx.T
    
    # Color to Sxx
    colormap = matplotlib.cm.get_cmap('viridis')  # Puedes cambiar 'viridis' a cualquier colormap que te guste
    amplitude_color = colormap(Sxx)
    img.setImage(amplitude_color, xvals=t, yvals=f)
    
    # Plot
    self.track_spectrum.clear()
    self.track_spectrum.addItem(img)
    self.track_spectrum.setLabel('left', 'Frequency', units='Hz')
    self.track_spectrum.setLabel('bottom', 'Time', units='s')
    

    


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
    
    img.setImage(amplitude_color, xvals=t, yvals=f)  # Divide el eje horizontal por 10
    
    #plot
    node_plots[i-1].clear()
    node_plots[i-1].addItem(img)
    node_plots[i-1].setLabel('left', 'Frequency', units='Hz')
    node_plots[i-1].setLabel('bottom', 'Time', units='s')

def midi_to_freq(midi_note):
    return 440.0 * np.power(2.0, (midi_note - 69) / 12.0)

def temporal(int_tiempos, int_velocities):
    t = np.linspace(0, get_song_duration(int_tiempos), 44100)
    y = np.zeros_like(t)

    for note, times in int_tiempos.items():
        freq = midi_to_freq(note)
        for time in times:
            start, end = time
            mask = (t >= start) & (t < end)
            y[mask] += np.sin(2 * np.pi * freq * t[mask]) * int_velocities[note][0] / 128.0

    return t, y

def get_song_duration(song_data):
    max_time = 0
    for note_intervals in song_data.values():
        for interval in note_intervals:
            max_time = max(max_time, interval[1])
    return max_time

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
    
    # print(int_tiempos, int_velocities)
    #plot scatter
    node_plots[i-1].clear()
    for note, intervals in int_tiempos.items():
        for interval in intervals:
            node_plots[i-1].plot(interval, [note, note], color='blue')
            
    node_plots[i-1].setLabel('left', 'Note', units='')
    node_plots[i-1].setLabel('bottom', 'Time', units='s')
    
    
            


def procesar_midi_messages(midi_messages):
    int_tiempos = {}
    int_velocities = {}
    
    for message in midi_messages:
        pitch = message.pitch
        start = message.start
        end = message.end
        velocity = message.velocity
        
        if pitch not in int_tiempos:
            int_tiempos[pitch] = []
            int_velocities[pitch] = []
        
        # Añadir el intervalo de tiempo
        int_tiempos[pitch].append([start, end])
        
        # Añadir la velocidad para el intervalo de tiempo
        int_velocities[pitch].append(velocity)
    
    return int_tiempos, int_velocities



