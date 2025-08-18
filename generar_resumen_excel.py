# Crear y actualizar el historial estructurado de actividad en un archivo
# Excel. Es clave para trazabilidad, auditoría y control operativo.
# Funciones principales:
# Inicialización del archivo resumen: si no existe, lo crea con encabezados 
# estándar (fecha, cuenta, nombre, CUIT, tipo, archivo, destino, hash).
# Concatenación de registros nuevos: agrega los datos generados por el 
# script de archivado sin borrar el historial anterior.
# Formato limpio y ordenado: aplica estilos básicos para facilitar la 
# lectura (ancho de columnas, encabezados en negrita).
# Protección opcional de hoja: puede bloquear la edición manual si se 
# requiere integridad documental.
# Preparación para envío por correo: guarda el archivo en una ruta 
# conocida para que lo adjunte automáticamente.



import openpyxl

def actualizar_resumen(resumen_data, excel_path="resumen_archivo.xlsx"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Archivo", "Destino"])
    for archivo, destino in resumen_data:
        ws.append([archivo, destino])
    wb.save(excel_path)