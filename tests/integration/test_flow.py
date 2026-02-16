import os
import pytest
from peru_susalud_seti import TableAGenerationService, Observer

# Un Observador simple para acumular logs reales
class IntegrationLogger(Observer):
    def __init__(self):
        self.logs = []
    
    def update(self, event_type, message, data=None):
        self.logs.append((event_type, message))

@pytest.fixture
def sample_data():
    """Retorna una lista de diccionarios válida para la Tabla A."""
    return [
        {
            "periodo": "202310",
            "codigo_ipress": "00004567",
            "codigo_ugipress": "10004567",
            "consultorios_fisicos": 10,
            "consultorios_funcionales": 5,
            "camas_hospitalarias": 50,
            "medicos_total": 20,
            "ambulancias_operativas": 2
            # El resto de campos faltantes serán 0 gracias al Mapper
        },
        {
            "periodo": "202310",
            "codigo_ipress": "00004567",
            "codigo_ugipress": "10004567",
            "consultorios_fisicos": 12,
            "ambulancias_operativas": 1
        }
    ]

def test_full_generation_cycle(tmp_path, sample_data):
    """
    Prueba de Integración:
    Input (Dicts) -> Service -> Mapper -> Domain -> Writer -> Output (File System)
    """
    # 1. Setup
    output_dir = str(tmp_path) # Usamos carpeta temporal real del OS
    service = TableAGenerationService()
    logger = IntegrationLogger()
    service.attach(logger)

    # 2. Execution
    file_path = service.process_data(sample_data, output_dir)

    # 3. Verifications
    
    # A. Existencia del archivo
    assert os.path.exists(file_path)
    assert "00004567_2023_10_TAA0.TXT" in file_path

    # B. Verificación de Contenido y Codificación (ANSI/CP1252)
    # Es crucial leerlo como cp1252 para asegurar que el Writer hizo su trabajo
    with open(file_path, 'r', encoding='cp1252') as f:
        lines = f.readlines()
    
    assert len(lines) == 2, "Deben haber 2 líneas de datos"
    
    # Validar estructura de la primera línea (Pipe delimited)
    first_row = lines[0].strip().split('|')
    assert len(first_row) == 19, "La trama debe tener exactamente 19 campos"
    assert first_row[0] == "202310"
    assert first_row[3] == "10" # consultorios_fisicos
    assert first_row[18] == "2" # ambulancias

    # C. Verificación de Flujo de Eventos (Observer)
    event_types = [log[0] for log in logger.logs]
    assert "START" in event_types
    assert "SUCCESS" in event_types