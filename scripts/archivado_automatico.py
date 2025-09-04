import os
import shutil
import re
import pandas as pd
from datetime import datetime
from pathlib import Path
import unicodedata

# --- Configuración ---
CARPETA_ORIGEN = Path("C:/Legajos/Docupen")
BASE_PATH = Path("C:/Legajos")
EXCEL_CUENTAS = Path("config/cuentas.xlsx")

# --- Estructura por tipo de cliente ---
ESTRUCTURA_CARPETAS = {
    "humana": [
        "01. CAC","02. DNI","03. CONSTANCIAS","04. NOSIS","05. DOCUMENTACION",
        "06. PERFIL-OI","07. MATRIZ DE RIESGO","08. PERFIL DEL INVERSOR",
        "09. OFICIOS JUDICIALES","10. OTROS"
    ],
    "juridica": [
        "01. CAC","02. ESTATUTO-CONTRATO SOCIAL", "03. ORGANO DE ADMINISTRACION",
        "04. PODERES", "05. DJTCS" , "06. DJBF", "07. DNI", "08. CONSTANCIAS",
        "09. ESTADOS CONTABLES", "10. MATRIZ DE RIESGO", "11. PERFIL DEL INVERSOR",
        "12. NOSIS", "13. PERFIL-OI", "14. OTROS"
    ]
}

# --- Normalizar texto ---
def normalizar(texto):
    return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII").lower().strip()

# --- Cargar cuentas desde Excel ---
def cargar_cuentas_desde_excel(ruta_excel):
    df = pd.read_excel(ruta_excel)
    cuentas_dict = {}

    for _, row in df.iterrows():
        cuenta = str(row["Comitente  -Número"]).strip()
        tipo_raw = str(row["Comitente  -Tipo de Comitente"])
        tipo_normalizado = normalizar(tipo_raw)

        if "juridica" in tipo_normalizado:
            tipo = "juridica"
        elif "fisica" in tipo_normalizado:
            tipo = "humana"
        else:
            tipo = "desconocido"
            print(f"⚠️ Tipo no reconocido para cuenta {cuenta}: '{tipo_raw}' → asignado como 'desconocido'")

        cuentas_dict[cuenta] = tipo

    return cuentas_dict

# --- Extraer datos desde nombre de archivo ---
def extraer_datos_desde_nombre(nombre_archivo):
    nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
    nombre_sin_ext = re.sub(r"[_\-]", " ", nombre_sin_ext)
    nombre_sin_ext = re.sub(r"\s+", " ", nombre_sin_ext).strip()

    match_prefijo = re.match(r"^(0[1-9]|1[0-4])\.(\-)?(\d+)", nombre_sin_ext)
    if match_prefijo:
        prefijo = f"{match_prefijo.group(1)}."
        nro_cuenta = match_prefijo.group(3)
        resto = nombre_sin_ext.replace(match_prefijo.group(0), "").strip()
    else:
        partes = nombre_sin_ext.split(" ")
        prefijo = partes[0] if partes[0].endswith(".") or partes[0].endswith(".-") else None
        offset = 1 if prefijo else 0
        nro_cuenta = partes[offset] if len(partes) > offset and partes[offset].isdigit() else None
        resto = " ".join(partes[offset+1:])

    if not nro_cuenta:
        return None, None, None, None

    fecha_raw = re.search(r"\d{2}-\d{2}-\d{4}", nombre_sin_ext)
    fecha_raw = fecha_raw.group() if fecha_raw else None

    if fecha_raw:
        fecha = fecha_raw.replace("-", "")
    else:
        fecha = datetime.now().strftime("%d%m%Y")
        print(f"🕒 Fecha asignada automáticamente para '{nombre_archivo}': {fecha}")

    if not re.match(r"^(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[0-2])\d{4}$", fecha):
        return None, None, None, None

    tipo_doc = None
    for parte in resto.split():
        if re.search(r"T\.|C\d+\.", parte.upper()):
            tipo_doc = re.sub(r"[^\w]", "", parte.upper())
            break

    nombre_doc = resto
    for elemento in [fecha_raw, tipo_doc]:
        if elemento:
            nombre_doc = nombre_doc.replace(elemento, "")
    nombre_doc = nombre_doc.strip()

    return nro_cuenta, tipo_doc, nombre_doc, fecha

# --- Detectar categoría por prefijo ---
def detectar_categoria_por_prefijo(prefijo, categorias_validas):
    if not isinstance(prefijo, str):
        return None
    for carpeta in categorias_validas:
        if carpeta.startswith(prefijo):
            return carpeta
    return None

# --- Extraer prefijo si existe ---
def obtener_prefijo(nombre_archivo):
    partes = nombre_archivo.split()
    return partes[0] if partes and (partes[0].endswith(".-") or partes[0].endswith(".")) else None

# --- Detectar subcategoría especial para CONSTANCIAS ---
def extraer_subcategoria_constancia(nombre):
    nombre = nombre.upper()
    if "SOCIEDAD" in nombre:
        return "SOCIEDAD"
    elif "CUIT RL" in nombre or "REPRESENTANTE LEGAL" in nombre:
        return "REPRESENTANTE LEGAL"
    elif "CUIT BF" in nombre or "BENEFICIARIO FINAL" in nombre or "BF" in nombre:
        return "BENEFICIARIOS FINALES"
    return "OTROS"

# --- Extraer año desde fecha en nombre ---
def extraer_anio(nombre):
    nombre = re.sub(r"\s+", " ", nombre).strip()
    match = re.search(r"\d{2}-\d{2}-\d{4}", nombre)
    if match:
        try:
            fecha = datetime.strptime(match.group(), "%d-%m-%Y")
            return str(fecha.year)
        except:
            pass
    return "SIN_FECHA"

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
        print(f"🔍 Cuenta {nro_cuenta} detectada como tipo: {tipo_cliente}")
        categorias_validas = ESTRUCTURA_CARPETAS.get(tipo_cliente, [])
        carpeta_cuenta = asegurar_estructura(BASE_PATH, nro_cuenta, categorias_validas)

        prefijo = obtener_prefijo(archivo.name)
        print(f"🔎 Prefijo detectado: {prefijo}")
        categoria_match = detectar_categoria_por_prefijo(prefijo, categorias_validas)

        # --- Lógica especial para CONSTANCIAS ---
        if prefijo in {"08.-", "08."} or categoria_match == "08. CONSTANCIAS":
            subcategoria = extraer_subcategoria_constancia(nombre_doc)
            anio = extraer_anio(archivo.name)
            print(f"📅 Año detectado para constancia: {anio}")
            destino_final = carpeta_cuenta / "08. CONSTANCIAS" / subcategoria / anio
            destino_final.mkdir(parents=True, exist_ok=True)
        elif categoria_match:
            destino_final = carpeta_cuenta / categoria_match
            destino_final.mkdir(parents=True, exist_ok=True)
        else:
            destino_final = carpeta_cuenta / "14. OTROS"
            destino_final.mkdir(parents=True, exist_ok=True)

        try:
            shutil.move(str(archivo), str(destino_final / archivo.name))
            print(f"📦 Movido: {archivo.name} → {destino_final}")
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
            "destino": str(destino_final / archivo.name),
            "cuenta": nro_cuenta,
            "categoria": categoria_match,
            "fecha": fecha
        })

    return resumen

# --- Ejecución directa ---
if __name__ == "__main__":
    resumen = procesar_archivos()
    print(f"\n✅ Archivos procesados: {len(resumen)}")

    errores = [r for r in resumen if "error" in r and r["error"]]
    if errores:
        print(f"⚠️ Archivos con error: {len(errores)}")
        for err in errores:
            print(f"   - {err['archivo']} → {err['error']}")
    else:
        print("🎉 Todos los archivos fueron archivados correctamente.")