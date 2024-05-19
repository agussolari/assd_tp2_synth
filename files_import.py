from PyQt5.QtWidgets import QFileDialog
import mido
import plots as pl
from mido import Message, MidiFile, MidiTrack
import threading
import time as tt
import threading
import mido
import sounddevice as sd


#Definir constantes
PIANO_BOX = 1
GUITAR_BOX = 2
HIHAT = 3
KICK = 4
CLARINET = 5
TUBA = 6
SAX = 7
SNARE = 8




def import_track_files(self, i):
    filename = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Track Files (*.mid *.midi)')
    if filename[0]:
        if i == 1:
            self.track_data.track_1_filename = filename[0]
        elif i == 2:
            self.track_data.track_2_filename = filename[0]
        elif i == 3:
            self.track_data.track_3_filename = filename[0]
    notes_proccessing(self, i)
    

def leer_archivo_midi(ruta_archivo):
    try:
        mid = pretty_midi.PrettyMIDI(ruta_archivo)
        return mid
    except Exception as e:
        print("Error al leer el archivo MIDI:", e)
        return None

def dividir_pistas(mid, canal_deseado):
    return mid.instruments[canal_deseado].notes


def notes_proccessing(self, i):
    # node_filenames = [self.track_data.track_1_filename, self.track_data.track_2_mid, self.track_data.track_3_mid]
    # node_box = [self.channel_1_box.value(), self.channel_2_box.value(), self.channel_3_box.value()]
    node_filenames = [self.track_data.track_1_filename, self.track_data.track_2_filename, self.track_data.track_3_filename]
    node_box = [self.channel_1_box.value(), self.channel_2_box.value(), self.channel_3_box.value()]
    node_mid = [self.track_data.track_1_mid, self.track_data.track_2_mid, self.track_data.track_3_mid]
    node_samples = [self.track_data.track_1_samples, self.track_data.track_2_samples, self.track_data.track_3_samples]
    
    if node_filenames[i-1] != []:
        mid = leer_archivo_midi(  node_filenames[i-1] )
        if mid is not None:
            mid_data = dividir_pistas(mid, int(node_box[i-1]))
            if i == 1:
                self.track_data.track_1_mid = mid_data
            elif i == 2:
                self.track_data.track_2_mid = mid_data
            elif i == 3:
                self.track_data.track_3_mid = mid_data
    plot_data(self, i)
            
                        
def thread_synth_data_1 (self):
    synth_data_1 = threading.Thread(target=synth_data, args=(self, 1, ))
    synth_data_1.start()  

def thread_synth_data_2 (self):
    synth_data_2 = threading.Thread(target=synth_data, args=(self, 2, ))
    synth_data_2.start()
    
def thread_synth_data_3 (self):
    synth_data_3 = threading.Thread(target=synth_data, args=(self, 3, ))
    synth_data_3.start()
    
            
def synth_data(self, i):
    node_ins_box = [self.track_1_box.currentIndex(), self.track_2_box.currentIndex(), self.track_3_box.currentIndex()]
    node_play_buttons = [self.play_track_1, self.play_track_2, self.play_track_3]
    node_stop_buttons = [self.stop_track_1, self.stop_track_2, self.stop_track_3]

    node_play_buttons[i-1].setEnabled(False)
    node_stop_buttons[i-1].setEnabled(False)
    
    
    if(node_ins_box[i-1] == PIANO_BOX):
        print("Sintetizando piano")
        if (i == 1):
            self.track_data.track_1_samples = synthesis_piano(self.track_data.track_1_mid)
        elif (i == 2):
            self.track_data.track_2_samples = synthesis_piano(self.track_data.track_2_mid)
        elif (i == 3):
            self.track_data.track_3_samples = synthesis_piano(self.track_data.track_3_mid)
        print("Sintetizacion piano finalizada")
        
    elif(node_ins_box[i-1] == GUITAR_BOX):
        print("Sintetizando guitarra")
        if (i == 1):
            self.track_data.track_1_samples = synthesis_guitar(self.track_data.track_1_mid)
        elif (i == 2):
            self.track_data.track_2_samples = synthesis_guitar(self.track_data.track_2_mid)
        elif (i == 3):
            self.track_data.track_3_samples = synthesis_guitar(self.track_data.track_3_mid)
        print("Sintetizacion guitar finalizada")
    
    elif(node_ins_box[i-1] == HIHAT):
        print("Sintetizando hihat")
        if (i == 1):
            self.track_data.track_1_samples = synthesis_hihat(self.track_data.track_1_mid)
        elif (i == 2):
            self.track_data.track_2_samples = synthesis_hihat(self.track_data.track_2_mid)
        elif (i == 3):
            self.track_data.track_3_samples = synthesis_hihat(self.track_data.track_3_mid)
        print("Sintetizacion hihat finalizada")
        
    elif(node_ins_box[i-1] == KICK):
        print("Sintetizando kick")
        if (i == 1):
            self.track_data.track_1_samples = synthesis_kick(self.track_data.track_1_mid)
        elif (i == 2):
            self.track_data.track_2_samples = synthesis_kick(self.track_data.track_2_mid)
        elif (i == 3):
            self.track_data.track_3_samples = synthesis_kick(self.track_data.track_3_mid)
        print("Sintetizacion kick finalizada")
        
    elif(node_ins_box[i-1] == CLARINET):
        print("Sintetizando clarinete")
        if (i == 1):
            self.track_data.track_1_samples = synthesis_clarinet(self.track_data.track_1_mid)
        elif (i == 2):
            self.track_data.track_2_samples = synthesis_clarinet(self.track_data.track_2_mid)
        elif (i == 3):
            self.track_data.track_3_samples = synthesis_clarinet(self.track_data.track_3_mid)
        print("Sintetizacion clarinete finalizada")
        
    elif(node_ins_box[i-1] == TUBA):
        print("Sintetizando tuba")
        if (i == 1):
            self.track_data.track_1_samples = synthesis_tuba(self.track_data.track_1_mid)
        elif (i == 2):
            self.track_data.track_2_samples = synthesis_tuba(self.track_data.track_2_mid)
        elif (i == 3):
            self.track_data.track_3_samples = synthesis_tuba(self.track_data.track_3_mid)
        print("Sintetizacion tuba finalizada")
        
    elif(node_ins_box[i-1] == SAX):
        print("Sintetizando saxofon")
        if (i == 1):
            self.track_data.track_1_samples = synthesis_sax(self.track_data.track_1_mid)
        elif (i == 2):
            self.track_data.track_2_samples = synthesis_sax(self.track_data.track_2_mid)
        elif (i == 3):
            self.track_data.track_3_samples = synthesis_sax(self.track_data.track_3_mid)
        print("Sintetizacion saxofon finalizada")
        
    elif(node_ins_box[i-1] == SNARE):
        print("Sintetizando snare")
        if (i == 1):
            self.track_data.track_1_samples = synthesis_snare(self.track_data.track_1_mid)
        elif (i == 2):
            self.track_data.track_2_samples = synthesis_snare(self.track_data.track_2_mid)
        elif (i == 3):
            self.track_data.track_3_samples = synthesis_snare(self.track_data.track_3_mid)
        print("Sintetizacion snare finalizada")
    
    node_play_buttons[i-1].setEnabled(True)
    node_stop_buttons[i-1].setEnabled(True)

                            

def plot_data(self, i):
    if i == 1:
        mid_data = self.track_data.track_1_mid
    elif i == 2:
        mid_data = self.track_data.track_2_mid
    elif i == 3:
        mid_data = self.track_data.track_3_mid
        
    pl.plot_scatter(mid_data, self, i)
    pl.plot_temporal(mid_data, self, i)
    pl.plot_spectrogram(mid_data, self, i)
    



    


        
        

# Variable global para controlar la reproducción
stop_playing = False

def thread_play_samples(self, i):
    node_samples = [self.track_data.track_1_samples, self.track_data.track_2_samples, self.track_data.track_3_samples, self.track_data.track_4_samples]
    if self.checkBox_r_t1.isChecked():
        node_samples[0] = self.track_data.track_1_effects
    if self.checkBox_r_t2.isChecked():
        node_samples[1] = self.track_data.track_2_effects
    if self.checkBox_r_t3.isChecked():
        node_samples[2] = self.track_data.track_3_effects
    if self.checkBox_r_t4.isChecked():
        node_samples[3] = self.track_data.track_4_effects
    node_vol = [self.track_1_vol.value()/100, self.track_2_vol.value()/100, self.track_3_vol.value()/100]
    node_pan = [self.track_1_pan.value()/100, self.track_2_pan.value()/100, self.track_3_pan.value()/100]
    
    if i == 4:
        # Encuentra la longitud del array más largo
        max_length = max(len(samples) for samples in node_samples[:-1])

        # Rellena los arrays más cortos con ceros hasta que tengan la misma longitud que el array más largo
        node_samples = [np.pad(samples, (0, max_length - len(samples))) for samples in node_samples[:-1]]

        
        self.track_data.track_4_samples = node_samples[0] + node_samples[1] + node_samples[2]
        
        # Suma los arrays para mezclar los sonidos
        vol_1 = self.track_1_vol.value()/100
        vol_2 = self.track_2_vol.value()/100
        vol_3 = self.track_3_vol.value()/100
        
        #panning
        pan = self.track_pan.value()/100
        pan_1 = self.track_1_pan.value()/100
        pan_2 = self.track_2_pan.value()/100
        pan_3 = self.track_3_pan.value()/100
        
        
        track_1 = np.vstack([(1-pan)*(1-pan_1)*vol_1*node_samples[0] , (pan)*(pan_1)*vol_1*node_samples[0]])
        track_2 = np.vstack([(1-pan)*(1-pan_2)*vol_2*node_samples[1] , (pan)*(pan_2)*vol_2*node_samples[1]])
        track_3 = np.vstack([(1-pan)*(1-pan_3)*vol_3*node_samples[2] , (pan)*(pan_3)*vol_3*node_samples[2]])
        
        samples = (track_1 + track_2 + track_3).T
        
        pl.plot_spectrogram_from_samples(self, self.track_data.track_4_samples)
    else:
        samples = node_vol[i-1]*np.vstack([(1-node_pan[i-1])*(node_samples[i-1]), (node_pan[i-1])*(node_samples[i-1])] ).T
        pl.plot_spectrogram_from_samples(self, node_samples[i-1])
        
    global stop_playing
    stop_playing = False
    midi_thread = threading.Thread(target=play, args=(samples, ))
    midi_thread.start()

def stop_playback():
    print("Stopping playback")
    global stop_playing
    stop_playing = True
    sd.stop()
    
    
def play(samples):
    if len(samples) != 0:
        while not stop_playing:
            print("Playing MIDI")
            sd.play(samples, 44100)
            sd.wait()
            print("Playback finished")
            stop_playback()


import numpy as np
import pretty_midi
from sample_synth import synth_piano
from sintesis_cuerdas import synth_guitar, synth_hihat, synth_kick
from sintesis_aditiva import synth_clarinet, synth_tuba, synth_sax, synth_snare


sample_rate = 44100

def get_notes_from_track(track):
    notes = []
    for note in track:
        notes.append({
            'pitch': note.pitch,
            'start': note.start,
            'end': note.end,
            'velocity': note.velocity,
            'synth': []
        })
    return notes

def synthesis_instrument (track, instrument):
    track_notes = get_notes_from_track(track)
    
    min_pitch = min(note['pitch'] for note in track_notes)
    max_pitch = max(note['pitch'] for note in track_notes)
    max_end = max(note['end'] for note in track_notes)

    for note in track_notes:
        note['synth'] = instrument(note['pitch'],  note['velocity'], note['end'] - note['start'])

    num_pitches = max_pitch - min_pitch + 1
    num_samples = int(np.ceil(max_end))*sample_rate
    tracks_s = np.zeros((num_pitches, num_samples))

    for note in track_notes:
        pitch = note['pitch'] - min_pitch
        start_frame = round(note['start']*sample_rate)
        # end_frame = int(np.ceil(note['end']*sample_rate))
        end_frame = start_frame + len(note['synth'])
        tracks_s[pitch, start_frame:end_frame] = note['synth']

    return np.sum(tracks_s, axis=0)

# SÍNTESIS POR MUESTRAS

def synthesis_piano (track):
    return synthesis_instrument(track, synth_piano)

# SÍNTESIS DE MODELOS FÍSICOS

def synthesis_guitar (track):
    return synthesis_instrument(track, synth_guitar)

def synthesis_hihat (track):
    return synthesis_instrument(track, synth_hihat)

def synthesis_kick (track):
    return synthesis_instrument(track, synth_kick)

# SÍNTESIS ADITIVA

def synthesis_clarinet (track):
    return synthesis_instrument(track, synth_clarinet)

def synthesis_tuba (track):
    return synthesis_instrument(track, synth_tuba)

def synthesis_sax (track):
    return synthesis_instrument(track, synth_sax)

def synthesis_snare (track):
    return synthesis_instrument(track, synth_snare)