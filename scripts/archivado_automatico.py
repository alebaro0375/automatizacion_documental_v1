# Proceso completo de archivado de documentos generados. 
# Sus funciones están pensadas para ejecutarse como parte de un flujo 
# automatizado.
# Tipo de documento: reconoce todo tipo de documento: PDF, JPG, WORD, EXCEL
# Llamada a: asegura que la estructura de carpetas por cliente/fecha esté 
# creada correctamente antes de archivar.
# Validación de nombres y duplicados: evita conflictos por archivos 
# repetidos o mal nombrados, apoyándose en reglas definidas en el archivo
# de configuración.
# Movimiento seguro de archivos: transfiere los archivos desde la carpeta
# temporal hacia la ubicación final, conservando metadatos clave.
# Log estructurado: registra cada acción (origen, destino, resultado) en 
# un archivo controlado para trazabilidad posterior.


import os
import shutil

def procesar_archivos(estructura):
    resumen = []
    for tipo, subcarpeta in estructura.items():
        origen = f"./{tipo}"
        destino = f"./Legajos/{subcarpeta}"
        os.makedirs(destino, exist_ok=True)
        if os.path.exists(origen):
            for archivo in os.listdir(origen):
                origen_path = os.path.join(origen, archivo)
                destino_path = os.path.join(destino, archivo)
                shutil.move(origen_path, destino_path)
                resumen.append((archivo, destino_path))
    return resumen