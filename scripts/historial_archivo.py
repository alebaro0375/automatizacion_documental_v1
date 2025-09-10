import os
import json
from datetime import datetime

HISTORIAL_PATH = "./historial_archivo.json"  # Usamos .json para coherencia con el formato

# --- Cargar historial existente ---
def cargar_historial(ruta_historial):
    if os.path.exists(ruta_historial):
        with open(ruta_historial, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# --- Guardar historial actualizado ---
def guardar_historial(historial, ruta_historial):
    with open(ruta_historial, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)

# --- Verificar si un evento ya fue registrado ---
def ya_registrado(historial, entrada):
    return any(
        h["archivo"] == entrada["archivo"] and h["evento"] == entrada["evento"]
        for h in historial
    )

# --- Registrar un evento puntual ---
def registrar_evento(ruta_historial, evento, archivo_afectado=None, hash_archivo=None):
    historial = cargar_historial(ruta_historial)
    entrada = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "evento": evento,
        "archivo": archivo_afectado,
        "hash": hash_archivo
    }
    if not ya_registrado(historial, entrada):
        historial.append(entrada)
        guardar_historial(historial, ruta_historial)

# --- Registrar múltiples eventos desde resumen_data ---
def actualizar_historial(resumen_data, ruta_historial, entorno=None):
    historial = cargar_historial(ruta_historial)

    for item in resumen_data:
        entrada = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "host": entorno.get("host") if entorno else None,
            "ip_local": entorno.get("ip_local") if entorno else None,
            "script": entorno.get("script") if entorno else None,
            "evento": "Archivo archivado" if "destino" in item else "Error al archivar",
            "archivo": item.get("archivo"),
            "cuenta": item.get("cuenta"),
            "categoria": item.get("categoria"),
            "origen": item.get("origen"),
            "destino": item.get("destino"),
            "error": item.get("error"),
            "hash": item.get("hash"),
            "alerta_integridad": item.get("alerta_integridad", False)
        }
        if not ya_registrado(historial, entrada):
            historial.append(entrada)

    guardar_historial(historial, ruta_historial)