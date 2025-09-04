# 📘 Automatización Documental V1  
Sistema modular para el archivado automático, validación técnica y trazabilidad de documentos por cliente y categoría. Diseñado para garantizar robustez, claridad y cumplimiento normativo en entornos documentales exigentes.

## 🚀 Objetivo del sistema  
- Clasificar y archivar documentos por número de cuenta y categoría  
- Validar rutas, permisos y configuración antes de ejecutar  
- Renombrar automáticamente según nomenclatura oficial  
- Generar resumen en Excel y actualizar historial  
- Enviar alertas automáticas por email con adjuntos  
- Blindar el sistema contra errores silenciosos y asegurar trazabilidad total  

## 🧩 Estructura del proyecto  
automatizacion_documental_v1/  
├── config/                  # Archivos de configuración (.ini, .json)  
├── logs/                   # Registro estructurado de eventos  
├── scripts/                # Módulos funcionales  
├── resumen_archivo.xlsx    # Resumen generado  
├── historial_archivo.xlsx  # Historial acumulativo  
├── main.py                 # Flujo principal  
├── verificar_resultados.py # Verificación post-ejecución  
├── test_main.py            # Tests unificados  
└── README.md               # Documentación  

## ⚙️ Módulos principales  
| Módulo                        | Función |
|------------------------------|---------|
| `config_loader.py`           | Carga y valida `config.ini` |
| `estructura_subcarpetas.py`  | Carga estructura desde `estructura.json` |
| `preprocesar_nombres.py`     | Renombra archivos según nomenclatura oficial |
| `archivado_automatico.py`    | Mueve archivos por cuenta y categoría |
| `verificar_resultados.py`    | Ejecuta flujo completo y verifica trazabilidad |
| `verificar_permisos_ruta.py` | Valida permisos de carpetas |
| `seguridad_v2.py`            | Verifica entorno, dependencias y hash |
| `generar_resumen_excel.py`   | Genera resumen desde cero |
| `actualizar_resumen.py`      | Actualiza resumen existente |
| `historial_archivo.py`       | Registra eventos en historial |
| `alertas_email.py`           | Envía alertas con adjunto |

## 🧪 Ejecución del sistema  
```bash
python scripts/verificar_resultados.py

Este script realiza:
- Renombrado automático de archivos en Docupen
- Archivado por cuenta y categoría
- Verificación de estructura y movimientos
- Validación de resumen, historial y log
- Registro técnico en registro.log
- Envío de alerta (si está activado)

Ejemplo de estructura esperada
Legajos/
└── 14959/
    ├── 01. CAC/
    ├── 05. DJTCS/
    ├── 08. CONSTANCIAS/
    │   ├── SOCIEDAD/
    │   │   └── 2025/
    │   │       └── 08.- 14959 CUIT SOCIEDAD 04-09-2025.pdf
    │   ├── REPRESENTANTE LEGAL/
    │   │   └── 2025/
    │   │       └── 08.- 14959 CUIT RL 04-09-2025.pdf
    │   ├── BENEFICIARIOS FINALES/
    │   │   └── 2025/
    │   │       └── 08.- 14959 CUIT BF JUAN PEREZ 04-09-2025.pdf

  🧠 Lógica documental
Archivado por prefijo numérico
El sistema detecta el número de subcarpeta directamente desde el nombre del archivo (ej. , ) y lo utiliza para determinar la carpeta de destino dentro de la cuenta. Si el prefijo es , se activa una lógica especial para constancias.
Archivado especial para 
• 	Detecta si el documento corresponde a SOCIEDAD, REPRESENTANTE LEGAL o BENEFICIARIO FINAL
• 	Extrae el año desde la fecha del archivo
• 	Crea subcarpetas por tipo y año si no existen
• 	Mueve el archivo al destino correspondiente con trazabilidad

🧠 Ejemplo de nombre válido
08.- 14959 CUIT BF JUAN PEREZ 04-09-2025.pdf
Se interpreta como:
• 	Prefijo: 08. → activa lógica de constancias
• 	Cuenta: 14959
• 	Tipo documental: CUIT BF JUAN PEREZ 
• 	Fecha: 04-09-2025 → convertida internamente a 04092025
• 	Subcarpeta destino: 08.CONSTANCIAS/BENEFICIARIOS FINALES/2025

📬 Envío de alertas
• 	Activar en  → 
• 	Definir destinatario → 
🔐 Seguridad
• 	Validación de entorno (Python 3.8+)
• 	Verificación de dependencias (, )
• 	Validación de hash SHA-256 para archivos críticos
🧪 Tests
python test_main.py

Cubre:
• 	Configuración
• 	Permisos
• 	Estructura
• 	Logging
• 	Historial
• 	Hash
• 	Flujo completo

📊 Verificación post-ejecución
Usar verificar_resultados.py para validar:
- Renombrado automático aplicado
- Estructura de carpetas creada
- Archivos movidos correctamente
- Resumen generado
- Historial actualizado
- Log técnico generado
- Archivos pendientes detectados

📌 Convenciones de commits
• 	 nueva funcionalidad
• 	 corrección de bug
• 	 mejora interna sin cambiar funcionalidad
• 	 cambios en documentación
• 	 mejoras o nuevos tests

📝 Autoría
Desarrollado por Alejandra, con enfoque en automatización robusta, validación modular y trazabilidad documental.

Este proyecto está en evolución constante, con mejoras iterativas basadas en pruebas reales y feedback técnico.




