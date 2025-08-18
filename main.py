from scripts.seguridad_v2 import (
    verificar_entorno,
    verificar_dependencias,
    verificar_permisos,
    verificar_hash
)

from scripts.verificacion_seguridad import verificar_entorno
from scripts.estructura_subcarpetas import cargar_estructura, crear_subcarpetas_para_cuenta
from scripts.archivado_automatico import procesar_archivos
from scripts.generar_resumen_excel import actualizar_resumen
from scripts.alertas_email import enviar_alerta

def main():
    verificar_entorno()
    estructura = cargar_estructura()
    resumen_data = procesar_archivos(estructura)
    actualizar_resumen(resumen_data)
    enviar_alerta("resumen_archivo.xlsx")

if __name__ == "__main__":
    main()