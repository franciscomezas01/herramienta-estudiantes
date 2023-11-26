import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import speech_recognition as sr
from paqueteGrabacion import grabar
from paqueteGrabacion import CortarGrabacion
from paqueteResumen import AudioTexto

class MenuPorVozGUI:
    def __init__(self, master):
        self.master = master
        master.title("Menú por Voz")

        # Fondo de la ventana principal
        master.configure(bg='#F0F0F0')

        # Configurar el estilo de los botones
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", font=('Helvetica', 12))

        # Iconos (ajustados al tamaño deseado)
        icono_brazo = tk.PhotoImage(file="brazo.png").subsample(3, 3)  # Ajusta el tamaño según sea necesario
        icono_microfono = tk.PhotoImage(file="microfono.png").subsample(3, 3)  # Ajusta el tamaño según sea necesario

        # Botón principal
        self.boton_ejecutar = ttk.Button(master, text="Ejecutar Script", command=self.iniciar_proceso, style="TButton")
        self.boton_ejecutar.pack(pady=20)

        # Imágenes decorativas al costado del botón
        self.label_imagen_brazo = tk.Label(master, image=icono_brazo, bg='#F0F0F0')
        self.label_imagen_brazo.image = icono_brazo
        self.label_imagen_brazo.pack(side=tk.LEFT, padx=10)

        self.label_imagen_microfono = tk.Label(master, image=icono_microfono, bg='#F0F0F0')
        self.label_imagen_microfono.image = icono_microfono
        self.label_imagen_microfono.pack(side=tk.RIGHT, padx=10)

    def obtener_texto_por_voz(self, mensaje):
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
            return self.obtener_texto_por_voz(mensaje)
        except sr.RequestError:
            print("Error al conectar con el servicio de reconocimiento de voz.")
            return None

    def iniciar_proceso(self):
        # Obtener el nombre de la carpeta mediante comandos de voz
        mensaje_nombre_carpeta = "Por favor, di el nombre de la carpeta."
        nombre_carpeta = self.obtener_texto_por_voz(mensaje_nombre_carpeta)
        while nombre_carpeta is None:
            nombre_carpeta = self.obtener_texto_por_voz(mensaje_nombre_carpeta)

        # Crear la carpeta en el escritorio
        ruta_carpeta = os.path.join(os.path.expanduser("~"), "Desktop", nombre_carpeta)
        if not os.path.exists(ruta_carpeta):
            os.mkdir(ruta_carpeta)
            print(f"Se ha creado la carpeta en el escritorio: {nombre_carpeta}")
        else:
            print(f"La carpeta {nombre_carpeta} ya existe en el escritorio.")

        # Obtener la duración mediante comandos de voz
        mensaje_duracion = "Por favor, di la duración de la grabación en segundos."
        duracion_grabacion = self.obtener_texto_por_voz(mensaje_duracion)
        while duracion_grabacion is None:
            duracion_grabacion = self.obtener_texto_por_voz(mensaje_duracion)

        duracion_grabacion = float(duracion_grabacion)

        nombre_archivo = nombre_carpeta
        grabar.grabar_audio(duracion_grabacion, nombre_carpeta, nombre_archivo)

        # Para dividir audio
        nombre_archivo_audio = nombre_archivo + ".wav"
        CortarGrabacion.dividir_audio(nombre_archivo_audio, ruta_carpeta)

        # Convertir audio a texto y guardar en archivos .txt y .docx
        ruta_archivo_txt, ruta_archivo_docx = AudioTexto.convertir_audio_a_texto(ruta_carpeta, nombre_archivo)

        messagebox.showinfo("Proceso Completado", f"Texto convertido y guardado en {ruta_archivo_txt} y {ruta_archivo_docx}")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x200")  # Cambiar el tamaño de la ventana
    menu_gui = MenuPorVozGUI(root)
    root.mainloop()


