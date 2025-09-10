import os
import re
from datetime import datetime
from pathlib import Path

CARPETA_ORIGEN = Path("C:/Legajos/Docupen")
EXTENSIONES_VALIDAS = {".pdf", ".xlsx", ".docx", ".jpg", ".png", ".txt"}

def limpiar_extension(nombre):
    partes = nombre.split(".")
    if len(partes) > 2 and partes[-1].lower() == partes[-2].lower():
        return ".".join(partes[:-1]) + "." + partes[-1]
    return nombre

def detectar_fecha(nombre):
    match = re.search(r"\d{2}-\d{2}-\d{4}", nombre)
    if match:
        return match.group(), True
    return datetime.now().strftime("%d-%m-%Y"), False

def proponer_nombre_corregido(nombre_archivo):
    nombre_limpio = limpiar_extension(nombre_archivo)
    nombre_sin_ext, ext = os.path.splitext(nombre_limpio)

    partes = nombre_sin_ext.strip().split(" ")
    if len(partes) < 2:
        return None

    nro_cuenta = partes[0]
    tipo_raw = partes[1].replace(".", "").upper()
    nombre_doc = " ".join(partes[2:]) if len(partes) > 2 else ""

    fecha_detectada, tiene_fecha = detectar_fecha(nombre_doc)
    nombre_doc = re.sub(r"\d{2}-\d{2}-\d{4}", "", nombre_doc).strip()

    if not nombre_doc:
        nombre_doc = "SIN_DESCRIPCION"

    nuevo_nombre = f"{nro_cuenta} {tipo_raw}. {nombre_doc} {fecha_detectada}{ext}"
    return nuevo_nombre, tiene_fecha

def preprocesar_archivos():
    print("🔧 Iniciando renombrado automático en Docupen...\n")
    if not CARPETA_ORIGEN.exists():
        print("❌ Carpeta Docupen no encontrada.")
        return

    archivos = list(CARPETA_ORIGEN.glob("*.*"))
    if not archivos:
        print("⚠️ No se encontraron archivos en Docupen.")
        return

    total_renombrados = 0
    for archivo in archivos:
        resultado = proponer_nombre_corregido(archivo.name)
        if resultado:
            propuesta, tiene_fecha = resultado
            nuevo_path = CARPETA_ORIGEN / propuesta
            try:
                archivo.rename(nuevo_path)
                estado = "✅ con fecha" if tiene_fecha else "⚠️ sin fecha"
                print(f"{estado} → '{archivo.name}' → '{propuesta}'")
                total_renombrados += 1
            except Exception as e:
                print(f"❌ Error al renombrar '{archivo.name}': {e}")

    print(f"\n📊 Total de archivos renombrados: {total_renombrados}")

if __name__ == "__main__":
    preprocesar_archivos()