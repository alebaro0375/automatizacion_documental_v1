"""
archivado_auditable.py

Sistema de archivado documental con trazabilidad, detección de duplicados, colisiones de hash y auditoría integrada.

Autor: Alejandra
Fecha: 10-09-2025

Funciones principales:
- Clasificación por cuenta, categoría, subrol y año
- Registro de hash y verificación de duplicados
- Detección de colisiones (contenido modificado con mismo hash)
- Reporte de inconsistencias (hash registrado sin archivo físico)
- Log de auditoría completo para revisión técnica y regulatoria
"""

import os
import re
import hashlib
from datetime import datetime

# 📁 Configuración
RUTA_ENTRADA = "C:/Legajos/Docupen/"
RUTA_SALIDA = "C:/Legajos/"
hashes_existentes = {}  # {hash: {"ruta": ..., "tamano": ..., "modificado": ...}}
log_auditoria = []

# 🔐 Cálculo de hash
def calcular_hash_archivo(ruta):
    with open(ruta, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# 🔍 Detección de colisión
def detectar_colision(hash_actual, ruta_actual):
    if hash_actual in hashes_existentes:
        registro = hashes_existentes[hash_actual]
        tamano_nuevo = os.path.getsize(ruta_actual)
        modificado_nuevo = os.path.getmtime(ruta_actual)
        if tamano_nuevo != registro["tamano"] or modificado_nuevo != registro["modificado"]:
            return {
                "estado": "COLISION DE HASH",
                "ruta_original": registro["ruta"],
                "ruta_nueva": ruta_actual
            }
    return None

# 🧾 Log de auditoría
def registrar_evento(archivo, cuenta, categoria, subrol, estado, hash_actual):
    log_auditoria.append({
        "fecha": datetime.now().isoformat(),
        "archivo": archivo,
        "cuenta": cuenta,
        "categoria": categoria,
        "subrol": subrol,
        "estado": estado,
        "hash": hash_actual
    })

# ⚠️ Inconsistencias
def detectar_inconsistencias():
    inconsistencias = []
    for hash_registrado, datos in hashes_existentes.items():
        if not os.path.exists(datos["ruta"]):
            inconsistencias.append({
                "hash": hash_registrado,
                "ruta_esperada": datos["ruta"],
                "estado": "Archivo no encontrado"
            })
    return inconsistencias

# 🧠 Clasificación
def extraer_datos(nombre):
    nombre = nombre.upper()
    cuenta_match = re.search(r"\b(\d{4,6})\b", nombre)
    cuenta = cuenta_match.group(1) if cuenta_match else "SIN_CUENTA"

    prefijo_match = re.match(r"^(\d{2,})[.\s_-]", nombre)
    categoria = f"{prefijo_match.group(1)}. " + detectar_categoria(prefijo_match.group(1)) if prefijo_match else "SIN_CATEGORIA"

    subrol = extraer_subrol_constancia(nombre)
    fecha_match = re.search(r"(\d{2})[-_/](\d{2})[-_/](\d{4})", nombre)
    anio = fecha_match.group(3) if fecha_match else "SIN_FECHA"

    return cuenta, categoria, subrol, anio

def detectar_categoria(prefijo):
    categorias = {
        "01": "CAC", "02": "ESTATUTO-CONTRATO SOCIAL", "03": "CONSTANCIAS",
        "04": "NOSIS", "05": "DOCUMENTACION", "06": "PERFIL-OI",
        "07": "DNI", "08": "CONSTANCIAS", "09": "ESTADOS CONTABLES",
        "10": "OTROS", "12": "NOSIS", "13": "PERFIL-OI"
    }
    return categorias.get(prefijo, "OTROS")

def extraer_subrol_constancia(nombre):
    if "SOCIEDAD" in nombre:
        return "SOCIEDAD"
    if re.search(r"CUIT[\s\-_]*RL", nombre) or "REPRESENTANTE LEGAL" in nombre:
        return "REPRESENTANTE LEGAL"
    if re.search(r"CUIT[\s\-_]*BF", nombre) or "BENEFICIARIO FINAL" in nombre or re.search(r"\bBF\b", nombre):
        return "BENEFICIARIOS FINALES"
    if re.search(r"\bT[.\s_-]", nombre):
        return "TITULAR"
    match = re.search(r"\bC(\d+)(?=[.\s_-])", nombre)
    if match:
        return f"COTITULAR {match.group(1)}"
    return "OTROS"

# 🚀 Procesamiento
def procesar_archivos():
    for archivo in os.listdir(RUTA_ENTRADA):
        ruta_archivo = os.path.join(RUTA_ENTRADA, archivo)
        hash_actual = calcular_hash_archivo(ruta_archivo)

        # Colisión
        colision = detectar_colision(hash_actual, ruta_archivo)
        if colision:
            registrar_evento(archivo, "-", "-", "-", colision["estado"], hash_actual)
            print(f"⚠️ Colisión detectada: {archivo}")
            continue

        # Duplicado físico
        if hash_actual in hashes_existentes and os.path.exists(hashes_existentes[hash_actual]["ruta"]):
            registrar_evento(archivo, "-", "-", "-", "Duplicado", hash_actual)
            print(f"🛑 Duplicado detectado: {archivo}")
            continue

        # Clasificación
        cuenta, categoria, subrol, anio = extraer_datos(archivo)
        destino = os.path.join(RUTA_SALIDA, cuenta, categoria, subrol, anio, archivo)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        os.rename(ruta_archivo, destino)

        # Registro
        hashes_existentes[hash_actual] = {
            "ruta": destino,
            "tamano": os.path.getsize(destino),
            "modificado": os.path.getmtime(destino)
        }
        registrar_evento(archivo, cuenta, categoria, subrol, "Procesado", hash_actual)
        print(f"📦 Movido: {archivo} → {destino}")

# 📄 Reporte final
def generar_reporte():
    print("\n📄 Log de auditoría:")
    for e in log_auditoria:
        print(f"{e['fecha']} | {e['estado']} | {e['archivo']} → {e['cuenta']}/{e['categoria']}/{e['subrol']}")

    inconsistencias = detectar_inconsistencias()
    if inconsistencias:
        print("\n⚠️ Inconsistencias detectadas:")
        for i in inconsistencias:
            print(f"🔍 Hash: {i['hash']} | Ruta esperada: {i['ruta_esperada']} | Estado: {i['estado']}")
    else:
        print("\n✅ No se detectaron inconsistencias.")

# 🧠 Ejecución
if __name__ == "__main__":
    procesar_archivos()
    generar_reporte()