import os
from paqueteGrabacion import grabar
from paqueteGrabacion import CortarGrabacion

# Pedir al usuario el nombre de la carpeta en el escritorio
nombre_carpeta = input("Ingresa el nombre de la carpeta en el escritorio: ")

# Crear la carpeta en el escritorio
ruta_carpeta = os.path.join(os.path.expanduser("~"), "Desktop", nombre_carpeta)
if not os.path.exists(ruta_carpeta):
    os.mkdir(ruta_carpeta)
    print(f"Se ha creado la carpeta en el escritorio: {nombre_carpeta}")
else:
    print(f"La carpeta {nombre_carpeta} ya existe en el escritorio.")

# Para grabar audio
duracion_grabacion = float(input("Ingresa la duración de la grabación en segundos: "))
nombre_archivo = nombre_carpeta
grabar.grabar_audio(duracion_grabacion, nombre_carpeta, nombre_archivo)

# Para dividir audio
nombre_archivo_audio = nombre_archivo +  ".wav"
CortarGrabacion.dividir_audio(nombre_archivo_audio, ruta_carpeta)



