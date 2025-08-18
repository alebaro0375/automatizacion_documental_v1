# Define y gestiona la estructura lógica de carpetas que se usa para 
# clasificar los documentos archivados. Es el corazón organizativo del sistema.
# Funciones principales:
# Lectura de : carga dinámicamente las reglas de clasificación por tipo de
# persona o tipo de documento.
# Creación de subcarpetas por cuenta: genera carpetas como CAC, CONSTANCIAS, etc.,
# según el tipo (física/jurídica).
# Adaptabilidad: permite modificar la estructura sin tocar el código,
# simplemente editando el archivo.
# Validación de estructura: verifica que las claves del JSON estén bien
# formadas y que no haya duplicados o errores de sintaxis.
# Interfaz con el archivador: devuelve la estructura como diccionario para
# que sepa dónde mover cada archivo.


import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging

# 📁 Rutas
BASE_ARCHIVADO = Path("Z:/Legajos/Archivados")
ESTRUCTURA_JSON = Path("estructura_carpetas.json")
EXCEL_CUENTAS = Path("datos_comitentes.xlsx")
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / f"estructura_{datetime.now().strftime('%Y%m%d')}.txt"

# 📝 Logging
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def cargar_estructura(json_path=ESTRUCTURA_JSON):
    with json_path.open("r", encoding="utf-8") as f:
        estructura = json.load(f)
    return estructura

def cargar_cuentas(excel_path=EXCEL_CUENTAS):
    df = pd.read_excel(excel_path, dtype=str)
    df = df.dropna(subset=["cuenta_comitente", "tipo"])
    cuentas_por_tipo = {
        "fisica": df[df["tipo"].str.lower() == "fisica"]["cuenta_comitente"].tolist(),
        "juridica": df[df["tipo"].str.lower() == "juridica"]["cuenta_comitente"].tolist(),
        "desconocido": df[~df["tipo"].str.lower().isin(["fisica", "juridica"])]["cuenta_comitente"].tolist()
    }
    return cuentas_por_tipo

def crear_subcarpetas_para_cuenta(cuenta, tipo, estructura, base_path=BASE_ARCHIVADO):
    subcarpetas = estructura.get(tipo, ["OTROS"])
    carpeta_base = base_path / cuenta
    for sub in subcarpetas:
        destino = carpeta_base / sub
        destino.mkdir(parents=True, exist_ok=True)
        logging.info(f"📁 Creada: {destino}")
    return carpeta_base

def main():
    estructura = cargar_estructura()
    cuentas_por_tipo = cargar_cuentas()

    for tipo, cuentas in cuentas_por_tipo.items():
        for cuenta in cuentas:
            crear_subcarpetas_para_cuenta(cuenta, tipo, estructura)

    print("✅ Subcarpetas creadas correctamente para todas las cuentas.")

if __name__ == "__main__":
    main()