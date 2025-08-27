from configparser import ConfigParser
import os

def cargar_configuracion(ruta_config):
    if not os.path.exists(ruta_config):
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {ruta_config}")

    config = ConfigParser()
    config.read(ruta_config, encoding="utf-8")

    if "RUTAS" not in config or "directorio_base" not in config["RUTAS"]:
        raise ValueError("La configuración debe incluir la sección [RUTAS] con la clave 'directorio_base'.")

    return config