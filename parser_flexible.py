import re
from datetime import datetime
import os

def extraer_datos_flexibles(nombre_archivo):
    nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
    nombre_sin_ext = re.sub(r"\s+", " ", nombre_sin_ext).strip()
    partes = nombre_sin_ext.split(" ")

    # Detectar si hay prefijo
    prefijo = partes[0] if partes[0].endswith(".") or partes[0].endswith(".-") else None
    offset = 1 if prefijo else 0

    try:
        nro_cuenta = partes[offset]
        if not nro_cuenta.isdigit():
            return None, None, None, None

        # Buscar fecha válida
        fecha = None
        for parte in reversed(partes):
            if re.match(r"\d{2}-\d{2}-\d{4}", parte):
                fecha = parte.replace("-", "")
                break

        if not fecha:
            fecha = datetime.now().strftime("%d%m%Y")
            print(f"🕒 Fecha asignada automáticamente para '{nombre_archivo}': {fecha}")

        # Construir nombre documental desde el resto
        nombre_doc = " ".join(partes[offset + 1:]).replace(fecha, "").strip()

        return nro_cuenta, nombre_doc, prefijo, fecha

    except Exception as e:
        print(f"❌ Error al parsear '{nombre_archivo}': {e}")
        return None, None, None, None