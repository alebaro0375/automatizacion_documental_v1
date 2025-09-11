import os
import re
import sys
from pathlib import Path
from datetime import datetime

# Agregar la raíz del proyecto al path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from estructura_subcarpetas import cargar_estructura  # Import corregido

CARPETA_ORIGEN = Path("C:\Users\ALEJANDRA\Desktop\LEGAJOS\Docupen")

def extraer_datos_desde_nombre(nombre_archivo):
    nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
    partes = nombre_sin_ext.strip().split(" ")

    if len(partes) < 4:
        return None, None, None, None

    nro_cuenta = partes[0]
    tipo_raw = partes[1].replace(".", "").upper()
    fecha_raw = partes[-1]

    nombre_doc = " ".join(partes[2:-1]).strip()

    # Validar fecha en formato DD-MM-YYYY
    if re.match(r"^\d{2}-\d{2}-\d{4}$", fecha_raw):
        fecha = fecha_raw.replace("-", "")
    else:
        fecha = datetime.now().strftime("%d%m%Y")
        print(f"🕒 Fecha asignada automáticamente para '{nombre_archivo}': {fecha}")

    if not nro_cuenta.isdigit():
        return None, None, None, None
    if not re.match(r"^(T|C\d+)$", tipo_raw):
        return None, None, None, None
    if not re.match(r"^(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[0-2])\d{4}$", fecha):
        return None, None, None, None

    return nro_cuenta, tipo_raw, nombre_doc, fecha

def diagnosticar_archivos():
    estructura = cargar_estructura()
    categorias_validas = set(cat.upper() for lista in estructura.values() for cat in lista)

    print("🔍 Iniciando diagnóstico de archivos en carpeta Docupen...\n")

    total_validos = 0
    total_invalidos = 0
    total_categoria_no_match = 0

    if not CARPETA_ORIGEN.exists():
        print("❌ La carpeta Docupen no existe.")
        return

    archivos = list(CARPETA_ORIGEN.glob("*.*"))
    if not archivos:
        print("⚠️ No se encontraron archivos en Docupen.")
        return

    for archivo in archivos:
        nro_cuenta, tipo_doc, nombre_doc, fecha = extraer_datos_desde_nombre(archivo.name)

        if not nro_cuenta or not tipo_doc:
            print(f"⚠️ Formato inválido: {archivo.name}")
            total_invalidos += 1
            continue

        categoria_match = next((cat for cat in categorias_validas if tipo_doc in cat.upper()), None)

        if not categoria_match:
            print(f"❌ Categoría no reconocida: {archivo.name} → tipo '{tipo_doc}' no mapea")
            total_categoria_no_match += 1
            continue

        print(f"✅ Válido: {archivo.name} → Cuenta: {nro_cuenta}, Categoría: {categoria_match}, Fecha: {fecha}")
        total_validos += 1

    print("\n📊 Resumen del diagnóstico:")
    print(f"✔ Archivos válidos: {total_validos}")
    print(f"⚠ Formato inválido: {total_invalidos}")
    print(f"❌ Categoría no reconocida: {total_categoria_no_match}")

if __name__ == "__main__":
    diagnosticar_archivos()
