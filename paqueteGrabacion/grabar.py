import os
import pyaudio
import wave

def grabar_audio(duracion_grabacion, nombre_carpeta, nombre_archivo):
    FORMATO = pyaudio.paInt16
    CANALES = 1
    TASA_MUESTREO = 44100
    TAMANO_BUFFER = 1024

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMATO, channels=CANALES,
                        rate=TASA_MUESTREO, input=True,
                        frames_per_buffer=TAMANO_BUFFER)

    print(f"Grabando durante {duracion_grabacion} segundos...")
    frames = []

    for i in range(0, int(TASA_MUESTREO / TAMANO_BUFFER * duracion_grabacion)):
        data = stream.read(TAMANO_BUFFER)
        frames.append(data)

    print("Grabación finalizada.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Crear la ruta completa al archivo de grabación
    ruta_carpeta = os.path.join(os.path.expanduser("~"), "Desktop", nombre_carpeta)
    ruta_archivo = os.path.join(ruta_carpeta, f"{nombre_archivo}.wav")

    # Crear la carpeta si no existe
    if not os.path.exists(ruta_carpeta):
        os.mkdir(ruta_carpeta)

    # Guardar la grabación en la carpeta personalizada
    wf = wave.open(ruta_archivo, 'wb')
    wf.setnchannels(CANALES)
    wf.setsampwidth(audio.get_sample_size(FORMATO))
    wf.setframerate(TASA_MUESTREO)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"La grabación se ha guardado en {ruta_archivo}")

if __name__ == "__main__":
    nombre_carpeta = input("Ingresa el nombre de la carpeta en el escritorio: ")
    duracion_grabacion = float(input("Ingresa la duración de la grabación en segundos: "))
    nombre_archivo = input("Ingresa el nombre del archivo de salida (sin la extensión .wav): ")
    grabar_audio(duracion_grabacion, nombre_carpeta, nombre_archivo)
