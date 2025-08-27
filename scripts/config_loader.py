#  Validar la integridad de archivos mediante hash SHA-256.
# • Calcula el hash de cualquier archivo binario
# • Permite validar integridad sin acoplarse al flujo principal
# • Lanza excepciones claras si el archivo no existe

import configparser
import hashlib
import os

def cargar_configuracion(ruta_config):
    """
    Carga y valida el archivo de configuración INI.
    Verifica existencia, formato y secciones requeridas.
    """
    if not os.path.exists(ruta_config):
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {ruta_config}")

    config = configparser.ConfigParser()
    config.read(ruta_config, encoding="utf-8")

    # Validación de secciones mínimas
    secciones_requeridas = ["RUTAS", "ARCHIVO", "SEGURIDAD", "EMAIL", "GENERAL"]
    for seccion in secciones_requeridas:
        if seccion not in config:
           raise ValueError(f"Falta la sección '{seccion}' en el archivo de configuración.")

    # Validación de claves esperadas (ejemplo)
    claves_general = ["modo_ejecucion", "log_nivel"]
    for clave in claves_general:
        if clave not in config["GENERAL"]:
            raise ValueError(f"Falta la clave '{clave}' en la sección [General].")

    return config

def calcular_hash_sha256(ruta_archivo):
    """
    Calcula el hash SHA-256 de un archivo dado.
    Lanza excepción si el archivo no existe.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")

    with open(ruta_archivo, "rb") as f:
        contenido = f.read()
        return hashlib.sha256(contenido).hexdigest()
    
import os 

def validar_hash(ruta_archivo, hash_esperado):
    """
    Compara el hash real del archivo con el esperado.
    Retorna True si coinciden, False si no.
    """
    hash_real = calcular_hash_sha256(ruta_archivo)
    return hash_real == hash_esperado