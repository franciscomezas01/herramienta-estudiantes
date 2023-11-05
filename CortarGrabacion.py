from pydub import AudioSegment
import os

def dividir_audio(nombre_archivo_audio):
    # Combinar el nombre del archivo con la ruta al escritorio
    ruta_archivo_audio = os.path.join(os.path.expanduser("~"), "Desktop", nombre_archivo_audio)

    duracion_segmento = 5   # 5 minutos en milisegundos
    audio = AudioSegment.from_file(ruta_archivo_audio)

    segmentos = []
    for i in range(0, len(audio), duracion_segmento):
        segmento = audio[i:i + duracion_segmento]
        segmentos.append(segmento)

    for i, segmento in enumerate(segmentos):
        nombre_archivo_segmento = f"segmento_{i + 1}.wav"
        nombre_completo_segmento = os.path.join(os.path.expanduser("~"), "Desktop", nombre_archivo_segmento)
        segmento.export(nombre_completo_segmento, format="wav")

    print(f"El archivo de audio se ha dividido en {len(segmentos)} segmentos de 5 minutos cada uno.")

if __name__ == "__main__":
    nombre_archivo_audio = input("Ingresa el nombre del archivo de audio a dividir (con la extensión .wav): ")
    dividir_audio(nombre_archivo_audio)
