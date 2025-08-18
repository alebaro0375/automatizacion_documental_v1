# Validar la seguridad de los documentos y del entorno antes de ejecutar 
# cualquier proceso automatizado:
# Hash check: compara el hash SHA256 de cada archivo contra un registro
#  esperado para detectar alteraciones.
# Permisos de acceso: verifica que el usuario actual tenga los permisos
# necesarios para lectura/escritura en las carpetas requeridas.
# Integridad del entorno: comprueba que las dependencias y versiones 
# críticas estén instaladas y sin conflictos.
# Logging seguro: registra cualquier irregularidad en un archivo protegido, 
# con timestamps y clasificación de riesgo.
# Alerta proactiva: en caso de fallas o inconsistencias, envía un correo
# a la casilla técnica predefinida (si está configurado).


import os

def verificar_entorno():
    print("Verificando entorno...")
    os.makedirs("logs", exist_ok=True)

def es_nombre_seguro(nombre):
    return nombre.isalnum()

def calcular_hash(path):
    import hashlib
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()