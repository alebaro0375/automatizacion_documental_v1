import hashlib
import json
import os

HASH_REGISTRO = "scripts/hashes_registrados.json"

def calcular_hash_archivo(ruta):
    sha256 = hashlib.sha256()
    with open(ruta, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def cargar_hashes():
    if os.path.exists(HASH_REGISTRO):
        with open(HASH_REGISTRO, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def guardar_hashes(hashes):
    with open(HASH_REGISTRO, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2, ensure_ascii=False)

def es_duplicado(hash_actual, hashes_existentes):
    return hash_actual in hashes_existentes.values()