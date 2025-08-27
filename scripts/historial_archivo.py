import os
import json
from datetime import datetime

HISTORIAL_PATH = "./historial_archivo.xlsx"  # Usado como ruta por defecto si no se especifica

# --- Registrar un evento puntual ---
def registrar_evento(ruta_historial, evento, archivo_afectado=None):
    """
    Registra un evento técnico en el historial.
    Ejemplo: "Inicio del flujo principal", "Verificación completada", etc.
    """
    entrada = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "evento": evento,
        "archivo": archivo_afectado
    }

    historial = []
    if os.path.exists(ruta_historial):
        with open(ruta_historial, "r", encoding="utf-8") as f:
            try:
                historial = json.load(f)
            except json.JSONDecodeError:
                historial = []

    historial.append(entrada)

    with open(ruta_historial, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)

# --- Registrar múltiples eventos desde resumen_data ---
def actualizar_historial(resumen_data, ruta_historial):
    """
    Registra múltiples eventos en el historial a partir del resumen generado.
    Cada entrada incluye timestamp, cuenta, categoría, archivo y estado.
    """
    historial = []
    if os.path.exists(ruta_historial):
        with open(ruta_historial, "r", encoding="utf-8") as f:
            try:
                historial = json.load(f)
            except json.JSONDecodeError:
                historial = []

    for item in resumen_data:
        entrada = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "evento": "Archivo archivado" if "destino" in item else "Error al archivar",
            "archivo": item.get("archivo"),
            "cuenta": item.get("cuenta"),
            "categoria": item.get("categoria"),
            "origen": item.get("origen"),
            "destino": item.get("destino") if "destino" in item else None,
            "error": item.get("error") if "error" in item else None
        }
        historial.append(entrada)

    with open(ruta_historial, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)