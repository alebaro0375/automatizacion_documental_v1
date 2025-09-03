import os
import shutil
import re
import pandas as pd
from datetime import datetime
from pathlib import Path

# --- Configuración ---
CARPETA_ORIGEN = Path("C:/Legajos/Docupen")
BASE_PATH = Path("C:/Legajos")
EXCEL_CUENTAS = Path("config/cuentas.xlsx")
ESTRUCTURA_CARPETAS = {
    "juridica": [
        "01. CAC", "02. ESTATUTO-CONTRATO SOCIAL", "03. ORGANO DE ADMINISTRACION", "04. PODERES"
    ],
    "humana": [
        "01. CAC", "05. DJTCS", "06. DJBF", "07. DNI", "08. CONSTANCIAS", "09. ESTADOS CONTABLES",
        "10. MATRIZ DE RIESGO", "11. PERFIL DEL INVERSOR", "12. NOSIS", "13. PERFIL-OI", "14. OTROS"
    ]
}

# --- Cargar cuentas desde Excel ---
def cargar_cuentas_desde_excel(ruta_excel="config/cuentas.xlsx"):
    df = pd.read_excel(ruta_excel)
    cuentas_dict = {}

    for _, row in df.iterrows():
        cuenta = str(row["Comitente  -Número"]).strip()
        tipo_raw = str(row["Comitente  -Tipo de Comitente"]).strip().lower()

        if tipo_raw in {"física", "fisica"}:
            tipo = "humana"
        elif tipo_raw in {"jurídica", "juridica"}:
            tipo = "juridica"
        else:
            tipo = "humana"

        cuentas_dict[cuenta] = tipo

    return cuentas_dict

# --- Extraer datos desde nombre de archivo ---
def extraer_datos_desde_nombre(nombre_archivo):
    nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
    partes = nombre_sin_ext.strip().split(" ")

    if len(partes) < 4:
        return None, None, None, None

    nro_cuenta = partes[0]
    tipo_doc = partes[1].replace(".", "").upper()
    fecha_raw = partes[-1]
    nombre_doc = " ".join(partes[2:-1]).strip()

    if re.match(r"\d{2}-\d{2}-\d{4}", fecha_raw):
        fecha = fecha_raw.replace("-", "")
    else:
        fecha = datetime.now().strftime("%d%m%Y")
        print(f"🕒 Fecha asignada automáticamente para '{nombre_archivo}': {fecha}")

    if not nro_cuenta.isdigit():
        return None, None, None, None
    if not re.match(r"^(T|C\d+)$", tipo_doc):
        return None, None, None, None
    if not re.match(r"^(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[0-2])\d{4}$", fecha):
        return None, None, None, None

    return nro_cuenta, tipo_doc, nombre_doc, fecha

# --- Detectar subcarpeta por nombre de documento ---
def detectar_categoria(nombre_doc, categorias_validas):
    nombre_doc = nombre_doc.lower()
    for carpeta in categorias_validas:
        if carpeta.lower().split(". ")[1] in nombre_doc:
            return carpeta
    return None

# --- Crear estructura si no existe ---
def asegurar_estructura(base_path, nro_cuenta, categorias_validas):
    carpeta_cuenta = base_path / nro_cuenta
    if not carpeta_cuenta.exists():
        carpeta_cuenta.mkdir(parents=True)
        print(f"📁 Carpeta creada para cuenta: {nro_cuenta}")
        for sub in categorias_validas:
            (carpeta_cuenta / sub).mkdir(exist_ok=True)
            print(f"📂 Subcarpeta creada: {sub}")
    return carpeta_cuenta

# --- Flujo principal ---
def procesar_archivos():
    resumen = []
    cuentas_dict = cargar_cuentas_desde_excel(EXCEL_CUENTAS)

    if not CARPETA_ORIGEN.exists():
        print("❌ Carpeta de origen no encontrada.")
        return []

    archivos = list(CARPETA_ORIGEN.glob("*.*"))
    if not archivos:
        print("⚠️ No se encontraron archivos en Docupen.")
        return []

    for archivo in archivos:
        print(f"\n➡️ Procesando: {archivo.name}")
        nro_cuenta, tipo_doc, nombre_doc, fecha = extraer_datos_desde_nombre(archivo.name)
        origen_path = str(archivo)

        if not nro_cuenta or not nombre_doc:
            print(f"❌ Nombre inválido: {archivo.name}")
            resumen.append({
                "archivo": archivo.name,
                "origen": origen_path,
                "error": "Nombre inválido",
                "cuenta": None,
                "categoria": None
            })
            continue

        tipo_cliente = cuentas_dict.get(nro_cuenta, "humana")
        print(f"   Cuenta detectada: {nro_cuenta} | Tipo: {tipo_cliente}")
        print(f"   Nombre documental: {nombre_doc}")

        categorias_validas = ESTRUCTURA_CARPETAS.get(tipo_cliente, [])
        categoria_match = detectar_categoria(nombre_doc, categorias_validas)
        print(f"   Categoría detectada: {categoria_match if categoria_match else '❌ No detectada'}")

        if not categoria_match:
            resumen.append({
                "archivo": archivo.name,
                "origen": origen_path,
                "error": f"No se detectó categoría para '{nombre_doc}'",
                "cuenta": nro_cuenta,
                "categoria": None
            })
            continue

        carpeta_cuenta = asegurar_estructura(BASE_PATH, nro_cuenta, categorias_validas)
        destino_final = carpeta_cuenta / categoria_match / archivo.name

        try:
            shutil.move(str(archivo), str(destino_final))
            print(f"📦 Movido: {archivo.name} → {categoria_match}")
        except Exception as e:
            print(f"❌ Error al mover {archivo.name}: {e}")
            resumen.append({
                "archivo": archivo.name,
                "origen": origen_path,
                "error": str(e),
                "cuenta": nro_cuenta,
                "categoria": categoria_match
            })
            continue

        resumen.append({
            "archivo": archivo.name,
            "origen": origen_path,
            "destino": str(destino_final),
            "cuenta": nro_cuenta,
            "categoria": categoria_match,
            "fecha": fecha
        })

    return resumen

# --- Ejecución directa ---
if __name__ == "__main__":
    resumen = procesar_archivos()
    print(f"\n✅ Archivos procesados: {len(resumen)}")