import os

def verificar_permisos(path):
    """
    Verifica que la ruta exista y tenga permisos de lectura y escritura.
    Lanza excepciones claras si algo falla.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"La ruta '{path}' no existe.")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"No hay permisos de lectura en '{path}'.")
    if not os.access(path, os.W_OK):
        raise PermissionError(f"No hay permisos de escritura en '{path}'.")
    return True