import os
import tkinter as tk
from tkinter import messagebox
from paqueteGrabacion import grabar
from paqueteGrabacion import CortarGrabacion

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

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Grabación y División de Audio")

# Etiqueta y entrada para el nombre de la carpeta
etiqueta_carpeta = tk.Label(ventana, text="Nombre de la carpeta:")
etiqueta_carpeta.pack()
entrada_carpeta = tk.Entry(ventana)
entrada_carpeta.pack()

# Botón para crear la carpeta
boton_crear_carpeta = tk.Button(ventana, text="Crear Carpeta", command=crear_carpeta)
boton_crear_carpeta.pack()

# Etiqueta y entrada para la duración de la grabación
etiqueta_duracion = tk.Label(ventana, text="Duración de la grabación (segundos):")
etiqueta_duracion.pack()
entrada_duracion = tk.Entry(ventana)
entrada_duracion.pack()

# Botón para grabar audio
boton_grabar_audio = tk.Button(ventana, text="Grabar Audio", command=grabar_audio)
boton_grabar_audio.pack()

# Botón para dividir audio
boton_dividir_audio = tk.Button(ventana, text="Dividir Audio", command=dividir_audio)
boton_dividir_audio.pack()

ventana.mainloop()
