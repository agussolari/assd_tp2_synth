import IPython.display as ipd
import matplotlib.pyplot as plt
import numpy
import math
import scipy.io.wavfile as wav
from numpy import random
from collections import deque
import sys, os
import time, random 
import wave, argparse
import scipy.signal as signal
import librosa

sr = 22050

def makesine(freq, dur):
    t = numpy.linspace(0, dur, math.ceil(sr*dur))
    x = numpy.sin(2 * numpy.pi * freq * t)
    return x

def addsyn(freq, dur, amplist):
    i = 1
    t = numpy.linspace(0, dur, math.ceil(sr*dur))
    ### initialize a new output
    out = numpy.zeros(t.size)
    for amp in amplist:
        ### make a sine waveform with this max amplitude
        ### frequency is the integer multiple 
        x = numpy.multiply(makesine(freq*i, dur), amp)
        ### sum it to the output
        out = out + x
        i+=1
    ### making sure the maximum amplitude does not exeed 1
    if numpy.max(out)>abs(numpy.min(out)):
        out = out / numpy.max(out)
    else:
        out = out / -numpy.min(out)
    return out

def pitch2frec(pitch):
    freq = 2**((pitch-69)/12) * 440 # See https://en.wikipedia.org/wiki/Pitch_(music)#Labeling_pitches
    return freq

def ADSR_envelope(signal, vel, attack_time, decay_time, decay_amp, sustain_amp, release_time, sample_rate):
    A = vel/127
    total_samples = len(signal)

    t = total_samples/sample_rate
    min_t = attack_time + decay_time + release_time
    if(min_t > t):
        attack_time = attack_time * t/min_t
        decay_time = decay_time * t/min_t
        release_time = release_time * t/min_t

    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)
    sustain_samples = int((1-attack_time-decay_time-release_time) * sample_rate)
    release_samples = int(release_time * sample_rate)


    envelope = numpy.ones(total_samples)
    
    # Attack phase
    envelope[:attack_samples] = numpy.linspace(0, A, attack_samples)
    
    # Decay phase
    envelope[attack_samples:attack_samples+decay_samples] = numpy.linspace(A, decay_amp*A, decay_samples)
    
    # Sustain phase
    envelope[attack_samples+decay_samples:total_samples-release_samples] = numpy.linspace(decay_amp*A, decay_amp*A,sustain_samples)
    
    # Release phase
    envelope[total_samples-release_samples:] = numpy.linspace(decay_amp*A, 0, release_samples)
    
    # Apply envelope to the signal
    return signal * envelope









def synth_add(note_midi, vel, dur, partials):
    xy = addsyn(pitch2frec(note_midi), dur, partials)
    b,a = signal.butter(4, 0.1, 'low', analog=False)
    xy = signal.filtfilt(b, a, xy)
    attack_time = 0.3
    decay_time = 0.1
    release_time = 0.4
    min_time = attack_time+decay_time+release_time
    
    if(min_time>dur):
        attack_time = attack_time*dur/min_time
        decay_time = decay_time*dur/min_time
        release_time = release_time*dur/min_time

    #x= ADSR_envelope(xy, 127, attack_time, decay_time, 0.82, 0.88, release_time, sr)
    x = xy/numpy.max(xy)
    return x

def synth_clarinet(note_midi, vel, dur):
    partials_clarinet = [0.517, 0.834, 0.467, 0.421, 0.738, 0.143, 0.3,0.869 ,0.631 ,0.855, 0.532, 0.652, 0.023, 0.047]
    return synth_add(note_midi, vel, dur, partials_clarinet)

def synth_tuba(note_midi, vel, dur):
    partials_tuba = [1, 0.2, 0.04, 0.88, 0.74, 0.32, 0.74, 0.64, 0.97, 0.11, 0.12]
    return synth_add(note_midi, vel, dur, partials_tuba)

def synth_sax(note_midi, vel, dur):
    partials_sax = [1, 0.263, 0.14, 0.099, 0.209, 0.02, 0.029, 0.077, 0.017, 0.01]
    return synth_add(note_midi, vel, dur, partials_sax)

def synth_snare(note_midi, vel, dur):
    partials_snare = [0.445, 0.224, 0.0, 0.023, 0.022, 0.022, 0.025, 0.03, 0.0, 0.022, 0.022, 0.02, 0.033, 0.026]
    return synth_add(note_midi, vel, dur, partials_snare)
