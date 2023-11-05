import os
import tkinter as tk
from tkinter import messagebox
from paqueteGrabacion import grabar
from paqueteGrabacion import CortarGrabacion
from paqueteResumen import AudioTexto

def crear_carpeta():
    nombre_carpeta = entrada_carpeta.get()
    ruta_carpeta = os.path.join(os.path.expanduser("~"), "Desktop", nombre_carpeta)
    
    if not os.path.exists(ruta_carpeta):
        os.mkdir(ruta_carpeta)
        messagebox.showinfo("Información", f"Se ha creado la carpeta en el escritorio: {nombre_carpeta}")
    else:
        messagebox.showwarning("Advertencia", f"La carpeta {nombre_carpeta} ya existe en el escritorio.")

def grabar_audio():
    nombre_carpeta = entrada_carpeta.get()
    nombre_archivo = nombre_carpeta
    duracion_grabacion = float(entrada_duracion.get())
    
    grabar.grabar_audio(duracion_grabacion, nombre_carpeta, nombre_archivo)
    messagebox.showinfo("Información", f"La grabación se ha guardado en {nombre_carpeta}/{nombre_archivo}.wav")

def dividir_audio():
    nombre_carpeta = entrada_carpeta.get()
    nombre_archivo = nombre_carpeta
    nombre_archivo_audio = nombre_archivo + ".wav"
    CortarGrabacion.dividir_audio(nombre_archivo_audio, os.path.join(os.path.expanduser("~"), "Desktop", nombre_carpeta))
    messagebox.showinfo("Información", f"Se han dividido los segmentos de audio en la carpeta: {nombre_carpeta}")

def convertir_audio():
    nombre_carpeta = entrada_carpeta.get()
    nombre_archivo = nombre_carpeta
    ruta_archivo_audio = os.path.join(nombre_carpeta, f"{nombre_archivo}.wav")
    
    if os.path.exists(ruta_archivo_audio):
        ruta_archivo_txt, ruta_archivo_docx = AudioTexto.convertir_audio_a_texto(nombre_carpeta, nombre_archivo)
        messagebox.showinfo("Información", f"Texto convertido y guardado en {ruta_archivo_txt} y {ruta_archivo_docx}")
    else:
        messagebox.showerror("Error", "No se encontró el archivo de audio. Asegúrate de grabar y dividir el audio primero.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Grabación y Conversión de Audio a Texto")
ventana.geometry("400x400")
ventana.configure(bg="#800080")

# Etiqueta y entrada para el nombre de la carpeta
etiqueta_carpeta = tk.Label(ventana, text="Nombre de la carpeta:", font=("Helvetica", 14), bg="#800080", fg="white")
etiqueta_carpeta.pack()
entrada_carpeta = tk.Entry(ventana, font=("Helvetica", 14))
entrada_carpeta.pack()

# Botón para crear la carpeta
boton_crear_carpeta = tk.Button(ventana, text="Crear Carpeta", command=crear_carpeta, font=("Helvetica", 14), bg="#4B0082", fg="white")
boton_crear_carpeta.pack()

# Etiqueta y entrada para la duración de la grabación
etiqueta_duracion = tk.Label(ventana, text="Duración de la grabación (segundos):", font=("Helvetica", 14), bg="#800080", fg="white")
etiqueta_duracion.pack()
entrada_duracion = tk.Entry(ventana, font=("Helvetica", 14))
entrada_duracion.pack()

# Botón para grabar audio
boton_grabar_audio = tk.Button(ventana, text="Grabar Audio", command=grabar_audio, font=("Helvetica", 14), bg="#4B0082", fg="white")
boton_grabar_audio.pack()

# Botón para dividir audio
boton_dividir_audio = tk.Button(ventana, text="Dividir Audio", command=dividir_audio, font=("Helvetica", 14), bg="#4B0082", fg="white")
boton_dividir_audio.pack()

# Botón para convertir audio a texto
boton_convertir_audio = tk.Button(ventana, text="Convertir a Texto", command=convertir_audio, font=("Helvetica", 14), bg="#4B0082", fg="white")
boton_convertir_audio.pack()

ventana.mainloop()
