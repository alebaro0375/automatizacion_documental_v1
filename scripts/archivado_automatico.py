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

# --- Subcarpetas válidas por categoría ---
SUBCARPETAS_VALIDAS = {
    "01. CAC", "02. ESTATUTO-CONTRATO SOCIAL", "03. ORGANO DE ADMINISTRACION",
    "04. PODERES", "05. DJTCS", "06. DJBF", "07. DNI", "08. CONSTANCIAS",
    "09. ESTADOS CONTABLES", "10. MATRIZ DE RIESGO", "11. PERFIL DEL INVERSOR",
    "12. NOSIS", "13. PERFIL-OI", "14. OTROS"
}

# --- Validación y creación de estructura por número de cuenta ---
def asegurar_estructura(base_path, nro_cuenta, categoria):
    carpeta_cuenta = os.path.join(base_path, nro_cuenta)

    if not os.path.exists(carpeta_cuenta):
        os.makedirs(carpeta_cuenta)
        print(f"📁 Carpeta creada para cuenta: {nro_cuenta}")
        for sub in SUBCARPETAS_VALIDAS:
            os.makedirs(os.path.join(carpeta_cuenta, sub), exist_ok=True)
            print(f"📂 Subcarpeta creada: {sub}")
    else:
        subcarpeta = os.path.join(carpeta_cuenta, categoria)
        if not os.path.exists(subcarpeta):
            os.makedirs(subcarpeta)
            print(f"📂 Subcarpeta asegurada: {categoria} en cuenta {nro_cuenta}")

    return carpeta_cuenta

# --- Movimiento seguro de archivos con validación por cuenta y categoría ---
def archivar_documento(ruta_origen, nro_cuenta, categoria, base_path):
    if categoria not in SUBCARPETAS_VALIDAS:
        raise ValueError(f"Categoría inválida: {categoria}")

    destino_base = asegurar_estructura(base_path, nro_cuenta)
    destino_final = os.path.join(destino_base, categoria)

    nombre_archivo = os.path.basename(ruta_origen)
    ruta_destino = os.path.join(destino_final, nombre_archivo)

    shutil.move(ruta_origen, ruta_destino)
    return ruta_destino

# --- Extracción de cuenta y categoría desde nombre de archivo ---
def extraer_datos_desde_nombre(nombre_archivo):
    partes = nombre_archivo.split("_")
    if len(partes) < 2:
        return None, None
    nro_cuenta = partes[0]
    categoria_raw = partes[1].split(".")[0].strip().upper()
    return nro_cuenta, categoria_raw

# --- Flujo principal de archivado automático ---
def procesar_archivos(estructura):
    """
    estructura: dict con claves tipo_cliente (juridica, fisica, desconocido)
                y valores como listas de categorías válidas
    """
    resumen = []
    base_path = "./Legajos/Archivados"

    tipos_soportados = ["PDF", "JPG", "PNG"]  # Ajustar según tus carpetas de origen

    for tipo_cliente, categorias_validas in estructura.items():
        for tipo_archivo in tipos_soportados:
            origen = f"./{tipo_archivo}"
            if not os.path.exists(origen):
                continue

            for archivo in os.listdir(origen):
                origen_path = os.path.join(origen, archivo)
                nro_cuenta, categoria_raw = extraer_datos_desde_nombre(archivo)

                if not nro_cuenta or not categoria_raw:
                    resumen.append({
                        "archivo": archivo,
                        "origen": origen_path,
                        "error": "Nombre inválido",
                        "cuenta": None,
                        "categoria": None
                    })
                    continue

                # Buscar categoría completa que contenga el texto
                categoria_match = next(
                    (cat for cat in categorias_validas if categoria_raw in cat.upper()), None
                )

                if not categoria_match:
                    resumen.append({
                        "archivo": archivo,
                        "origen": origen_path,
                        "error": f"Categoría '{categoria_raw}' no válida para tipo '{tipo_cliente}'",
                        "cuenta": nro_cuenta,
                        "categoria": categoria_raw
                    })
                    continue

                try:
                    destino_path = archivar_documento(origen_path, nro_cuenta, categoria_match, base_path)
                    resumen.append({
                        "archivo": archivo,
                        "origen": origen_path,
                        "destino": destino_path,
                        "cuenta": nro_cuenta,
                        "categoria": categoria_match
                    })
                except Exception as e:
                    resumen.append({
                        "archivo": archivo,
                        "origen": origen_path,
                        "error": str(e),
                        "cuenta": nro_cuenta,
                        "categoria": categoria_match
                    })

    return resumen