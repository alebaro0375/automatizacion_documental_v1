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
1. 	Renombrado automático de archivos en 
2. 	Archivado por cuenta y categoría
3. 	Verificación de estructura y movimientos
4. 	Validación de resumen, historial y log
5. 	Registro técnico en 
6. 	Envío de alerta (si está activado)
📦 Ejemplo de estructura esperada
Legajos/Archivados/
└── 8721/
├── 01. CAC/
├── 05. DJTCS/
└── ...
🧠 Ejemplo de nombre válido
8721 T. CAC 03-09-2025.pdf
Se interpreta como:
• 	Cuenta: 
• 	Tipo: 
• 	Nombre: 
• 	Fecha:  → convertida internamente a 
📬 Envío de alertas
• 	Activar en  → 
• 	Definir destinatario → 
🔐 Seguridad
• 	Validación de entorno (Python 3.8+)
• 	Verificación de dependencia
• 	Validación de hash SHA-256 para archivos críticos   
🧪 Tests
Cubre:
• 	Configuración
• 	Permisos
• 	Estructura
• 	Logging
• 	Historial
• 	Hash
• 	Flujo completo
📊 Verificación post-ejecución
Usar  para validar:
• 	Renombrado automático aplicado
• 	Estructura de carpetas creada
• 	Archivos movidos correctamente
• 	Resumen generado
• 	Historial actualizado
• 	Log técnico generado
• 	Archivos pendientes detectados

📝 Autoría
Desarrollado por Alejandra, con enfoque en automatización robusta, validación modular y trazabilidad documental.
Este proyecto está en evolución constante, con mejoras iterativas basadas en pruebas reales y feedback técnico.
