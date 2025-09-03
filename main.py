import os

# --- Importación de módulos ---
from scripts.config_loader import cargar_configuracion
from scripts.verificar_permisos_ruta import verificar_permisos
from scripts.seguridad_v2 import (
    verificar_entorno,
    verificar_dependencias,
    verificar_hash
)
from scripts.archivado_automatico import procesar_archivos
from scripts.generar_resumen_excel import generar_resumen
from scripts.actualizar_resumen import actualizar_resumen
from scripts.historial_archivo import actualizar_historial
from scripts.alertas_email import enviar_alerta

# --- Validación de configuración ---
def validar_configuracion_interna(config):
    for seccion in ["RUTAS", "ARCHIVO", "SEGURIDAD", "EMAIL"]:
        if seccion not in config:
            raise ValueError(f"Falta la sección [{seccion}] en config.ini")

    carpeta_origen = config.get("ARCHIVO", "carpeta_origen", fallback="")
    if not carpeta_origen or not os.path.exists(carpeta_origen):
        raise FileNotFoundError(f"Carpeta de origen inválida o inexistente: {carpeta_origen}")
    verificar_permisos(carpeta_origen)

    rutas = [
        config.get("RUTAS", "directorio_base", fallback=""),
        config.get("RUTAS", "estructura_json", fallback=""),
        config.get("RUTAS", "log_path", fallback="")
    ]
    for ruta in rutas:
        if not ruta or not os.path.exists(os.path.dirname(ruta)):
            raise FileNotFoundError(f"Ruta inválida o carpeta inexistente: {ruta}")

    tipos = config.get("ARCHIVO", "tipo_cliente", fallback="").split(",")
    if not all(t.strip().lower() in ["juridico", "fisico"] for t in tipos):
        raise ValueError(f"Tipo de cliente inválido: {tipos}")

    for clave in [("SEGURIDAD", "validar_hash"), ("EMAIL", "activar_alertas")]:
        try:
            config.getboolean(*clave)
        except ValueError:
            raise ValueError(f"Valor booleano inválido en {clave}")

    if not config.get("EMAIL", "destinatario", fallback=""):
        raise ValueError("Falta destinatario en sección [EMAIL]")

    print("✅ Configuración validada correctamente.")

# --- Manejo inteligente del resumen ---
RUTA_RESUMEN = "./resumen_archivo.xlsx"

def manejar_resumen(resumen_data):
    if os.path.exists(RUTA_RESUMEN):
        print("📄 Resumen existente detectado. Actualizando...")
        actualizar_resumen(resumen_data, RUTA_RESUMEN)
    else:
        print("📄 No hay resumen previo. Generando desde cero...")
        generar_resumen(resumen_data, RUTA_RESUMEN)

# --- Flujo principal del sistema ---
def ejecutar_flujo_principal():
    config = cargar_configuracion("config/config.ini")
    validar_configuracion_interna(config)

    verificar_entorno()
    verificar_dependencias()

    if config.getboolean("SEGURIDAD", "validar_hash"):
        verificar_hash("scripts/archivado_automatico.py")

    resumen_data = procesar_archivos()

    actualizar_historial(resumen_data, "historial_archivo.xlsx")
    manejar_resumen(resumen_data)

    if config.getboolean("EMAIL", "activar_alertas", fallback=False):
        enviar_alerta(resumen_path=RUTA_RESUMEN, destinatario=config.get("EMAIL", "destinatario"))
    else:
        print("📭 Alerta desactivada por configuración")

# --- Punto de entrada ---
if __name__ == "__main__":
    ejecutar_flujo_principal()
    print("✅ main.py se ejecutó correctamente")