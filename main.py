import os

# --- Importación de módulos ---
from scripts.config_loader import cargar_configuracion
from scripts.verificar_permisos_ruta import verificar_permisos
from scripts.seguridad_v2 import (
    verificar_entorno,
    verificar_dependencias,
    verificar_hash
)
from scripts.estructura_subcarpetas import cargar_estructura, crear_subcarpetas_para_cuenta
from scripts.archivado_automatico import procesar_archivos
from scripts.generar_resumen_excel import generar_resumen
from scripts.actualizar_resumen import actualizar_resumen
from scripts.historial_archivo import actualizar_historial
from scripts.alertas_email import enviar_alerta

# --- Validación de configuración ---
def validar_configuracion_interna(config):
    # Validar secciones mínimas
    for seccion in ["RUTAS", "ARCHIVO", "SEGURIDAD", "EMAIL"]:
        if seccion not in config:
            raise ValueError(f"Falta la sección [{seccion}] en config.ini")

    # Validar carpeta de origen
    carpeta_origen = config.get("ARCHIVO", "carpeta_origen", fallback="")
    if not carpeta_origen or not os.path.exists(carpeta_origen):
        raise FileNotFoundError(f"Carpeta de origen inválida o inexistente: {carpeta_origen}")
    verificar_permisos(carpeta_origen)

    # Validar rutas críticas
    rutas = [
        config.get("RUTAS", "directorio_base", fallback=""),
        config.get("RUTAS", "estructura_json", fallback=""),
        config.get("RUTAS", "log_path", fallback="")
    ]
    for ruta in rutas:
        if not ruta or not os.path.exists(os.path.dirname(ruta)):
            raise FileNotFoundError(f"Ruta inválida o carpeta inexistente: {ruta}")

    # Validar tipos de cliente
    tipos = config.get("ARCHIVO", "tipo_cliente", fallback="").split(",")
    if not all(t.strip() in ["juridico", "fisico"] for t in tipos):
        raise ValueError(f"Tipo de cliente inválido: {tipos}")

    # Validar booleanos
    for clave in [("SEGURIDAD", "validar_hash"), ("EMAIL", "activar_alertas")]:
        try:
            config.getboolean(*clave)
        except ValueError:
            raise ValueError(f"Valor booleano inválido en {clave}")

    # Validar destinatario de email
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
    # Paso 1: Cargar configuración
    config = cargar_configuracion("config/config.ini")
    validar_configuracion_interna(config)

    # Paso 2: Validar entorno y dependencias
    verificar_entorno()
    verificar_dependencias()

    # Paso 3: Verificar integridad si está activado
    if config.getboolean("SEGURIDAD", "validar_hash"):
        verificar_hash("scripts/archivado_automatico.py")

    # Paso 4: Cargar estructura y procesar archivos
    estructura = cargar_estructura()
    resumen_data = procesar_archivos(estructura)

    # Paso 5: Actualizar historial
    actualizar_historial(resumen_data, "historial_archivo.xlsx")

    # Paso 6: Generar o actualizar resumen
    manejar_resumen(resumen_data)

    # Paso 7: Enviar alerta si está activado
    if config.getboolean("EMAIL", "activar_alertas", fallback=False):
       enviar_alerta(resumen_path=RUTA_RESUMEN, destinatario=config.get("EMAIL", "destinatario"))
    else: 
        print("📭 Alerta desactivada por configuración")

# --- Punto de entrada ---
if __name__ == "__main__":
    ejecutar_flujo_principal()
    print("✅ main.py se ejecutó correctamente")