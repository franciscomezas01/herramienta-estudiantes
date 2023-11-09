import os
from paqueteGrabacion import grabar
from paqueteGrabacion import CortarGrabacion
from paqueteResumen import AudioTexto
import speech_recognition as sr

def obtener_texto_por_voz(mensaje):
    recognizer = sr.Recognizer()

    print(mensaje)
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        return texto
    except sr.UnknownValueError:
        print("No se pudo entender. Inténtalo de nuevo.")
        return obtener_texto_por_voz(mensaje)
    except sr.RequestError:
        print("Error al conectar con el servicio de reconocimiento de voz.")
        return None

# Obtener el nombre de la carpeta mediante comandos de voz
mensaje_nombre_carpeta = "Por favor, di el nombre de la carpeta."
nombre_carpeta = obtener_texto_por_voz(mensaje_nombre_carpeta)
while nombre_carpeta is None:
    nombre_carpeta = obtener_texto_por_voz(mensaje_nombre_carpeta)

# Crear la carpeta en el escritorio
ruta_carpeta = os.path.join(os.path.expanduser("~"), "Desktop", nombre_carpeta)
if not os.path.exists(ruta_carpeta):
    os.mkdir(ruta_carpeta)
    print(f"Se ha creado la carpeta en el escritorio: {nombre_carpeta}")
else:
    print(f"La carpeta {nombre_carpeta} ya existe en el escritorio.")

# Obtener la duración mediante comandos de voz
mensaje_duracion = "Por favor, di la duración de la grabación en segundos."
duracion_grabacion = obtener_texto_por_voz(mensaje_duracion)
while duracion_grabacion is None:
    duracion_grabacion = obtener_texto_por_voz(mensaje_duracion)

duracion_grabacion = float(duracion_grabacion)

nombre_archivo = nombre_carpeta
grabar.grabar_audio(duracion_grabacion, nombre_carpeta, nombre_archivo)

# Para dividir audio
nombre_archivo_audio = nombre_archivo + ".wav"
CortarGrabacion.dividir_audio(nombre_archivo_audio, ruta_carpeta)

# Convertir audio a texto y guardar en archivos .txt y .docx
ruta_archivo_txt, ruta_archivo_docx = AudioTexto.convertir_audio_a_texto(ruta_carpeta, nombre_archivo)

print(f"Texto convertido y guardado en {ruta_archivo_txt} y {ruta_archivo_docx}")
