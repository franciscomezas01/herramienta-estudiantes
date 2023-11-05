import os

# Ruta de la carpeta que deseas crear
nombre_carpeta = "mi_carpeta"

# Verificar si la carpeta ya existe
if not os.path.exists(nombre_carpeta):
    # Crear la carpeta si no existe
    os.mkdir(nombre_carpeta)
    print(f"Se ha creado la carpeta: {nombre_carpeta}")
else:
    print(f"La carpeta {nombre_carpeta} ya existe.")

# Ruta completa del archivo a guardar en la carpeta
nombre_archivo = "mi_archivo.txt"
ruta_archivo = os.path.join(nombre_carpeta, nombre_archivo)

# Guardar un archivo en la carpeta
with open(ruta_archivo, "w") as archivo:
    archivo.write("Este es el contenido del archivo.")

print(f"Se ha guardado el archivo en la carpeta: {nombre_carpeta}/{nombre_archivo}")
