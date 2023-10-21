import os
import pyaudio
import wave

# Configuraciin de la grabacion
FORMATO = pyaudio.paInt16  # Formato de audio
CANALES = 1  # 1 canal de audio (mono)
TASA_MUESTREO = 44100  # Tasa de muestreo en Hz (muestras por segundo)
TAMANO_BUFFER = 1024

# Pedir al usuario la duracion de la grabacion en segundos
while True:
    try:
        DURACION_GRABACION = float(input("Ingresa la duracion de la grabacion en segundos: "))
        break
    except ValueError:
        print("Ingresa un numero valido.")

# Pedir al usuario el nombre del archivo de salida
NOMBRE_ARCHIVO = input("Ingresa el nombre del archivo de salida (sin la extension .wav): ") + ".wav"

# Obtener la ruta al escritorio en un sistema Windows
ruta_escritorio = os.path.join(os.path.expanduser("~"), "Desktop")

# Definir la ubicacion del archivo de salida en el escritorio
RUTA_ARCHIVO = os.path.join(ruta_escritorio, NOMBRE_ARCHIVO)

# Inicializar PyAudio
audio = pyaudio.PyAudio()

# Abrir un flujo de audio
stream = audio.open(format=FORMATO, channels=CANALES,
                    rate=TASA_MUESTREO, input=True,
                    frames_per_buffer=TAMANO_BUFFER)

print(f"Grabando durante {DURACION_GRABACION} segundos...")

frames = []

# Capturar datos de audio en tiempo real
for i in range(0, int(TASA_MUESTREO / TAMANO_BUFFER * DURACION_GRABACION)):
    data = stream.read(TAMANO_BUFFER)
    frames.append(data)

print("Grabacion finalizada.")

# Detener y cerrar el flujo de audio
stream.stop_stream()
stream.close()
audio.terminate()

# Guardar la grabacion en un archivo WAV en el escritorio
wf = wave.open(RUTA_ARCHIVO, 'wb')
wf.setnchannels(CANALES)
wf.setsampwidth(audio.get_sample_size(FORMATO))
wf.setframerate(TASA_MUESTREO)
wf.writeframes(b''.join(frames))
wf.close()

print(f"La grabacion se ha guardado en {RUTA_ARCHIVO}")
