# 📘 Automatización Documental V1

Sistema modular para el archivado automático, validación técnica y trazabilidad de documentos por cliente y categoría. Diseñado para garantizar robustez, claridad y cumplimiento normativo en entornos documentales exigentes.

---

## 🚀 Objetivo del sistema

- Clasificar y archivar documentos por número de cuenta y categoría.
- Validar rutas, permisos y configuración antes de ejecutar.
- Generar resumen en Excel y actualizar historial.
- Enviar alertas automáticas por email con adjuntos.
- Blindar el sistema contra errores silenciosos y asegurar trazabilidad total.

---

## 🧩 Estructura del proyecto

```
automatizacion_documental_v1/
├── config/                  # Archivos de configuración (.ini, .json)
├── logs/                   # Registro estructurado de eventos
├── scripts/                # Módulos funcionales
├── templates/              # Plantillas (si aplica)
├── resumen_archivo.xlsx    # Resumen generado
├── historial_archivo.xlsx  # Historial acumulativo
├── main.py                 # Flujo principal
├── test_main.py            # Tests unificados
└── README.md               # Documentación
```

---

## ⚙️ Módulos principales

| Módulo                        | Función |
|------------------------------|---------|
| `config_loader.py`           | Carga y valida `config.ini` |
| `estructura_subcarpetas.py`  | Carga estructura desde `estructura.json` |
| `archivado_automatico.py`    | Mueve archivos por cuenta y categoría |
| `verificar_permisos_ruta.py` | Valida permisos de carpetas |
| `seguridad_v2.py`            | Verifica entorno, dependencias y hash |
| `generar_resumen_excel.py`   | Genera resumen desde cero |
| `actualizar_resumen.py`      | Actualiza resumen existente |
| `historial_archivo.py`       | Registra eventos en historial |
| `alertas_email.py`           | Envía alertas con adjunto |

---

## 🧪 Ejecución del sistema

```bash
python main.py
```

El sistema realiza:

1. Validación de configuración y permisos  
2. Verificación de entorno y seguridad  
3. Procesamiento de archivos  
4. Actualización de historial  
5. Generación o actualización de resumen  
6. Envío de alerta (si está activado)

---

## 📦 Ejemplo de estructura esperada

```
Legajos/Archivados/
└── 123456/
    ├── 01. CAC/
    ├── 02. ESTATUTO-CONTRATO SOCIAL/
    └── ...
```

---

## 📬 Envío de alertas

- Activar en `[EMAIL]` → `activar_alertas = True`
- Definir destinatario → `destinatario = ejemplo@dominio.com`

---

## 🔐 Seguridad

- Validación de entorno (Python 3.8+)
- Verificación de dependencias (`openpyxl`, `pandas`)
- Validación de hash SHA-256 para archivos críticos

---

## 🧪 Tests

```bash
python test_main.py
```

Cubre:

- Configuración  
- Permisos  
- Estructura  
- Logging  
- Historial  
- Hash  
- Flujo completo

---

## 📊 Verificación post-ejecución

Usar `verificar_resultados.py` para validar:

- Estructura de carpetas  
- Archivos movidos  
- Resumen generado  
- Historial actualizado  
- Log completo  
- Hash de integridad

---

## 📌 Convenciones de commits

- `feat:` nueva funcionalidad  
- `fix:` corrección de bug  
- `refactor:` mejora interna sin cambiar funcionalidad  
- `docs:` cambios en documentación  
- `test:` mejoras o nuevos tests

## 📝 Autoría

Desarrollado por Alejandra, con enfoque en automatización robusta, validación modular y trazabilidad documental.  
Este proyecto está en evolución constante, con mejoras iterativas basadas en pruebas reales y feedback técnico.