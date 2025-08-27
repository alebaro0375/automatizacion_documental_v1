#• 	Configuración (config.ini)
#• 	Estructura de carpetas (estructura.json)
#• 	Validaciones de nombres
#• 	Ejecución del flujo principal
#• 	Logging
#• 	Hash de archivos (config_loader.py)
#• 	Historial de eventos (historial_archivo.py)
#• 	Permisos de carpeta
#• 	Cobertura de errores comunes

import os
import json
import shutil
import tempfile
import hashlib
import unittest
from configparser import ConfigParser
from scripts.config_loader import cargar_configuracion
from scripts.estructura_subcarpetas import cargar_estructura
from scripts.main import ejecutar_flujo_principal
from scripts.seguridad_v2 import calcular_hash_sha256, validar_hash
from scripts.historial_archivo import actualizar_historial
from scripts.verificar_permisos_ruta import verificar_permisos

class TestMainWorkflow(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.test_dir, "config.ini")
        self.estructura_path = os.path.join(self.test_dir, "estructura.json")
        self.log_path = os.path.join(self.test_dir, "registro.log")
        self.historial_path = os.path.join(self.test_dir, "historial.json")

        config = ConfigParser()
        config["RUTAS"] = {
            "directorio_base": self.test_dir,
            "estructura_json": self.estructura_path,
            "log_path": self.log_path
        }
        config["ARCHIVO"] = {
            "carpeta_origen": self.test_dir,
            "tipo_cliente": "juridico,fisico"
        }
        config["SEGURIDAD"] = {"validar_hash": "True"}
        config["EMAIL"] = {
            "activar_alertas": "False",
            "destinatario": "test@correo.com"
        }
        with open(self.config_path, "w", encoding="utf-8") as f:
            config.write(f)

        estructura = {
            "juridica": ["contratos", "estatutos"],
            "tecnica": ["planos", "manuales"]
        }
        with open(self.estructura_path, "w", encoding="utf-8") as f:
            json.dump(estructura, f)

        self.plantilla_path = os.path.join(self.test_dir, "juridica", "contratos", "plantilla.txt")
        os.makedirs(os.path.dirname(self.plantilla_path), exist_ok=True)
        with open(self.plantilla_path, "w", encoding="utf-8") as f:
            f.write("Contenido fijo para validación de hash.")
        with open(self.plantilla_path, "rb") as f:
            self.hash_esperado = hashlib.sha256(f.read()).hexdigest()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_configuracion_valida(self):
        config = cargar_configuracion(self.config_path)
        self.assertIn("RUTAS", config)

    def test_carpeta_origen_valida(self):
        config = cargar_configuracion(self.config_path)
        carpeta_origen = config.get("ARCHIVO", "carpeta_origen", fallback="")
        self.assertTrue(carpeta_origen)
        self.assertTrue(os.path.exists(carpeta_origen))

    def test_configuracion_incompleta(self):
        ruta_invalida = os.path.join(self.test_dir, "config_invalido.ini")
        with open(ruta_invalida, "w", encoding="utf-8") as f:
            f.write("[OTRA_SECCION]\nclave=valor")
        with self.assertRaises(ValueError):
            cargar_configuracion(ruta_invalida)

    def test_configuracion_inexistente(self):
        ruta_falsa = os.path.join(self.test_dir, "no_existe.ini")
        with self.assertRaises(FileNotFoundError):
            cargar_configuracion(ruta_falsa)

    def test_estructura_valida(self):
        estructura = cargar_estructura(self.estructura_path)
        self.assertIn("juridica", estructura)

    def test_ejecucion_general(self):
        try:
            ejecutar_flujo_principal(self.config_path)
        except Exception as e:
            self.fail(f"ejecutar_flujo_principal lanzó excepción: {e}")
        ruta = os.path.join(self.test_dir, "tecnica", "manuales")
        self.assertTrue(os.path.exists(ruta))

    def test_logging_generado(self):
        ejecutar_flujo_principal(self.config_path)
        with open(self.log_path, "r", encoding="utf-8") as f:
            contenido = f.read()
        self.assertIn("Inicio del flujo principal", contenido)

    def test_hash_integridad(self):
        hash_real = calcular_hash_sha256(self.plantilla_path)
        self.assertEqual(hash_real, self.hash_esperado)
        self.assertTrue(validar_hash(self.plantilla_path, self.hash_esperado))

    def test_permisos_de_carpeta(self):
        carpeta_path = os.path.join(self.test_dir, "juridica", "estatutos")
        ejecutar_flujo_principal(self.config_path)
        self.assertTrue(os.access(carpeta_path, os.R_OK))
        self.assertTrue(os.access(carpeta_path, os.W_OK))

    def test_historial_evento(self):
        actualizar_historial(self.historial_path, "Creación", "juridica/contratos/plantilla.txt")
        with open(self.historial_path, "r", encoding="utf-8") as f:
            historial = json.load(f)
        self.assertEqual(len(historial), 1)
        self.assertEqual(historial[0]["evento"], "Creación")

    def test_historial_corrupto(self):
        with open(self.historial_path, "w", encoding="utf-8") as f:
            f.write("contenido inválido")
        actualizar_historial(self.historial_path, "Evento nuevo")
        with open(self.historial_path, "r", encoding="utf-8") as f:
            historial = json.load(f)
        self.assertEqual(len(historial), 1)
        self.assertEqual(historial[0]["evento"], "Evento nuevo")

# Tests independientes para verificar_permisos
def test_verificar_permisos_ruta_valida(tmp_path):
    carpeta = tmp_path / "entrada"
    carpeta.mkdir()
    verificar_permisos(str(carpeta))  # No debería lanzar excepción

def test_verificar_permisos_ruta_inexistente():
    with pytest.raises(FileNotFoundError):
        verificar_permisos("tests/data/no_existe")

def test_verificar_permisos_sin_escritura(tmp_path, monkeypatch):
    carpeta = tmp_path / "entrada"
    carpeta.mkdir()
    monkeypatch.setattr(os, "access", lambda p, m: False if m == os.W_OK else True)
    with pytest.raises(PermissionError):
        verificar_permisos(str(carpeta))

if __name__ == "__main__":
    unittest.main()