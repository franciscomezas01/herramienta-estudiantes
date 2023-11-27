import os
import tkinter as tk
import speech_recognition as sr
from pydub import AudioSegment
import wave
from machine import Pin
import time
import keyboard
from docx import Document
import pyaudio 

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

def crear_carpeta(nombre_carpeta):
    ruta_carpeta = os.path.join(os.path.expanduser("~"), "Desktop", nombre_carpeta)
    
    if not os.path.exists(ruta_carpeta):
        os.mkdir(ruta_carpeta)
        print(f"Se ha creado la carpeta en el escritorio: {nombre_carpeta}")
    else:
        print(f"La carpeta {nombre_carpeta} ya existe en el escritorio.")

def dividir_grabar_convertir(nombre_carpeta, duracion_grabacion):
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
    ruta_archivo = os.path.join(ruta_carpeta, f"{nombre_carpeta}.wav")

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

    # Para dividir audio
    nombre_archivo_audio = f"{nombre_carpeta}.wav"
    dividir_audio(nombre_archivo_audio, ruta_carpeta)

    # Convertir audio a texto y guardar en archivos .txt y .docx
    ruta_archivo_txt, ruta_archivo_docx = convertir_audio_a_texto(ruta_carpeta, nombre_carpeta)

    print(f"Texto convertido y guardado en {ruta_archivo_txt} y {ruta_archivo_docx}")

def dividir_audio(nombre_archivo_audio, nombre_carpeta_destino):
    ruta_archivo_audio = os.path.join(nombre_carpeta_destino, nombre_archivo_audio)

    duracion_segmento = 1000  # 5 minutos en milisegundos
    audio = AudioSegment.from_file(ruta_archivo_audio)

    segmentos = []
    for i in range(0, len(audio), duracion_segmento):
        segmento = audio[i:i + duracion_segmento]
        segmentos.append(segmento)

    for i, segmento in enumerate(segmentos):
        nombre_archivo_segmento = f"{nombre_archivo_audio.replace('.wav', '')} parte_{i + 1}.wav"
        ruta_completa_segmento = os.path.join(nombre_carpeta_destino, nombre_archivo_segmento)
        segmento.export(ruta_completa_segmento, format="wav")

    print(f"El archivo de audio se ha dividido en {len(segmentos)} segmentos de 5 minutos cada uno y se han guardado en {nombre_carpeta_destino}.")

def convertir_audio_a_texto(nombre_carpeta, nombre_archivo_audio):
    ruta_archivo_audio = os.path.join(nombre_carpeta, f"{nombre_archivo_audio}.wav")

    recognizer = sr.Recognizer()

    with sr.AudioFile(ruta_archivo_audio) as source:
        audio = recognizer.record(source)

    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
    except sr.UnknownValueError:
        texto = "No se pudo reconocer ningún texto en el audio."
    except sr.RequestError:
        texto = "No se pudo procesar la solicitud de reconocimiento de voz."

    ruta_archivo_txt = os.path.join(nombre_carpeta, f"{nombre_archivo_audio}.txt")
    with open(ruta_archivo_txt, "w") as txt_file:
        txt_file.write(texto)

    ruta_archivo_docx = os.path.join(nombre_carpeta, f"{nombre_archivo_audio}.docx")
    doc = Document()
    doc.add_paragraph(texto)
    doc.save(ruta_archivo_docx)

    return ruta_archivo_txt, ruta_archivo_docx

# Configuración de pines
PIN_A = 3
PIN_B = 2
PIN_BUTTON = 0

# Configuración de pines como entrada
pin_a = Pin(PIN_A, Pin.IN)
pin_b = Pin(PIN_B, Pin.IN)
pin_button = Pin(PIN_BUTTON, Pin.IN)

# Variables para el estado del encoder
encoder_posicion = 0
pin_a_estado_anterior = pin_a.value()

# Funciones para el encoder
def manejar_cambio(pin):
    global encoder_posicion
    global pin_a_estado_anterior

    pin_a_estado = pin_a.value()
    pin_b_estado = pin_b.value()

    if pin == pin_a and pin_a_estado != pin_a_estado_anterior:
        if pin_b_estado != pin_a_estado:
            encoder_posicion += 1
            keyboard.press_and_release('right')
        else:
            encoder_posicion -= 1
            keyboard.press_and_release('left')

    pin_a_estado_anterior = pin_a_estado

def manejar_click(pin):
    if pin() == 0:  # Verifica si el botón está presionado
        keyboard.press_and_release('enter')

# Configurar interrupciones del encoder
pin_a.irq(trigger=Pin.IRQ_BOTH, handler=manejar_cambio)
pin_b.irq(trigger=Pin.IRQ_BOTH, handler=manejar_cambio)
pin_button.irq(trigger=Pin.IRQ_FALLING, handler=manejar_click)

# Funciones de los botones
def ejecutar_comandos_por_voz():
    mensaje_nombre_carpeta = "Por favor, di el nombre de la carpeta."
    nombre_carpeta = obtener_texto_por_voz(mensaje_nombre_carpeta)
    while nombre_carpeta is None:
        nombre_carpeta = obtener_texto_por_voz(mensaje_nombre_carpeta)

    crear_carpeta(nombre_carpeta)

    mensaje_duracion = "Por favor, di la duración de la grabación en segundos."
    duracion_grabacion = obtener_texto_por_voz(mensaje_duracion)
    while duracion_grabacion is None:
        duracion_grabacion = obtener_texto_por_voz(mensaje_duracion)

    duracion_grabacion = float(duracion_grabacion)

    dividir_grabar_convertir(nombre_carpeta, duracion_grabacion)

def ver_carpetas():
    ruta_escritorio = os.path.join(os.path.expanduser("~"), "Desktop")
    os.startfile(ruta_escritorio)

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Menú Raspberry Pi")

# Botones en la interfaz gráfica
boton_grabar = tk.Button(ventana, text="Grabar", command=ejecutar_comandos_por_voz)
boton_ver_carpetas = tk.Button(ventana, text="Ver Carpetas", command=ver_carpetas)

# Posicionamiento de los botones
boton_grabar.pack(pady=10)
boton_ver_carpetas.pack(pady=10)

# Bucle principal de la interfaz gráfica
ventana.mainloop()
