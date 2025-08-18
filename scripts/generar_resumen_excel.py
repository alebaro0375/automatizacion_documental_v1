import openpyxl
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

ENCABEZADOS = [
    "Cuenta", "CUIT / CUIL", "Nombre / Razón Social",
    "Fecha de Archivo", "Tipo de Documento", "Subcarpeta", "Ruta Relativa"
]

def generar_resumen(datos, archivo_excel, ruta_base_alternativa=None):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resumen Archivos"

    # Agregar encabezados
    ws.append(ENCABEZADOS)
    for col in range(1, len(ENCABEZADOS) + 1):
        ws.cell(row=1, column=col).font = Font(bold=True)

    # Agregar filas con hipervínculos
    for fila in datos:
        ruta_relativa = fila["ruta_relativa"]
        ruta_completa = (
            ruta_base_alternativa.rstrip("/") + "/" + ruta_relativa.replace("\\", "/")
            if ruta_base_alternativa else ruta_relativa
        )

        nueva_fila = [
            fila["cuenta"],
            fila["cuit_cuil"],
            fila["nombre"],
            fila["fecha_archivo"],
            fila["tipo_documento"],
            fila["subcarpeta"],
            ruta_relativa  # texto visible
        ]
        ws.append(nueva_fila)

        # Insertar hipervínculo en la última celda
        celda = ws.cell(row=ws.max_row, column=7)
        celda.hyperlink = ruta_completa
        celda.font = Font(color="0000FF", underline="single")

    # Ajustar ancho de columnas
    for col in range(1, len(ENCABEZADOS) + 1):
        ws.column_dimensions[get_column_letter(col)].width = 20

    wb.save(archivo_excel)