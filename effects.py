import numpy as np
import scipy.signal as signal
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift
from PyQt5.QtWidgets import QFileDialog

### Presets/Pre-Configurations ###

# Simple

s_gain = 0.7
s_delay = 4410

# Low Pass

fb_gain = 0.7
low_pass_gain = 0.4
lp_delay = 4410

# All Pass

ap_gains = [0.7, 0.7, 0.7]
ap_delays = [1051, 337, 113]

# SATRev

jcrev_comb_delays = [4799, 4999, 5399, 5801]
jcrev_comb_gains = [0.742, 0.733, 0.715, 0.697]
jcrev_all_pass_delay = [1051, 337, 113]
jcrev_all_pass_gains = [0.7, 0.7, 0.7]

# JCRev

satrev_comb_delays = [901, 778, 1011, 1123]
satrev_comb_gains = [0.805, 0.827, 0.783, 0.764]
satrev_all_pass_delay = [125, 42, 12]
satrev_all_pass_gains = [0.7, 0.7, 0.7]

# Moorer

moorer_delays_early = [877, 1561, 1715, 1825, 3082, 3510]
moorer_gains_early = [1.02, 0.818, 0.635, 0.719, 0.267, 0.242]
moorer_delays_r = [2205, 2469, 2690, 2998, 3175, 3439] # Comb
moorer_g1_list = [0.41, 0.43, 0.45, 0.47, 0.48, 0.50] # Low Pass
moorer_g = 0.84
moorer_rev_to_er_delay = 1800
moorer_allpass_delay = 286
moorer_allpass_g = 0.7

# Freeverb

freeverb_delays_early = [190,  949,  993,  1183, 1192, 1315,
                            2021, 2140, 2524, 2590, 2625, 2700,
                            3119, 3123, 3202, 3268, 3321, 3515]
freeverb_gains_early = [0.841, 0.504, 0.49,  0.379, 0.38,  0.346,
                        0.289, 0.272, 0.192, 0.193, 0.217,  0.181,
                        0.18,  0.181, 0.176, 0.142, 0.167, 0.134]
freeverb_comb_delays = [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617]
freeverb_allpass_delays = [556, 441, 341, 225]

# Convolution

irsamples = ['src/ir_samples/EMES_Virtual_Rooms/Ambience_Close_Mic.wav',
             'src/ir_samples/EMES_Virtual_Rooms/Ambience_with_Punch.wav',
             'src/ir_samples/EMES_Virtual_Rooms/Arena_South_West.wav',
             'src/ir_samples/EMES_Virtual_Rooms/Bright_Big_Room.wav',
             'src/ir_samples/EMES_Virtual_Rooms/Gothic_Church.wav',
             'src/ir_samples/EMES_Virtual_Rooms/One_Wall_on_a_Room.wav',
             'src/ir_samples/EMES_Virtual_Rooms/Small_Studio.wav',
             'src/ir_samples/EMES_Virtual_Rooms/Sparkling_Hall.wav',
             'src/ir_samples/EMES_Virtual_Rooms/Stonewall_Room.wav',
             'src/ir_samples/Voxengo/cement_blocks.wav',
             'src/ir_samples/Voxengo/chateau_de_logne_outside.wav',
             'src/ir_samples/Voxengo/conic_long_echo_hall.wav',
             'src/ir_samples/Voxengo/french_18th_century_salon.wav',
             'src/ir_samples/Voxengo/greek_7_echo_hall.wav',
             'src/ir_samples/Voxengo/highly_damped_large_room.wav',
             'src/ir_samples/Voxengo/large_wide_echo_hall.wav',
             'src/ir_samples/Voxengo/masonic_lodge.wav',
             'src/ir_samples/Voxengo/musikvereinsaal.wav',
             'src/ir_samples/Voxengo/narrow_bumpy_space.wav',
             'src/ir_samples/Voxengo/on_a_star.wav',
             'src/ir_samples/Voxengo/scala_milan_opera_hall.wav',
             'src/ir_samples/Voxengo/small_prehistoric_cave.wav',
             'src/ir_samples/Voxengo/vocal_duo.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_bright_1.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_bright_2.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_bright_3.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_bright_4.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_bright_5.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_dark_1.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_dark_2.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_dark_3.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_dark_4.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_dark_5.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_medium_1.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_medium_2.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_medium_3.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_medium_4.wav',
             'src/ir_samples/EMT-140_Plate/emt_140_medium_5.wav',
             'src/ir_samples/EchoThief/Batcave.wav',
             'src/ir_samples/EchoThief/BatteryBenson.wav',
             'src/ir_samples/EchoThief/ByronGlacier.wav',
             'src/ir_samples/EchoThief/CathedralRoom.wav',
             'src/ir_samples/EchoThief/CleftRidgeArch.wav',
             'src/ir_samples/EchoThief/NaumburgBandshell.wav',
             'src/ir_samples/EchoThief/Qasgiq.wav',
             'src/ir_samples/EchoThief/RacquetballCourt.wav',
             'src/ir_samples/EchoThief/RedBridge.wav'
]

def delay(input_signal, delay, gain = 1):
    output_signal = np.concatenate((np.zeros(delay), input_signal))
    output_signal = output_signal*gain
    return output_signal

def comb(input_signal, delay, gain):
    B = np.zeros(delay)
    B[delay-1] = 1
    A = np.zeros(delay)
    A[0] = 1
    A[delay-1] = -gain
    output_signal = np.zeros(input_signal.shape)
    output_signal = signal.lfilter(B, A, input_signal)
    return output_signal

def combWithLowPass(input_signal, delay, g, g1):
    g2 = g*(1-g1)
    B = np.zeros(delay+1)
    B[delay-1] = 1
    B[delay] = -g1
    A = np.zeros(delay)
    A[0] = 1
    A[1] = -g1
    A[delay-1] = -g2
    output_signal = np.zeros(input_signal.shape)
    output_signal = signal.lfilter(B, A, input_signal)
    return output_signal

def allpass(input_signal, delay, gain):
    B = np.zeros(delay)
    B[0] = gain
    B[delay-1] = 1
    A = np.zeros(delay)
    A[0] = 1
    A[delay-1] = gain
    output_signal = np.zeros(input_signal.shape)
    output_signal = signal.lfilter(B, A, input_signal)
    return output_signal

def echo(sample, repetitions, echo_delay, dry_gain, wet_gain):
    yff = np.concatenate((sample, np.zeros(echo_delay*repetitions)))
    yfb = np.zeros(yff.shape)
    for m in range(repetitions):
        yfb += np.concatenate((delay(sample, echo_delay*(m+1))*wet_gain*np.exp(-(m+1)),
                               np.zeros(echo_delay*(repetitions-(m+1)))))

    return yff*dry_gain+yfb

def simpleReverb(sample, fb_gains, delays, dry_gain, wet_gain):
    y = np.zeros(len(sample))
    for i in range(len(delays)):
        y += comb(sample, delays[i], fb_gains[i])

    return sample*dry_gain+y*wet_gain

def lowPassReverb(sample, fb_gains, lp_gains, delays, dry_gain, wet_gain):
    y = np.zeros(len(sample))
    for i in range(len(delays)):
        y += combWithLowPass(sample, delays[i], fb_gains[i], lp_gains[i])

    return sample*dry_gain+y*wet_gain

def allPassReverb(sample, gains, delays, dry_gain, wet_gain):
    y = allpass(sample, delays[0], gains[0])
    for i in range(1, len(gains)):
        y = allpass(y, int(delays[i]), gains[i])

    return sample*dry_gain+y*wet_gain

def schroederReverb(sample, comb_delays, all_pass_delays,
                    comb_gains, allpass_gains, dry_gain, wet_gain):
    y = np.zeros(len(sample))
    for i in range(len(comb_delays)):
        y += comb(sample, comb_delays[i], comb_gains[i])

    for i in range(len(all_pass_delays)):
        y += allpass(y, all_pass_delays[0], allpass_gains[0])

    return sample*dry_gain+y*wet_gain

def moorerFreeverbReverb(sample_in, delays_early, gains_early, rev_to_er_delay,
                         allpass_delay, allpass_g, dry_gain,
                         wet_gain, hf_damping, stereo_width,
                         room_scale, pre_delay, delays_r, g, g1_list,
                         reverberance, channels = 2, sample_rate = 44100):
    if len(sample_in)%2 != 0:
        sample_in = sample_in[:-1]
    sample = np.array([sample_in[0::2], sample_in[1::2]], dtype = np.float64)
    sample[0] /= np.max(np.abs(sample[0]), axis = 0)
    sample[1] /= np.max(np.abs(sample[1]), axis = 0)

    r = sample_rate/44100
    stereospread = 23 # Freeverb
    delays_l = [d+stereospread for d in delays_early]

    # Configurations
    delay_length = int(pre_delay*sample_rate+0.5)-delays_early[0]
    delays_early = [delays_early[i]+delay_length for i in range(len(delays_early))]
    scale = room_scale/100*0.9+0.1
    width = stereo_width/100
    a = -1/np.log(0.7)
    b = 100/(np.log(0.02)*a+1)
    if g is None:
        g = 1-np.exp((reverberance-b)/(a*b))
    if g1_list is None:
        g1_list = [(hf_damping/100)*0.3+0.2]*len(delays_r)

    wet1 = wet_gain * (width/2+0.5)
    wet2 = wet_gain * ((1-width)/2)

    stereo = channels == 2

    # # Pre-delay buffer
    # if delay_length != 0:
    #     sample[0] = delay(sample[0], delay_length)[:sample[0].size]
    #     sample[1] = delay(sample[1], delay_length)[:sample[1].size]

    # Early reflections by tapped delay line
    early_reflections_r = np.zeros(sample[0].size)
    early_reflections_l = np.zeros(sample[1].size)
    n_early = len(delays_early)
    for i in range(n_early):
        early_reflections_r = early_reflections_r+delay(sample[0], delays_early[i], gains_early[i])[:sample[0].size]
        early_reflections_l = early_reflections_l+delay(sample[1], delays_early[i], gains_early[i])[:sample[1].size]

    # Parallel comb filters
    combs_out_r = np.zeros(sample[0].size)
    combs_out_l = np.zeros(sample[1].size)
    n_r = len(delays_r)
    for i in range(n_r):
        combs_out_r = combs_out_r+combWithLowPass(sample[0], int(r*scale*delays_r[i]+0.5), g, g1_list[i])
        combs_out_l = combs_out_l+combWithLowPass(sample[1], int(r*scale*delays_l[i]+0.5), g, g1_list[i])

    # Cascaded allpass filters
    n_ap = len(allpass_delay)
    for i in range(n_ap):
        reverb_r = allpass(combs_out_r, allpass_delay[i], int(r*allpass_g+0.5))
        reverb_l = allpass(combs_out_l, allpass_delay[i], int(r*allpass_g+0.5))

    reverb_out_r = np.concatenate((early_reflections_r, np.zeros(rev_to_er_delay)))+delay(reverb_r, rev_to_er_delay)
    reverb_out_l = np.concatenate((early_reflections_l, np.zeros(rev_to_er_delay)))+delay(reverb_l, rev_to_er_delay)

    reverb_out_r = reverb_out_r*wet1+reverb_out_l*wet2+np.concatenate((sample[0], np.zeros(rev_to_er_delay)))*dry_gain
    reverb_out_l = reverb_out_l*wet1+reverb_out_r*wet2+np.concatenate((sample[1], np.zeros(rev_to_er_delay)))*dry_gain

    signal_to_render = np.empty((reverb_out_r.size+reverb_out_l.size))
    signal_to_render[0::2] = reverb_out_r
    signal_to_render[1::2] = reverb_out_l

    sample_in = np.concatenate((sample_in, np.zeros(2*rev_to_er_delay)))

    return sample_in*dry_gain+signal_to_render*wet_gain

def convolutionReverb(sample_in, irsample, dry_gain, wet_gain):
    if len(sample_in)%2 != 0:
        sample_in = sample_in[:-1]
    if len(irsample)%2 != 0:
        irsample = irsample[:-1]
    sample = np.array([sample_in[0::2], sample_in[1::2]], dtype=np.float64)
    sample[0] /= np.max(np.abs(sample[0]), axis = 0)
    sample[1] /= np.max(np.abs(sample[1]), axis = 0)
    reverb = np.array([irsample[0::2], irsample[1::2]], dtype=np.float64)
    reverb[0] /= np.max(np.abs(reverb[0]), axis = 0)
    reverb[1] /= np.max(np.abs(reverb[1]), axis = 0)

    reverb_out = np.zeros([2, np.shape(sample)[1]+np.shape(reverb)[1]-1], dtype=np.float64)
    reverb_out[0] = signal.convolve(sample[0], reverb[0], method='fft')
    reverb_out[1] = signal.convolve(sample[1], reverb[1], method='fft')

    reverb_to_render = np.empty((reverb_out[0].size+reverb_out[1].size))
    reverb_to_render[0::2] = reverb_out[0]
    reverb_to_render[1::2] = reverb_out[1]

    sample_in = np.concatenate((sample_in, np.zeros(len(reverb_to_render)-len(sample_in))))

    return sample_in*dry_gain+reverb_to_render*wet_gain

def flanger(data, sample_rate, delays, widths, freqs, depths, dry_gain, fb_gain, lfos):
    nsamples = len(data)
    voices = len(delays)

    output = np.zeros(nsamples)
    n = np.arange(nsamples)
    for i in range(voices): # Chorus
        delay = delays[i]
        width = widths[i]
        freq = freqs[i]
        depth = depths[i]
        lfo = lfos[i]
        width = int(np.floor(sample_rate*width))
        delay = int(np.floor(sample_rate*delay))
        if delay < width:
            delay = width
        delay_buf_length = delay+2*width+3
        delay_data = np.zeros(delay_buf_length)

        if lfo == 0: # sin
            ph = np.sin(2*np.pi*((n*freq/sample_rate)%1))
        elif lfo == 1: # tri
            ph = np.abs(2*((n*freq/sample_rate)%1) - np.floor(2*((n*freq/sample_rate)%1)) - 0.5)
        elif lfo == 2: # saw
            ph = 2*n*freq/sample_rate - np.floor(2*((n*freq/sample_rate)%1)) - 0.5
        elif lfo == 3: # sqr
            ph = np.floor(2*((n*freq/sample_rate)%1))

        input = data
        dpw = 0
        for i in range(nsamples): # Vibrato
            interpolated_sample = 0.0

            current_delay = np.fmod(delay+0.5*width*(1+ph[i]), delay_buf_length) # LFO
            dpr = (dpw-current_delay+delay_buf_length-3.0)%delay_buf_length

            fraction = dpr - np.floor(dpr)
            previousSample = int(np.floor(dpr))
            nextSample = (previousSample+1)%delay_buf_length
            interpolated_sample = fraction*delay_data[nextSample]+(1.0-fraction)*delay_data[previousSample]

            delay_data[dpw] = input[i]+(interpolated_sample*fb_gain)
            dpw = (dpw+1)%delay_buf_length
            input[i] = depth*interpolated_sample

        output += input

    return output+data*dry_gain # Flanger


def update(self):
    ### Available Effects ###########

    # Reverberation

    r_room_size = self.dial_r_room_size.value() # %
    r_dry_wet = round(self.dial_r_dry_wet.value()/100, 2) # % -> 0-1
    r_damping = self.dial_r_damping.value() # %
    r_width = self.dial_r_width.value() # %
    r_pre_delay = round(self.dial_r_pre_delay.value()/1000, 3) # ms -> s
    r_reverberance = self.dial_r_reverberance.value() # %
    r_idg = round(self.dial_r_idg.value()/1000, 3) # ms -> s
    r_wet_gain = self.dial_r_wet_gain.value() # dB
    r_echoes = self.dial_r_echoes.value() # N
    r_delay = round(self.dial_r_delay.value()/1000, 3) # ms -> s

    r_type = self.comboBox_r_type.currentIndex()
    r_dataset = self.comboBox_r_dataset.currentIndex()
    r_preset = self.comboBox_r_preset.currentIndex()

    self.label_r_room_size.setText(str(r_room_size))
    self.label_r_delay.setText(str(round(r_delay*1000)))
    self.label_r_echoes.setText(str(r_echoes))
    self.label_r_damping.setText(str(r_damping))
    self.label_r_width.setText(str(r_width))
    self.label_r_pre_delay.setText(str(round(r_pre_delay*1000)))
    self.label_r_idg.setText(str(round(r_idg*1000)))
    self.label_r_wet_gain.setText(str(r_wet_gain))
    self.label_r_dry_wet.setText(str(round(r_dry_wet*100)))
    self.label_r_reverberance.setText(str(r_reverberance))

    # Delay Line

    dl_voices = self.horizontalSlider_dl_voices.value()
    dl_feedback = round(self.dial_dl_feedback.value()/100, 2) # % -> 0-1
    dl_dry_gain = self.dial_dl_dry_gain.value() # dB
    dl_lfo_freq = round(self.dial_dl_lfo_freq.value()/10, 1) # dHz -> Hz
    dl_lfo_width = round(self.dial_dl_lfo_width.value()/1000, 3) # ms -> s
    dl_lfo_delay = round(self.dial_dl_lfo_delay.value()/1000, 3) # ms -> s
    dl_lfo_depth = self.dial_dl_lfo_depth.value() # dB
    dl_lfo_freq_2 = round(self.dial_dl_lfo_freq_2.value()/10, 1) # dHz -> Hz
    dl_lfo_width_2 = round(self.dial_dl_lfo_width_2.value()/1000, 3) # ms -> s
    dl_lfo_delay_2 = round(self.dial_dl_lfo_delay_2.value()/1000, 3) # ms -> s
    dl_lfo_depth_2 = self.dial_dl_lfo_depth_2.value() # dB
    dl_lfo_freq_3 = round(self.dial_dl_lfo_freq_3.value()/10, 1) # dHz -> Hz
    dl_lfo_width_3 = round(self.dial_dl_lfo_width_3.value()/1000, 3) # ms -> s
    dl_lfo_delay_3 = round(self.dial_dl_lfo_delay_3.value()/1000, 3) # ms -> s
    dl_lfo_depth_3 = self.dial_dl_lfo_depth_3.value() # dB

    dl_lfo_type = self.comboBox_dl_lfo_type.currentIndex()
    dl_interpolation = self.comboBox_dl_interpolation.currentIndex()
    dl_lfo_type2 = self.comboBox_dl_lfo_type_2.currentIndex()
    dl_interpolation2 = self.comboBox_dl_interpolation_2.currentIndex()
    dl_lfo_type3 = self.comboBox_dl_lfo_type_3.currentIndex()
    dl_interpolation3 = self.comboBox_dl_interpolation_3.currentIndex()
    dl_type = self.comboBox_dl_type.currentIndex()

    self.label_dl_feedback.setText(str(round(dl_feedback*100)))
    self.label_dl_dry_gain.setText(str(dl_dry_gain))
    self.label_dl_lfo_freq.setText(str(dl_lfo_freq))
    self.label_dl_lfo_width.setText(str(round(dl_lfo_width*1000)))
    self.label_dl_lfo_delay.setText(str(round(dl_lfo_delay*1000)))
    self.label_dl_lfo_depth.setText(str(dl_lfo_depth))
    self.label_dl_lfo_freq_2.setText(str(dl_lfo_freq_2))
    self.label_dl_lfo_width_2.setText(str(round(dl_lfo_width_2*1000)))
    self.label_dl_lfo_delay_2.setText(str(round(dl_lfo_delay_2*1000)))
    self.label_dl_lfo_depth_2.setText(str(dl_lfo_depth_2))
    self.label_dl_lfo_freq_3.setText(str(dl_lfo_freq_3))
    self.label_dl_lfo_width_3.setText(str(round(dl_lfo_width_3*1000)))
    self.label_dl_lfo_delay_3.setText(str(round(dl_lfo_delay_3*1000)))
    self.label_dl_lfo_depth_3.setText(str(dl_lfo_depth_3))
    self.label_dl_voices.setText(str(dl_voices))

    ### Not yet implemented ##########

    # # Filtering

    # f_nfilters = self.spinBox_f_nfilters.value()
    # f_center_freq = self.dial_f_center_freq.value()
    # f_Q = self.dial_f_Q.value()
    # f_gain = self.dial_f_gain.value()
    # f_dry_wet = self.dial_f_dry_wet.value()
    # f_feedback = self.dial_f_feedback.value()
    # f_lfo_freq = self.dial_f_lfo_freq.value()
    # f_lfo_width = self.dial_f_lfo_width.value()
    # f_lfo_delay = self.dial_f_lfo_delay.value()

    # am_type = self.comboBox_am_lfo_type.currentIndex()
    # am_type = self.comboBox_am_lfo_interpolation.currentIndex()
    # f_type = self.comboBox_f_type.currentIndex()

    # # Amplitude Modulation

    # am_lfo_freq = self.dial_am_lfo_freq.value()
    # am_lfo_width = self.dial_am_lfo_width.value()
    # am_lfo_delay = self.dial_am_lfo_delay.value()

    # am_type = self.comboBox_am_lfo_type.currentIndex()
    # am_type = self.comboBox_am_lfo_interpolation.currentIndex()

    tab_effect = self.tabEffects.currentIndex()

    # TO-DO
    # delays in ms -> samples (doesn't work with fs != 44100)
    # presets
    # log dial
    # int() -> round()
    # reset button
    # stereo input and output
    # check if files are opened and closed correctly
    # conv to flanger
    # double gains if conv?
    # plots dl equal

    if self.comboBox_r_type.currentIndex() != 0:
        self.groupBox_r.setEnabled(True)
        self.groupBox_r_rir.setEnabled(False)
        self.dial_r_room_size.setEnabled(True)
        self.dial_r_dry_wet.setEnabled(True)
        self.dial_r_damping.setEnabled(True)
        self.dial_r_width.setEnabled(True)
        self.dial_r_pre_delay.setEnabled(True)
        self.dial_r_reverberance.setEnabled(True)
        self.dial_r_idg.setEnabled(True)
        self.dial_r_wet_gain.setEnabled(True)
        self.dial_r_echoes.setEnabled(True)
        self.dial_r_delay.setEnabled(True)
        self.checkBox_r_convolution.setEnabled(True)

    else:
        self.groupBox_r.setEnabled(False)
        self.groupBox_r_rir.setEnabled(False)
        self.checkBox_r_convolution.setEnabled(False)

    if self.comboBox_dl_type.currentIndex() != 0:
        self.tabWidget_dl_voices.setEnabled(True)
        self.horizontalSlider_dl_voices.setEnabled(False)
        self.dial_dl_feedback.setEnabled(True)
        self.dial_dl_dry_gain.setEnabled(True)
        self.tab_dl_voice_1.setEnabled(True)
        self.tab_dl_voice_2.setEnabled(False)
        self.tab_dl_voice_3.setEnabled(False)
        self.checkBox_dl_convolution.setEnabled(False)

    else:
        self.tabWidget_dl_voices.setEnabled(False)
        self.horizontalSlider_dl_voices.setEnabled(False)
        self.dial_dl_feedback.setEnabled(False)
        self.dial_dl_dry_gain.setEnabled(False)
        self.checkBox_dl_convolution.setEnabled(False)

    if tab_effect == 0:
        if r_type == 1:
            self.dial_r_room_size.setEnabled(False)
            self.dial_r_damping.setEnabled(False)
            self.dial_r_width.setEnabled(False)
            self.dial_r_pre_delay.setEnabled(False)
            self.dial_r_reverberance.setEnabled(False)
            self.dial_r_idg.setEnabled(False)

        elif r_type == 2:
            self.dial_r_room_size.setEnabled(False)
            self.dial_r_damping.setEnabled(False)
            self.dial_r_width.setEnabled(False)
            self.dial_r_pre_delay.setEnabled(False)
            self.dial_r_idg.setEnabled(False)
            self.dial_r_echoes.setEnabled(False)

        elif r_type == 3:
            self.dial_r_room_size.setEnabled(False)
            self.dial_r_width.setEnabled(False)
            self.dial_r_pre_delay.setEnabled(False)
            self.dial_r_idg.setEnabled(False)
            self.dial_r_echoes.setEnabled(False)

        elif r_type == 4:
            self.dial_r_room_size.setEnabled(False)
            self.dial_r_damping.setEnabled(False)
            self.dial_r_width.setEnabled(False)
            self.dial_r_pre_delay.setEnabled(False)
            self.dial_r_idg.setEnabled(False)
            self.dial_r_echoes.setEnabled(False)

        elif r_type == 5:
            self.dial_r_room_size.setEnabled(False)
            self.dial_r_damping.setEnabled(False)
            self.dial_r_width.setEnabled(False)
            self.dial_r_pre_delay.setEnabled(False)
            self.dial_r_reverberance.setEnabled(False)
            self.dial_r_idg.setEnabled(False)
            self.dial_r_echoes.setEnabled(False)
            self.dial_r_delay.setEnabled(False)

        elif r_type == 6:
            self.dial_r_room_size.setEnabled(False)
            self.dial_r_damping.setEnabled(False)
            self.dial_r_width.setEnabled(False)
            self.dial_r_pre_delay.setEnabled(False)
            self.dial_r_reverberance.setEnabled(False)
            self.dial_r_idg.setEnabled(False)
            self.dial_r_echoes.setEnabled(False)
            self.dial_r_delay.setEnabled(False)

        elif r_type == 7:
            self.dial_r_damping.setEnabled(False)
            self.dial_r_reverberance.setEnabled(False)
            self.dial_r_echoes.setEnabled(False)
            self.dial_r_delay.setEnabled(False)

        elif r_type == 8:
            self.dial_r_echoes.setEnabled(False)
            self.dial_r_delay.setEnabled(False)

        elif r_type == 9:
            self.dial_r_room_size.setEnabled(False)
            self.dial_r_damping.setEnabled(False)
            self.dial_r_width.setEnabled(False)
            self.dial_r_pre_delay.setEnabled(False)
            self.dial_r_reverberance.setEnabled(False)
            self.dial_r_idg.setEnabled(False)
            self.dial_r_echoes.setEnabled(False)
            self.dial_r_delay.setEnabled(False)
            self.checkBox_r_convolution.setEnabled(False)
            self.checkBox_r_convolution.setChecked(False)
            self.groupBox_r_rir.setEnabled(True)

            if r_dataset != self.prev_r_dataset:
                self.comboBox_r_preset.setCurrentIndex(0)
                self.prev_r_dataset = r_dataset

            if r_dataset == 0:
                self.comboBox_r_preset.setEnabled(False)
            else:
                self.comboBox_r_preset.setEnabled(True)
                view = self.comboBox_r_preset.view()
                for i in range(1, 48):
                    view.setRowHidden(i, True)

                if r_dataset == 1:
                    for i in range(1, 10):
                        view.setRowHidden(i, False)

                elif r_dataset == 2:
                    for i in range(10, 24):
                        view.setRowHidden(i, False)

                elif r_dataset == 3:
                    for i in range(24, 39):
                        view.setRowHidden(i, False)

                elif r_dataset == 4:
                    for i in range(39, 49):
                        view.setRowHidden(i, False)

    elif tab_effect == 1:
        if dl_type == 1:
            self.horizontalSlider_dl_voices.setEnabled(False)
            self.dial_dl_feedback.setEnabled(False)
            self.dial_dl_dry_gain.setEnabled(False)

        elif dl_type == 2:
            self.horizontalSlider_dl_voices.setEnabled(False)
            self.dial_dl_feedback.setEnabled(True)
            self.dial_dl_dry_gain.setEnabled(True)

        elif dl_type == 3:
            self.horizontalSlider_dl_voices.setEnabled(True)
            self.dial_dl_feedback.setEnabled(True)
            self.dial_dl_dry_gain.setEnabled(True)
            if dl_voices > 1:
                self.tab_dl_voice_2.setEnabled(True)
            if dl_voices > 2:
                self.tab_dl_voice_3.setEnabled(True)

    if (len(self.input_file_data) == 0 and self.comboBox_tracks.currentIndex() == 0) \
    or tab_effect >= 2 \
    or (tab_effect == 0 and r_type == 0) \
    or (tab_effect == 1 and dl_type == 0) \
    or (tab_effect == 0 and r_type == 9 and r_preset == 0):
        self.label_status.setText('Waiting...')
    else:
        self.label_status.setText('Ready.')

def importWAVFile(self):
    filename = QFileDialog.getOpenFileName(self, 'Open File', 'c:\\', 'Audio File (*.wav)')
    name = str(filename[0])
    if name:
        self.input_file_data, sr = sf.read(name)
        msg = 'Successfully opened input file '+name
        if len(msg) > 70:
            msg = msg[:70]+'..'
        self.label_status.setText(msg+'.')

def exportWAVFile(self, data):
    filename = QFileDialog.getSaveFileName(self, 'Save Fiile', 'c:\\', 'Audio File (*.wav)')
    name = str(filename[0])
    if name:
        sf.write(name, data, 44100, 'PCM_24')
        msg = 'Audio was successfully exported to '+name
        if len(msg) > 70:
            msg = msg[:70]+'..'
        self.label_status.setText(msg+'.')

def reset(self):
    self.input_file_data = []
    self.track_data.track_1_effects = []
    self.track_data.track_2_effects = []
    self.track_data.track_3_effects = []
    self.track_data.track_4_effects = []
    self.label_status.setText('Waiting...')

def apply(self):
    self.label_status.setText('Working...') # No sirve son threads

    r_room_size = self.dial_r_room_size.value() # %
    r_dry_wet = self.dial_r_dry_wet.value()/100 # % -> 0-1
    r_damping = self.dial_r_damping.value() # %
    r_width = self.dial_r_width.value() # %
    r_pre_delay = self.dial_r_pre_delay.value()/1000 # ms -> s
    r_reverberance = self.dial_r_reverberance.value() # %
    r_idg = self.dial_r_idg.value()/1000 # ms -> s
    r_wet_gain = self.dial_r_wet_gain.value() # dB
    r_echoes = self.dial_r_echoes.value() # N
    r_delay = self.dial_r_delay.value()/1000 # ms -> s

    r_type = self.comboBox_r_type.currentIndex()
    r_dataset = self.comboBox_r_dataset.currentIndex()
    r_preset = self.comboBox_r_preset.currentIndex()

    dl_voices = self.horizontalSlider_dl_voices.value()
    dl_feedback = self.dial_dl_feedback.value()/100 # % -> 0-1
    dl_dry_gain = self.dial_dl_dry_gain.value() # dB
    dl_lfo_freq = self.dial_dl_lfo_freq.value()/10 # dHz -> Hz
    dl_lfo_width = self.dial_dl_lfo_width.value()/1000 # ms -> s
    dl_lfo_delay = self.dial_dl_lfo_delay.value()/1000 # ms -> s
    dl_lfo_depth = self.dial_dl_lfo_depth.value() # dB
    dl_lfo_freq_2 = self.dial_dl_lfo_freq_2.value()/10 # dHz -> Hz
    dl_lfo_width_2 = self.dial_dl_lfo_width_2.value()/1000 # ms -> s
    dl_lfo_delay_2 = self.dial_dl_lfo_delay_2.value()/1000 # ms -> s
    dl_lfo_depth_2 = self.dial_dl_lfo_depth_2.value() # dB
    dl_lfo_freq_3 = self.dial_dl_lfo_freq_3.value()/10 # dHz -> Hz
    dl_lfo_width_3 = self.dial_dl_lfo_width_3.value()/1000 # ms -> s
    dl_lfo_delay_3 = self.dial_dl_lfo_delay_3.value()/1000 # ms -> s
    dl_lfo_depth_3 = self.dial_dl_lfo_depth_3.value() # dB

    dl_lfo_type = self.comboBox_dl_lfo_type.currentIndex()
    dl_interpolation = self.comboBox_dl_interpolation.currentIndex()
    dl_lfo_type_2 = self.comboBox_dl_lfo_type_2.currentIndex()
    dl_interpolation2 = self.comboBox_dl_interpolation_2.currentIndex()
    dl_lfo_type_3 = self.comboBox_dl_lfo_type_3.currentIndex()
    dl_interpolation3 = self.comboBox_dl_interpolation_3.currentIndex()
    dl_type = self.comboBox_dl_type.currentIndex()

    tab_effect = self.tabEffects.currentIndex()
    track_samples_in = [self.track_data.track_1_samples,
                        self.track_data.track_2_samples,
                        self.track_data.track_3_samples,
                        self.track_data.track_4_samples]
    index = self.comboBox_tracks.currentIndex()

    if tab_effect >= 2 \
    or (tab_effect == 0 and r_type == 0) \
    or (tab_effect == 1 and dl_type == 0) \
    or (tab_effect == 0 and r_type == 9 and r_preset == 0):
        err = 'Please finish configuring the effect before applying it to the audio.'
        self.label_status.setText(err)
        print(err)
        return -1
    elif len(self.input_file_data) == 0 and index == 0:
        err = 'Please select a track or open a WAV file before applying the effect.'
        self.label_status.setText(err)
        print(err)
        return -1
    elif len(self.input_file_data) == 0 and index != 0 and len(track_samples_in[index-1]) == 0:
        err = 'Selected track was not ready. Please synthesize first.'
        self.label_status.setText(err)
        print(err)
        return -1

    # Control

    room_scale = r_room_size
    pre_delay = r_pre_delay
    wet_gain = 10**(r_wet_gain/20)
    dry_gain = wet_gain*r_dry_wet
    hf_damping = r_damping
    reverberance = r_reverberance
    stereo_width = r_width
    fs = 44100
    a = -1/np.log(0.7)
    b = 100/(np.log(0.02)*a+1)
    dl_lfo_depth, dl_lfo_depth_2, dl_lfo_depth_3 = 10**(dl_lfo_depth/20), 10**(dl_lfo_depth_2/20), 10**(dl_lfo_depth_3/20)
    dl_dry_gain = 10**(dl_dry_gain/20)

    ### Apply Effects ################

    x = y = []
    if len(self.input_file_data) != 0:
        x = self.input_file_data
    else:
        if index == 1:
            x = self.track_data.track_1_samples
        elif index == 2:
            x = self.track_data.track_2_samples
        elif index == 3:
            x = self.track_data.track_3_samples
        elif index == 4:
            x = self.track_data.track_4_samples

    if np.ndim(x)>1:
        x = np.mean(x, axis=1)
    if (self.checkBox_r_convolution.isChecked() and tab_effect == 0) or (self.checkBox_dl_convolution.isChecked() and tab_effect == 1):
        x_in = x
        x = np.zeros(2*fs)
        x[0:2] = 1

    if tab_effect == 0:
        if r_type == 1:
            y = echo(x, r_echoes, int(r_delay*fs), dry_gain, wet_gain)

        elif r_type == 2:
            gain = 1-np.exp((reverberance-b)/(a*b))
            y = simpleReverb(x, [gain], [int(r_delay*fs)], dry_gain, wet_gain)

        elif r_type == 3:
            gain = 1-np.exp((reverberance-b)/(a*b))
            lp_gain = (hf_damping/100)*0.3+0.2
            y = lowPassReverb(x, [gain], [lp_gain], [int(r_delay*fs)], dry_gain, wet_gain)

        elif r_type == 4:
            gain = 1-np.exp((reverberance-b)/(a*b))
            y = allPassReverb(x, [gain], [int(r_delay*fs)], dry_gain, wet_gain)

        elif r_type == 5:
            y = schroederReverb(x, satrev_comb_delays, satrev_all_pass_delay,
                                satrev_comb_gains, satrev_all_pass_gains, dry_gain, wet_gain)

        elif r_type == 6:
            y = schroederReverb(x, jcrev_comb_delays, jcrev_all_pass_delay,
                                jcrev_comb_gains, jcrev_all_pass_gains, dry_gain, wet_gain)

        elif r_type == 7:
            y = moorerFreeverbReverb(x, moorer_delays_early, moorer_gains_early,
                                     moorer_rev_to_er_delay, [moorer_allpass_delay],
                                     moorer_allpass_g, dry_gain, wet_gain, hf_damping,
                                     stereo_width, room_scale, pre_delay, moorer_delays_r,
                                     moorer_g, moorer_g1_list, reverberance, 2, fs)

        elif r_type == 8:
            y = moorerFreeverbReverb(x, freeverb_delays_early, freeverb_gains_early,
                                     int(r_idg*fs), freeverb_allpass_delays, 0.84, dry_gain,
                                     wet_gain, hf_damping, stereo_width, room_scale, pre_delay,
                                     freeverb_comb_delays, None, None, reverberance, 2, fs)

        elif r_type == 9:
            y, sr = sf.read(irsamples[r_preset-1])
            if np.ndim(y)>1:
                y = np.mean(y, axis=1)
            x_in = x
            output = convolutionReverb(x_in, y, dry_gain, wet_gain)

        if self.checkBox_r_convolution.isChecked():
            output = convolutionReverb(x_in, y, 0, 1)

    elif tab_effect == 1:
        if dl_type == 1:
            y = flanger(x, fs, [dl_lfo_delay], [dl_lfo_width],
                        [dl_lfo_freq], [dl_lfo_depth], 0, 0, [dl_lfo_type])

        elif dl_type == 2:
            y = flanger(x, fs, [dl_lfo_delay], [dl_lfo_width],
                        [dl_lfo_freq], [dl_lfo_depth], dl_dry_gain,
                        dl_feedback, [dl_lfo_type])

        elif dl_type == 3:
            dl_lfo_delay = [dl_lfo_delay]
            dl_lfo_width = [dl_lfo_width]
            dl_lfo_freq = [dl_lfo_freq]
            dl_lfo_depth = [dl_lfo_depth]
            dl_lfo_type = [dl_lfo_type]

            if dl_voices >= 2:
                dl_lfo_delay.append(dl_lfo_delay_2)
                dl_lfo_width.append(dl_lfo_width_2)
                dl_lfo_freq.append(dl_lfo_freq_2)
                dl_lfo_depth.append(dl_lfo_depth_2)
                dl_lfo_type.append(dl_lfo_type_2)

            if dl_voices >= 3:
                dl_lfo_delay.append(dl_lfo_delay_3)
                dl_lfo_width.append(dl_lfo_width_3)
                dl_lfo_freq.append(dl_lfo_freq_3)
                dl_lfo_depth.append(dl_lfo_depth_3)
                dl_lfo_type.append(dl_lfo_type_3)

            y = flanger(x, fs, dl_lfo_delay, dl_lfo_width, dl_lfo_freq, dl_lfo_depth,
                        dl_dry_gain, dl_feedback, dl_lfo_type)

        if self.checkBox_dl_convolution.isChecked():
            output = convolutionReverb(x_in, y, 0, 1)

    rows = 2
    if ((self.checkBox_r_convolution.isChecked() or r_type == 9) and tab_effect == 0) or (self.checkBox_dl_convolution.isChecked() and tab_effect == 1):
        rows = 3

    if self.radioButton_plot.isChecked():
        fig = plt.figure()

        if rows == 2:
            ax1 = plt.subplot2grid((2, 2), (0, 0), fig=fig)
            ax2 = plt.subplot2grid((2, 2), (1, 0), fig=fig, sharex=ax1)
            ax3 = plt.subplot2grid((2, 2), (0, 1), rowspan=2, fig=fig)
            ax = [ax1, ax2]
            # max_t = max(len(x), len(y))
            # t = np.linspace(0, max_t, max_t)
            # x = np.concatenate((x, np.zeros(max_t-len(x))))
            # y = np.concatenate((y, np.zeros(max_t-len(y))))
            t1 = np.linspace(0, len(x), len(x))
            t2 = np.linspace(0, len(y), len(y))
            ax[0].plot(t1/fs, x)
            ax[0].set_title('Input')
            ax[0].set_ylabel('Amplitude')
            ax[1].plot(t2/fs, y)
            ax[1].set_title('Output')
            ax[1].set_ylabel('Amplitude')
            ax[1].set_xlabel('Time')
            # fig.subplots_adjust(hspace=0)
            # plt.setp([a.get_xticklabels() for a in ax[:-1]], visible=False)
            pxx, freqs, bins, im = ax3.specgram(y, Fs=fs)
            ax3.set_xlabel('Time [s]')
            ax3.set_ylabel('Frequency [Hz]')
            fig.colorbar(im, ax=ax3, label="Magnitude $|S_y(t, f)|$")
            for axn in ax:
                axn.grid()
        
        else:
            ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=2, fig=fig)
            ax2 = plt.subplot2grid((3, 3), (1, 0), fig=fig)
            ax2_2 = plt.subplot2grid((3, 3), (1, 1), fig=fig)
            ax3 = plt.subplot2grid((3, 3), (2, 0), colspan=2, fig=fig, sharex=ax1)
            ax5 = plt.subplot2grid((3, 3), (0, 2), rowspan=3, fig=fig)
            ax = [ax1, ax2, ax2_2, ax3]
            # max_t = max(len(x_in), len(y), len(output))
            # t = np.linspace(0, max_t, max_t)
            # x_in = np.concatenate((x_in, np.zeros(max_t-len(x_in))))
            # y = np.concatenate((y, np.zeros(max_t-len(y))))
            # output = np.concatenate((output, np.zeros(max_t-len(output))))
            t1 = np.linspace(0, len(x_in), len(x_in))
            t2 = np.linspace(0, len(y), len(y))
            t3 = np.linspace(0, len(output), len(output))
            ax[0].plot(t1/fs, x_in)
            ax[0].set_title('Input')
            ax[0].set_ylabel('Amplitude')
            ax[1].plot(t2/fs, y)
            ax[1].set_title('Effect Impulse Response')
            ax[1].set_xlabel('Time [s]')
            ax[1].set_ylabel('Amplitude')
            ax[3].plot(t3/fs, output)
            ax[3].set_title('Output')
            ax[3].set_ylabel('Amplitude')
            ax[3].set_xlabel('Time [s]')
            # fig.subplots_adjust(hspace=0)
            # plt.setp([a.get_xticklabels() for a in ax[:-1]], visible=False)
            sp = fftshift(fft(y))
            freq = fftshift(fftfreq(y.shape[-1], d=1/fs))
            ax[2].plot(freq, 20*np.log(abs(sp)))
            ax[2].set_xlabel('Frequency [Hz]')
            ax[2].set_title('Effect Frequency Response')
            ax[2].set_ylabel('Magnitude [dB]')
            ax[2].set_ylim(-100, 100)
            ax4 = ax[2].twinx()
            ax4.plot(freq, np.unwrap(np.angle(sp)), color='g')
            ax4.set_ylabel('Phase [°]')
            pxx, freqs, bins, im = ax5.specgram(output, Fs=fs)
            ax5.set_xlabel('Time [s]')
            ax5.set_ylabel('Frequency [Hz]')
            fig.colorbar(im, ax=ax5, label="Magnitude $|S_y(t, f)|$")
            for axn in ax:
                axn.grid()

        plt.subplots_adjust(wspace=0.5, hspace=0.5)
        plt.margins(0)
        # plt.tight_layout()
        plt.show()

    if rows == 3:
        y = output
    max_output = max(np.abs(y))
    if (max_output != 0):
        output = 0.5*y/max_output # Max level of output audio. Adjust as needed.
        if len(self.input_file_data) != 0:
            self.label_status.setText('Exporting to WAV...')
            exportWAVFile(self, output)
        else:
            if index == 1:
                self.track_data.track_1_effects = output
            elif index == 2:
                self.track_data.track_2_effects = output
            elif index == 3:
                self.track_data.track_3_effects = output
            elif index == 4:
                self.track_data.track_4_effects = output
            self.label_status.setText('Effect applied successfully.')
    else:
        err = 'An error has occurred. Output is empty'
        self.label_status.setText(err)
        print(err)
