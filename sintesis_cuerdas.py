import IPython.display as ipd
import matplotlib.pyplot as plt
import numpy
import scipy.io.wavfile as wav
from numpy import random
from collections import deque
import time, random 
import scipy.signal as signal
import librosa

sr = 22050


def pitch2frec(pitch):
    freq = 2**((pitch-69)/12) * 440 # See https://en.wikipedia.org/wiki/Pitch_(music)#Labeling_pitches
    return freq



# generate note of given frequency
def generateNote(freq,vel,gShowPlot=False):
    nSamples = 44100
    sampleRate = 44100
    if freq == 0:
        return numpy.zeros(nSamples)
    else:
        N = int(sampleRate/freq)
    # initialize ring buffer
    buf = deque([random.random() - 0.5 for i in range(N)])
    # plot of flag set 
    if gShowPlot:
        axline, = plt.plot(buf)
    # init sample buffer
    samples = numpy.array([0]*nSamples, 'float32')
    for i in range(nSamples):
        samples[i] = buf[0]
        avg = (0.9+vel/1280)*0.48*(buf[0] + buf[1])
        buf.append(avg)
        buf.popleft()  
        # plot of flag set 
        if gShowPlot:
            if i % 1000 == 0:
                axline.set_ydata(buf)
                plt.draw()
      
    # samples to 16-bit to string
    # max value is 32767 for 16-bit
    samples = numpy.array(samples * 32767, 'int16')
    return samples


def ADSR_envelope(signal, vel, attack_time, decay_time, decay_amp, sustain_amp, release_time, duration, sample_rate):
    A = vel/127
    
    t = (len(signal)/sample_rate)
    
    """
    min_time = attack_time + decay_time + release_time

    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)
    release_samples = int(release_time * sample_rate)

    if duration < min_time: #la nota dura menos que el tiempo ADR
        sustain_samples = 0
    elif duration < t:  #la nota dura menos que el tiempo de la señal, dejo release y corto attack
        sustain_samples = 0
    else:
        sustain_samples = int((duration - min_time) * sample_rate)

    
    total_samples = int(duration * sample_rate)
    
    envelope = numpy.ones(total_samples)
    
    if(attack_samples+decay_samples > total_samples-release_samples):
        decay_samples = total_samples-release_samples-attack_samples
    
    if duration < min_time:
        envelope[total_samples-release_samples:] = numpy.linspace(sustain_amp*A, 0, release_samples)
        envelope[:total_samples-release_samples] = numpy.linspace(0, sustain_amp*A, total_samples-release_samples)
    else:
        envelope[:attack_samples] = numpy.linspace(0, A, attack_samples)
        envelope[attack_samples:attack_samples+decay_samples] = numpy.linspace(A, decay_amp*A, decay_samples)
        envelope[attack_samples+decay_samples:total_samples-release_samples] = numpy.linspace(decay_amp*A, decay_amp*A,sustain_samples)
        envelope[total_samples-release_samples:] = numpy.linspace(sustain_amp*A, 0, release_samples)
    
    """
    signal = (signal / numpy.max(signal))*A
    signal = librosa.effects.time_stretch(signal, rate=(t/duration))
    # Apply envelope to the signal
    return signal #* envelope

import numpy as np

def karplus_strong(wavetable, n_samples, stretch_factor):
    # stretch_factor = 1    no altera el estiramiento de la nota
    # stretch_factor = inf  genera un tono puro.
    samples = [] 
    # Condiciones Iniciales:
    curr_sample = 0 # Índice para recorrer la tabla de onda
    prev_value = 0  # Valor anterior
    while len(samples) < n_samples: # Recorro hasta que retorno tenga mismo largo
        stretch = np.random.binomial(1, 1-1/stretch_factor)
        if stretch == 0: # Hago el promedio entre la muestra y la anterior
            wavetable[curr_sample] = 0.5 * (wavetable[curr_sample] + prev_value)
        samples.append(wavetable[curr_sample])
        prev_value = samples[-1]    # Tomo el último valor que ingresé a la nueva señal
        curr_sample = (curr_sample+1) % wavetable.size  # Avanzo el índice circularmente
    return np.array(samples)


class GuitarString:
    def __init__(self, pitch, fs, A, T, noise_type, S=1):
        """Initialize Guitar String"""
        self.pitch = pitch                      # Frecuencia de la nota
        self.fs = fs                            # Frecuencia de Sampleo
        self.S = S                              # Stretch Factor
        self.A = A                              # Amplitud
        self.T = T                              # Duración de la nota (samples)
        self.noise_type = noise_type            # Tipo de Ruido Inicial
        self.init_wavetable()
        self.init_samples()
        self.L = None
        
    def init_wavetable(self):
        """Generate new Wavetable for String"""
        self.L = int(np.floor(self.fs / int(self.pitch)-1/2/self.S))
        if self.noise_type == "normal":
            self.wavetable = (self.A * np.random.normal(0, 1, self.L))#.astype(np.float)
        if self.noise_type == "uniform":
            self.wavetable = (self.A * np.random.uniform(-1, 1, self.L))#.astype(np.float)
        if self.noise_type == "2-level":
            self.wavetable = (self.A * 2 * np.random.randint(0, 2, self.L) - 1)#.astype(np.float)

    def init_samples(self):
        """Create sound samples for string"""
        self.samples = karplus_strong(self.wavetable, 2*self.T, self.S)
        
    def get_samples(self):
        """Return Sound Samples"""
        return self.samples




def chord(frec,vel):
    note1 = generateNote(frec[0],vel)
    note2 = generateNote(frec[1],vel)
    note3 = generateNote(frec[2],vel)
    note4 = generateNote(frec[3],vel)
    output = note1+note2+note3+note4
    output = ADSR_envelope(output, vel, 0.05, 0.74, 0.54, 0.13, 0.08, sr)
    return output

def synth_guitar (midi_note,vel,dur):
    note = GuitarString(pitch2frec(midi_note), 44100, 1, 22050, "normal", 1)
    note_samples = note.get_samples()
    output = librosa.effects.time_stretch(note_samples, rate=1/dur)
    """
    note = generateNote(pitch2frec(midi_note),vel)
    note = note/numpy.max(note)
    output = ADSR_envelope(note,170, 0.1,0.05, 0.64, 0.54, 0.13, dur,sr)
    output = output/numpy.max(output)
    """
    return output

def synth_hihat(midi_pitch, vel, dur):
    length = int(sr*0.5)
    noise = numpy.random.sample(length)*2-1

    t = numpy.arange(length)/sr
    env = .5 ** (t*25)

    hihat = noise * env

    hihat = ADSR_envelope(hihat, vel, 0.05, 0.1, 0.3, 0.3, 0.1, dur, sr)
    maxAmp = numpy.max(numpy.abs(hihat))
    hihat = hihat / maxAmp
    return hihat

def sumation(callback, freq):
    phaseY = numpy.cumsum(freq)
    x = numpy.sin((phaseY)*(2*numpy.pi)/sr)
    return x

def synth_kick(midi_note, vel, dur):
    length = int(sr*dur)
    lowfreq = midi_note
    highfreq = lowfreq*10+50
    t = numpy.maximum(1 - numpy.arange(length)/sr / .05, 0)
    freqs = (highfreq-lowfreq)*t**4 + lowfreq

    kick = sumation(numpy.sin, freqs)
    b,a = signal.butter(4, lowfreq*10, fs=(44100*2), btype='low', analog=False)
    kick = signal.lfilter(b, a, kick)

    decay_rate = 2.5 # Adjust the decay rate as desired

    envelope = numpy.exp(-decay_rate * numpy.arange(length) / sr)
    kick = kick * envelope * 5
    t = len(kick)/sr
    kick = librosa.effects.time_stretch(kick, rate=t/dur)
    return kick