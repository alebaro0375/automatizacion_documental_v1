import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging

# Rutas absolutas
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
LOG_DIR = BASE_DIR / "logs"

BASE_ARCHIVADO = Path("C:/Legajos/Archivados")
ESTRUCTURA_JSON = CONFIG_DIR / "estructura_carpetas.json"
EXCEL_CUENTAS = CONFIG_DIR / "datos_comitentes.xlsx"
LOG_FILE = LOG_DIR / f"estructura_{datetime.now().strftime('%Y%m%d')}.txt"

# Logging
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# Validación de existencia de archivos
def validar_archivos():
    if not ESTRUCTURA_JSON.exists():
        raise FileNotFoundError(f"❌ No se encontró el archivo de estructura: {ESTRUCTURA_JSON}")
    if not EXCEL_CUENTAS.exists():
        raise FileNotFoundError(f"❌ No se encontró el archivo de comitentes: {EXCEL_CUENTAS}")

# Cargar estructura desde JSON
def cargar_estructura(json_path=ESTRUCTURA_JSON):
    with json_path.open("r", encoding="utf-8") as f:
        estructura = json.load(f)
    return estructura

# Cargar cuentas desde Excel
def cargar_cuentas(excel_path=EXCEL_CUENTAS):
    df = pd.read_excel(excel_path, dtype=str)
    df = df.dropna(subset=["cuenta_comitente", "tipo"])
    cuentas_por_tipo = {
        "fisica": df[df["tipo"].str.lower() == "fisica"]["cuenta_comitente"].tolist(),
        "juridica": df[df["tipo"].str.lower() == "juridica"]["cuenta_comitente"].tolist(),
        "desconocido": df[~df["tipo"].str.lower().isin(["fisica", "juridica"])]["cuenta_comitente"].tolist()
    }
    return cuentas_por_tipo

# Crear subcarpetas por cuenta
def crear_subcarpetas_para_cuenta(cuenta, tipo, estructura, base_path=BASE_ARCHIVADO):
    subcarpetas = estructura.get(tipo, ["OTROS"])
    carpeta_base = base_path / cuenta
    for sub in subcarpetas:
        destino = carpeta_base / sub
        destino.mkdir(parents=True, exist_ok=True)
        logging.info(f"📁 Creada: {destino}")
    return carpeta_base

# Ejecución directa
def main():
    validar_archivos()
    estructura = cargar_estructura()
    cuentas_por_tipo = cargar_cuentas()

    for tipo, cuentas in cuentas_por_tipo.items():
        for cuenta in cuentas:
            crear_subcarpetas_para_cuenta(cuenta, tipo, estructura)

    print("✅ Subcarpetas creadas correctamente para todas las cuentas.")

if __name__ == "__main__":
    main()