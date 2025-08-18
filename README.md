# 📁 LegajosAutomation

Automatización modular para archivar documentos de clientes, generar resúmenes en Excel y enviar alertas por correo electrónico.

---

## ⚙️ Componentes Principales

| Script                      | Función                                                                 |
|----------------------------|-------------------------------------------------------------------------|
| `main.py`                  | Orquestador del flujo completo                                          |
| `verificacion_seguridad.py`| Verifica entorno, permisos y nombres seguros                            |
| `estructura_subcarpetas.py`| Carga estructura de carpetas desde archivo JSON                         |
| `archivado_automatico.py`  | Clasifica y mueve archivos según tipo                                   |
| `generar_resumen_excel.py` | Genera resumen de archivos en formato Excel                             |
| `alertas_email.py`         | Envía correo con resumen adjunto                                        |

---

## 🧩 Archivos de Configuración

- `estructura_carpetas.json`: Define subcarpetas por tipo de documento
- `config.json` *(opcional)*: Parámetros como rutas, email, y opciones de ejecución
- `resumen_archivo.xlsx`: Archivo generado con el resumen de documentos
- `logs/`: Carpeta para registros de ejecución y errores

---

## 🚀 Ejecución

```bash
python main.py