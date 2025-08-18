# LegajosAutomation

Automatización modular para archivar documentos de clientes, generar resúmenes en Excel y enviar alertas por correo.

# Estructura

- `main.py`: Ejecuta todo el flujo.
- `verificacion_seguridad.py`: Verifica entorno y nombres seguros.
- `estructura_subcarpetas.py`: Carga estructura desde JSON.
- `archivado_automatico.py`: Mueve archivos según tipo.
- `generar_resumen_excel.py`: Crea resumen en Excel.
- `alertas_email.py`: Envía correo con resumen adjunto.

# Configuración

- `estructura_carpetas.json`: Define subcarpetas por tipo.
- `resumen_archivo.xlsx`: Archivo generado con el resumen.
- `logs/`: Carpeta para logs (puede expandirse).
- `config.json`: (opcional) para parámetros como email, rutas, etc.

# Ejecución

```bash
python main.py