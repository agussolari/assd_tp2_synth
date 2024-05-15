#SINTESIS DE UN PIANO BASADO EN MUESTRAS

import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt

#Función que carga muestras de sonido estéreo elegidas por el usuario
def cargar_muestras(ruta_banco):
    muestras = {} # Diccionario para almacenar las muestras de sonido
    notas_elegidas = ["C1", "G1", "D2", "A2", "E3", "B3", "F4", "C5", "G5", "D6", "A6", "E7", "B7"]
    for nota in notas_elegidas: 
        archivo = f"{ruta_banco}/{nota}.wav"
        data, fs = librosa.load(archivo, sr=44100, mono=True)  
        muestras[nota] = data.astype(np.float32) # Almacenar la muestra de sonido en el diccionario, la clave es la nota
    return muestras

path_banco_muestras = "src/Piano2"
banco_muestras = cargar_muestras(path_banco_muestras)
#Función de búsqueda binaria para encontrar la muestra más cercana en el banco de muestras
def binary_search(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        # Si el elemento medio es el objetivo, se ha encontrado
        if abs(arr[mid] - target) <= 3:
            return mid
        # Si el objetivo es menor que el elemento medio, se busca en la mitad izquierda
        elif arr[mid] > target:
            right = mid - 1
        # Si el objetivo es mayor que el elemento medio, se busca en la mitad derecha
        else:
            left = mid + 1

    # Si el elemento  no está presente en la lista
    return -1



#Función que devuelve la muestra más cercana en el banco de muestras a la nota dada usando la busqueda binaria

def encontrar_muestra_cercana(nota_midi, banco_muestras):
    notas_banco = [librosa.note_to_midi(nota) for nota in banco_muestras.keys()]
    indice = binary_search(notas_banco, nota_midi)
    if indice != -1:
        nota_cercana = list(banco_muestras.keys())[indice]
        #Imprimir la nota ingresada y la nota encontrada
        #print(f"Nota ingresada: {librosa.midi_to_note(nota_midi)}, {nota_midi}")
        #xprint(f"Nota encontrada: {nota_cercana}, {librosa.note_to_midi(nota_cercana)}")
        dif_bins = nota_midi - librosa.note_to_midi(nota_cercana)
        return banco_muestras[nota_cercana], dif_bins
    else:
        return np.zeros(1), 0


#Función para ajustar la altura tonal del audio según la diferencia de bins
def ajustar_altura_audio(audio, diferencia_bins, vel=1.0, dur=1.0):
    # Aplicar el cambio de tono al audio
    audio_ajustado = librosa.effects.pitch_shift(audio, sr=44100, n_steps=diferencia_bins, scale=False)
    
    #obtengo el tiempo que dura la nota
    t = len(audio_ajustado) / 44100
    
    #timestretch
    audio_ajustado = librosa.effects.time_stretch(audio_ajustado, rate=t/dur) #si rate > 1, se acelera, si rate < 1, se desacelera

    audio_ajustado = (vel / 127.0) *audio_ajustado  # Normalizando la velocidad al rango de 0 a 1

    #pasar el audio por un filtro pasabajos para limpiar el ruido metido por el ajuste:

    # Diseñar un filtro pasabajos Butterworth
    orden = 4  # Orden del filtro
    frecuencia_corte = 7000  # Frecuencia de corte en Hz
    frecuencia_normalizada = frecuencia_corte / (44100 / 2)  # Normalizar la frecuencia de corte

    # Convertir los coeficientes del filtro a secciones de segundo orden (SOS)
    sos = butter(orden, frecuencia_normalizada, btype='low', output='sos', analog=False)  # Coeficientes SOS del filtro

    # Aplicar el filtro a los datos utilizando sosfiltfilt
    audio_ajustado = sosfiltfilt(sos, audio_ajustado)
    #plt.plot(audio_ajustado)
    #plt.show()
    return audio_ajustado



#Función que engloba todo el proceso de sintesis y devuelve el arreglo modificado solo recibiendo la nota midi, velocidad y duración
def synth_piano(nota_midi, vel, dur):
    """Sintesis de un piano basado en muestras.

    Recibe nota_midi (int), vel(de 0 a 127 int) y la duración en segundos de la nota.
    
    Devuelve un arreglo de las muestras de dicha nota sintetizada.
    """
    muestra_modificar, dif_bins = encontrar_muestra_cercana(nota_midi, banco_muestras)
    audio_ajustado = ajustar_altura_audio(muestra_modificar, dif_bins, vel, dur)
    return audio_ajustado
