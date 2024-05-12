from PyQt5.QtWidgets import QFileDialog
import mido
import plots as pl
from mido import Message, MidiFile, MidiTrack
import threading
import time as tt



def import_track_files(self, i):
    filename = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Track Files (*.mid *.midi)')
    print(filename[0])
    if filename[0]:
        if i == 1:
            self.track_data.track_1_filename = filename[0]
        elif i == 2:
            self.track_data.track_2_filename = filename[0]
        elif i == 3:
            self.track_data.track_3_filename = filename[0]

def leer_archivo_midi(ruta_archivo):
    try:
        mid = MidiFile(ruta_archivo)
        return mid
    except Exception as e:
        print("Error al leer el archivo MIDI:", e)
        return None

def dividir_pistas(mid, canal_deseado):
    mensajes_filtrados = []  # Usar una lista para almacenar mensajes filtrados
    tiempo_actual = 0  # Inicializar el tiempo del mensaje anterior

    for mensaje in mid:
        if hasattr(mensaje, 'channel') and mensaje.channel == canal_deseado:
            mensajes_filtrados.append(mensaje)
            
    return mensajes_filtrados


def notes_proccessing(self, i):
    # node_filenames = [self.track_data.track_1_filename, self.track_data.track_2_mid, self.track_data.track_3_mid]
    # node_box = [self.channel_1_box.value(), self.channel_2_box.value(), self.channel_3_box.value()]
    node_filenames = [self.track_data.track_1_filename, self.track_data.track_2_filename, self.track_data.track_3_filename]
    node_box = [self.channel_1_box.value(), self.channel_2_box.value(), self.channel_3_box.value()]
    node_mid = [self.track_data.track_1_mid, self.track_data.track_2_mid, self.track_data.track_3_mid]
    
    if node_filenames[i-1] != []:
        
        print("procesando notas:", i)
        # print(i, type(i))
        print(node_filenames[i-1])

        mid = leer_archivo_midi(  node_filenames[i-1] )
        if mid is not None:
            mid_data = dividir_pistas(mid, int(node_box[i-1]))
            # print(mid_data)
            if i == 1:
                self.track_data.track_1_mid = mid_data
            elif i == 2:
                self.track_data.track_2_mid = mid_data
            elif i == 3:
                self.track_data.track_3_mid = mid_data
            
            # types, times, notes, velocities = pl.parse_data(mensajes_filtrados)
            # print(types, times, notes, velocities)
            
            # print(mid_data)
            
            pl.plot_scatter(mid_data, self, i)
            pl.plot_temporal(mid_data, self, i)
            # pl.plot_spectrogram(mid_data, self, i)
            
            # print(mid_data)
            # pl.plot_notes_over_time(notes, times, types, self, i)

            # pl.plot_spectrogram(notes, velocities, times, self)
        
        
        
import threading
import mido
from mido import MidiFile, MidiTrack, Message
import time as tt

# Variable global para controlar la reproducción
stop_playing = False

def thread_play_midi(i, self):
    global stop_playing
    stop_playing = False
    midi_thread = threading.Thread(target=play_midi, args=(i, self, ))
    midi_thread.start()

def stop_playback():
    global stop_playing
    stop_playing = True

def play_midi(i, self):
    global stop_playing

    print('Playing MIDI...')
    times = []
    notes = []
    velocities = []
    types = []
    

    node_filenames = [self.track_data.track_1_filename, self.track_data.track_2_filename, self.track_data.track_3_filename]
    node_box = [self.channel_1_box.value(), self.channel_2_box.value(), self.channel_3_box.value()]

    mid = leer_archivo_midi(node_filenames[i-1])

    for mensaje in mid:
        if hasattr(mensaje, 'channel') and mensaje.channel == node_box[i-1]:
            types.append(mensaje.type)
            times.append(mensaje.time)
            notes.append(mensaje.note)
            velocities.append(mensaje.velocity)

    print(times, notes, velocities)

    # Crear un nuevo archivo MIDI
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Añadir los mensajes al track
    prev_time = 0
    for note, time, velocity in zip(notes, times, velocities):
        interval = time - prev_time
        track.append(Message('note_on', note=note, velocity=velocity, time=interval))
        prev_time = time

    # Reproducir el archivo MIDI
    with mido.open_output() as outport:
        for msg in mid.play():
            if stop_playing:
                print('MIDI playback stopped.')
                break  # Si se establece stop_playing en True, salimos del bucle
            outport.send(msg)
            tt.sleep(float(msg.time)) # Esperar la duración del mensaje

    print('MIDI playback finished.')

