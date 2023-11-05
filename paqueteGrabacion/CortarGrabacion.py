from pydub import AudioSegment
import os

def dividir_audio(nombre_archivo_audio, nombre_carpeta_destino):
    # Combinar el nombre del archivo con la ruta de la carpeta personalizada
    ruta_archivo_audio = os.path.join(nombre_carpeta_destino, nombre_archivo_audio)

    duracion_segmento = 1000  # 5 minutos en milisegundos
    audio = AudioSegment.from_file(ruta_archivo_audio)

    segmentos = []
    for i in range(0, len(audio), duracion_segmento):
        segmento = audio[i:i + duracion_segmento]
        segmentos.append(segmento)

    for i, segmento in enumerate(segmentos):
        nombre_archivo_segmento = f"{nombre_archivo_audio} {i + 1}.wav"
        ruta_completa_segmento = os.path.join(nombre_carpeta_destino, nombre_archivo_segmento)
        segmento.export(ruta_completa_segmento, format="wav")

    print(f"El archivo de audio se ha dividido en {len(segmentos)} segmentos de 5 minutos cada uno y se han guardado en {nombre_carpeta_destino}.")
