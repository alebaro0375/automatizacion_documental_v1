import os
import sys
import logging
from pathlib import Path

# Agregar la raíz del proyecto al path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from archivado_automatico import procesar_archivos
from estructura_subcarpetas import cargar_estructura
from scripts.preprocesar_nombres import preprocesar_archivos  # ✅ Renombrado automático integrado

# --- Configuración de logging ---
logging.basicConfig(
    filename="./logs/registro.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

RESUMEN_PATH = "./resumen_archivo.xlsx"
HISTORIAL_PATH = "./historial_archivo.xlsx"
LOG_PATH = "./logs/registro.log"
BASE_PATH = "./Legajos/Archivados"
CARPETA_ORIGEN = Path("C:/Legajos/Docupen")

# --- Verificación de estructura por cuenta ---
def verificar_estructura(cuentas, categorias):
    for cuenta in cuentas:
        carpeta_cuenta = os.path.join(BASE_PATH, cuenta)
        print(f"🔍 Verificando carpeta de cuenta: {carpeta_cuenta}")
        assert os.path.exists(carpeta_cuenta), f"❌ Carpeta de cuenta no encontrada: {cuenta}"

        for categoria in categorias:
            subcarpeta = os.path.join(carpeta_cuenta, categoria)
            assert os.path.exists(subcarpeta), f"❌ Falta subcarpeta: {categoria} en cuenta {cuenta}"
    print("✅ Estructura de carpetas OK")

# --- Verificación de archivos movidos ---
def verificar_archivos_movidos(cuentas, categorias):
    total_archivos = 0
    for cuenta in cuentas:
        for categoria in categorias:
            subcarpeta = os.path.join(BASE_PATH, cuenta, categoria)
            if os.path.exists(subcarpeta):
                archivos = os.listdir(subcarpeta)
                total_archivos += len(archivos)
    if total_archivos == 0:
        print("⚠️ No se movió ningún archivo. Verificá el formato y las categorías.")
    else:
        print(f"✅ Archivos movidos: {total_archivos} encontrados")

# --- Verificación de archivos pendientes en Docupen ---
def verificar_archivos_pendientes():
    pendientes = []
    if CARPETA_ORIGEN.exists():
        for archivo in CARPETA_ORIGEN.glob("*.*"):
            pendientes.append(archivo.name)

    if pendientes:
        print(f"\n⚠️ Archivos que quedaron sin mover ({len(pendientes)}):")
        for nombre in pendientes:
            print(f"   ⏸️ {nombre}")
    else:
        print("\n✅ No quedaron archivos pendientes en Docupen.")

# --- Verificación de resumen ---
def verificar_resumen():
    if os.path.exists(RESUMEN_PATH):
        print("✅ Resumen generado correctamente")
    else:
        print("⚠️ No se generó el resumen Excel")

# --- Verificación de historial ---
def verificar_historial():
    if os.path.exists(HISTORIAL_PATH):
        print("✅ Historial actualizado")
    else:
        print("⚠️ No se generó el historial")

# --- Verificación de log ---
def verificar_log():
    if not os.path.exists(LOG_PATH):
        print("⚠️ No se generó el log")
        return
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        contenido = f.read()
    if "Inicio del flujo principal" in contenido:
        print("✅ Log generado correctamente")
    else:
        print("⚠️ Log incompleto")

# --- Verificación de archivado automático con logging ---
def verificar_archivado(estructura):
    logging.info("🔍 Iniciando verificación de archivado automático post-ejecución")
    resumen = procesar_archivos(estructura)

    errores = [r for r in resumen if "error" in r]
    exitosos = [r for r in resumen if "destino" in r]

    print(f"✅ Archivos archivados correctamente: {len(exitosos)}")
    print(f"⚠️ Archivos con errores: {len(errores)}")

    for r in exitosos:
        logging.info(f"Archivo archivado: {r['archivo']} → {r['destino']} (Cuenta: {r['cuenta']}, Categoría: {r['categoria']}, Fecha: {r['fecha']})")

    for r in errores:
        logging.warning(f"Error al archivar: {r['archivo']} → {r['error']} (Cuenta: {r.get('cuenta')}, Categoría: {r.get('categoria')})")

# --- Punto de entrada ---
if __name__ == "__main__":
    print("🧪 Iniciando verificación post-ejecución...\n")

    estructura = cargar_estructura()
    categorias = set(cat for lista in estructura.values() for cat in lista)

    print("🧼 Ejecutando renombrado automático...")
    preprocesar_archivos()

    print("\n📦 Ejecutando archivado automático...")
    verificar_archivado(estructura)

    cuentas_detectadas = [
        nombre for nombre in os.listdir(BASE_PATH)
        if os.path.isdir(os.path.join(BASE_PATH, nombre))
    ]

    print("\n🔍 Verificando estructura y resultados...")
    verificar_estructura(cuentas_detectadas, categorias)
    verificar_archivos_movidos(cuentas_detectadas, categorias)
    verificar_archivos_pendientes()
    verificar_resumen()
    verificar_historial()
    verificar_log()

    print("\n🎉 Verificación completa: todo está en orden.")