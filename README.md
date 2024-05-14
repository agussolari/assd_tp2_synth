# Programa de Síntesis de Pistas MIDI

Este programa tiene como objetivo sintetizar pistas de audio a partir de archivos MIDI (.mid), permitiendo asignar instrumentos a cada pista, mezclar los distintos tracks, agregar efectos y guardar la pista generada en diferentes formatos de audio.



## Funcionalidades

- **Cargar Archivo MIDI:** Permite cargar un archivo en formato MIDI para su procesamiento.
- **Asignar Instrumentos:** Asigna cualquier instrumento a cada pista del archivo MIDI cargado.
- **Mezclar Tracks:** Combina los distintos tracks para generar una pista única.
- **Agregar Efectos:** Permite agregar y configurar diferentes efectos tanto para cada track como para la mezcla total, incluyendo delay y reverberación.
- **Guardar Pista Generada:** Guarda la pista generada en un formato de audio como wav, mp3, entre otros.
- **Visualización del Espectrograma:** Muestra el espectrograma del audio generado para su análisis.
- **Reproducción de Notas y Acordes:** Permite reproducir cualquier nota del instrumento o acordes con cualquier duración.

## Prestaciones Implementadas

- **Síntesis Aditiva o FM:** Se ha implementado la síntesis aditiva para la creación de un instrumento.
- **Síntesis por Modelado Físico:** Se ha implementado la síntesis por modelado físico para recrear características específicas de algunos instrumentos.
- **Síntesis por Muestras:** Se ha implementado la síntesis por muestras para generar sonidos realistas basados en muestras pregrabadas.
- **Delay y Reverberación:** Se han incorporado efectos de delay y reverberación para enriquecer el sonido final.

## Instalación

Para instalar este proyecto, sigue estos pasos:

1. Clona el repositorio: `git clone https://github.com/AgusSolari/assd_tp2_synth`
2. Navega al directorio del proyecto
3. Instala las dependencias: `pip install -r requirements.txt`


## Instrucciones de Uso

1. **Cargar Archivo MIDI:** Selecciona el archivo MIDI que deseas procesar.
2. **Asignar Instrumentos:** Asigna los instrumentos deseados a cada pista del archivo MIDI.
3. **Agregar Efectos:** Configura los efectos deseados para cada pista y para la mezcla total.
4. **Generar Pista:** Procesa la pista de audio con las configuraciones establecidas.
5. **Guardar Pista:** Guarda la pista generada en el formato de audio preferido.
6. **Visualizar Espectrograma:** Analiza el espectrograma del audio generado para evaluar su calidad.

## Ensayo con "Concierto de Aranjuez"

Para demostrar la funcionalidad del programa, se recomienda ensayar con un fragmento considerable del segundo movimiento (Adagio) del Concierto de Aranjuez, de Joaquín Rodrigo. Puedes encontrar archivos MIDI de esta obra en la web.

---

¡Esperamos que disfrutes utilizando nuestro programa para sintetizar tus pistas MIDI favoritas! Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto con nosotros.

*(Nota: Se incluirá el archivo .wav generado como parte de la entrega)*
