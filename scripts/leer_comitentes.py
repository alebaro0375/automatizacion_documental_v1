import pandas as pd
from collections import defaultdict

def leer_comitentes(path_excel):
    """
    Lee el Excel de comitentes y genera dos estructuras:
    - cuentas_info: dict con info por cuenta comitente
    - cuit_to_cuentas: dict inverso con CUIT como clave y lista de cuentas asociadas
    """
    df = pd.read_excel(path_excel, dtype=str).fillna("")

    cuentas_info = {}
    cuit_to_cuentas = defaultdict(list)

    for _, row in df.iterrows():
        cuenta = row["Cuenta"]
        cuit = row["CUIT"]
        tipo = row["Tipo"]  # Físico / Jurídico
        nombre = row["Nombre"]

        cuentas_info[cuenta] = {
            "CUIT": cuit,
            "Tipo": tipo,
            "Nombre": nombre
        }

        cuit_to_cuentas[cuit].append(cuenta)

    return cuentas_info, dict(cuit_to_cuentas)