import os
import logging
from scripts.archivado_automatico import procesar_archivos
from scripts.estructura_subcarpetas import cargar_estructura

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
    assert total_archivos > 0, "❌ No se movió ningún archivo"
    print(f"✅ Archivos movidos: {total_archivos} encontrados")

# --- Verificación de resumen ---
def verificar_resumen():
    assert os.path.exists(RESUMEN_PATH), "❌ No se generó el resumen Excel"
    print("✅ Resumen generado correctamente")

# --- Verificación de historial ---
def verificar_historial():
    assert os.path.exists(HISTORIAL_PATH), "❌ No se generó el historial"
    print("✅ Historial actualizado")

# --- Verificación de log ---
def verificar_log():
    assert os.path.exists(LOG_PATH), "❌ No se generó el log"
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        contenido = f.read()
    assert "Inicio del flujo principal" in contenido, "❌ Log incompleto"
    print("✅ Log generado correctamente")

# --- Verificación de archivado automático con logging ---
def verificar_archivado(estructura):
    logging.info("🔍 Iniciando verificación de archivado automático post-ejecución")
    resumen = procesar_archivos(estructura)

    errores = [r for r in resumen if "error" in r]
    exitosos = [r for r in resumen if "destino" in r]

    print(f"✅ Archivos archivados correctamente: {len(exitosos)}")
    print(f"⚠️ Archivos con errores: {len(errores)}")

    for r in exitosos:
        logging.info(f"Archivo archivado: {r['archivo']} → {r['destino']} (Cuenta: {r['cuenta']}, Categoría: {r['categoria']})")

    for r in errores:
        logging.warning(f"Error al archivar: {r['archivo']} → {r['error']} (Cuenta: {r.get('cuenta')}, Categoría: {r.get('categoria')})")

# --- Punto de entrada ---
if __name__ == "__main__":
    print("🧪 Iniciando verificación post-ejecución...\n")

    estructura = cargar_estructura()
    categorias = set(cat for lista in estructura.values() for cat in lista)

    # Detectar cuentas procesadas dinámicamente
    cuentas_detectadas = [
        nombre for nombre in os.listdir(BASE_PATH)
        if os.path.isdir(os.path.join(BASE_PATH, nombre))
    ]

    verificar_estructura(cuentas_detectadas, categorias)
    verificar_archivos_movidos(cuentas_detectadas, categorias)
    verificar_resumen()
    verificar_historial()
    verificar_log()
    verificar_archivado(estructura)

    print("\n🎉 Verificación completa: todo está en orden.")