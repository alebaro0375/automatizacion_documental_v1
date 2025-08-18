import os
import hashlib
import logging
import smtplib
from email.message import EmailMessage

# Configuración
LOG_PATH = "logs/seguridad.log"
HASH_REGISTRO = "config/hashes_validos.txt"
CORREO_ALERTA = "soporte@empresa.com"
SMTP_SERVER = "smtp.empresa.com"

# Inicializar logging seguro
def inicializar_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

# Verificar entorno básico
def verificar_entorno():
    print("🔍 Verificando entorno...")
    inicializar_logging()
    os.makedirs("logs", exist_ok=True)
    logging.info("Entorno verificado: carpeta de logs creada")

# Validar nombre seguro (sin caracteres especiales)
def es_nombre_seguro(nombre):
    seguro = nombre.isalnum()
    if not seguro:
        logging.warning(f"Nombre inseguro detectado: {nombre}")
    return seguro

# Verificar permisos de lectura/escritura
def verificar_permisos(path):
    lectura = os.access(path, os.R_OK)
    escritura = os.access(path, os.W_OK)
    if not lectura or not escritura:
        logging.error(f"Permisos insuficientes en: {path}")
    return lectura and escritura

# Verificar dependencias críticas
def verificar_dependencias():
    try:
        import pandas, openpyxl, selenium
        logging.info("Dependencias críticas OK")
        return True
    except ImportError as e:
        logging.critical(f"Falta dependencia: {e.name}")
        enviar_alerta(f"Dependencia faltante: {e.name}")
        return False

# Calcular hash SHA256
def calcular_hash(path):
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

# Verificar hash contra registro
def verificar_hash(path):
    hash_actual = calcular_hash(path)
    if not os.path.exists(HASH_REGISTRO):
        logging.warning(f"No se encontró el registro de hashes: {HASH_REGISTRO}")
        return True  # no se puede validar

    with open(HASH_REGISTRO, "r") as f:
        hashes_validos = set(line.strip() for line in f if line.strip())

    if hash_actual in hashes_validos:
        logging.info(f"Hash verificado para {path}")
        return True
    else:
        logging.error(f"Hash inválido para {path}: {hash_actual}")
        enviar_alerta(f"⚠️ Archivo alterado: {path}")
        return False

# Enviar alerta por correo
def enviar_alerta(mensaje, destino=CORREO_ALERTA):
    try:
        msg = EmailMessage()
        msg.set_content(mensaje)
        msg["Subject"] = "⚠️ Alerta de seguridad"
        msg["From"] = "sistema@empresa.com"
        msg["To"] = destino

        with smtplib.SMTP(SMTP_SERVER) as server:
            server.send_message(msg)
        logging.info(f"Alerta enviada a {destino}")
    except Exception as e:
        logging.error(f"No se pudo enviar alerta: {e}")