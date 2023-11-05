import grabar
import CortarGrabacion

# Para grabar audio
duracion_grabacion = float(input("Ingresa la duración de la grabación en segundos: "))
nombre_archivo = input("Ingresa el nombre del archivo de salida (sin la extensión .wav): ")
grabar.grabar_audio(duracion_grabacion, nombre_archivo)

# Para dividir audio5
nombre_archivo_audio = nombre_archivo + ".wav"
CortarGrabacion.dividir_audio(nombre_archivo_audio)


