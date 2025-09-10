# Este script analiza el historial técnico y genera un reporte con:
#• 	Total de archivos procesados
#• 	Cantidad de archivados, duplicados y errores
#• 	Cuentas con más actividad
#• 	Archivos sin categoría
#• 	Alertas de integridad
# 🧩 Cómo programarlo automáticamente en Windows:
#1. 	Abrí el Programador de tareas
#2. 	Creá una nueva tarea
#3. 	En “Acciones”, seleccioná Iniciar un programa
#4. 	Ruta: PYTHON
#5. 	Argumentos: scripts/revision_mensual.py
#6. 	Programala para que se ejecute el primer día de cada mes o cuando prefieras
# Con esto el sistema se revisa solo, genera métricas, y permite detectar problemas antes de que escalen

import json
from collections import Counter
from datetime import datetime

def cargar_historial(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        print("⚠️ No se pudo cargar el historial.")
        return []

def generar_reporte(historial):
    total = len(historial)
    estados = Counter(
        "Archivado" if h.get("evento") == "Archivo archivado" and not h.get("error")
        else "Duplicado" if h.get("error") == "Duplicado por hash"
        else "Error"
        for h in historial
    )
    cuentas = Counter(h.get("cuenta") for h in historial if h.get("cuenta"))
    sin_categoria = sum(1 for h in historial if not h.get("categoria"))
    alertas = sum(1 for h in historial if h.get("alerta_integridad"))

    print(f"\n📋 Reporte de cumplimiento ({datetime.now().strftime('%Y-%m-%d')}):")
    print(f" - Total procesados: {total}")
    print(f" - Archivados: {estados['Archivado']}")
    print(f" - Duplicados: {estados['Duplicado']}")
    print(f" - Errores: {estados['Error']}")
    print(f" - Archivos sin categoría: {sin_categoria}")
    print(f" - Alertas de integridad: {alertas}")
    print(f" - Cuentas con más actividad:")
    for cuenta, cantidad in cuentas.most_common(5):
        print(f"   • {cuenta}: {cantidad} archivos")

def ejecutar_revision_mensual():
    historial = cargar_historial("scripts/historial_archivo.json")
    if historial:
        generar_reporte(historial)
    else:
        print("❌ No se encontró historial para generar el reporte.")

if __name__ == "__main__":
    ejecutar_revision_mensual()