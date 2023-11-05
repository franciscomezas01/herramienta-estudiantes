import os
import speech_recognition as sr
from docx import Document

def convertir_audio_a_texto(nombre_carpeta, nombre_archivo_audio):
    # Crear la ruta completa al archivo de audio en la misma carpeta
    ruta_archivo_audio = os.path.join(nombre_carpeta, f"{nombre_archivo_audio}.wav")

    recognizer = sr.Recognizer()

    # Cargar el archivo de audio
    with sr.AudioFile(ruta_archivo_audio) as source:
        audio = recognizer.record(source)

    # Realizar la conversión de audio a texto
    try:
        texto = recognizer.recognize_google(audio, language="es-ES")  # Cambia el idioma si es necesario
    except sr.UnknownValueError:
        texto = "No se pudo reconocer ningún texto en el audio."
    except sr.RequestError:
        texto = "No se pudo procesar la solicitud de reconocimiento de voz."

    # Guardar el texto en un archivo de texto (.txt)
    ruta_archivo_txt = os.path.join(nombre_carpeta, f"{nombre_archivo_audio}.txt")
    with open(ruta_archivo_txt, "w") as txt_file:
        txt_file.write(texto)

    # Guardar el texto en un archivo de Microsoft Word (.docx)
    ruta_archivo_docx = os.path.join(nombre_carpeta, f"{nombre_archivo_audio}.docx")
    doc = Document()
    doc.add_paragraph(texto)
    doc.save(ruta_archivo_docx)

    return ruta_archivo_txt, ruta_archivo_docx

if __name__ == "__main__":
    nombre_carpeta = input("Ingresa el nombre de la carpeta: ")
    nombre_archivo_audio = input("Ingresa el nombre del archivo de audio (sin la extensión .wav): ")

    ruta_archivo_txt, ruta_archivo_docx = convertir_audio_a_texto(nombre_carpeta, nombre_archivo_audio)

    print(f"Texto convertido y guardado en {ruta_archivo_txt} y {ruta_archivo_docx}")
