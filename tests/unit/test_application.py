import pytest
from peru_susalud_seti.application.mappers import TableAMapper
from peru_susalud_seti.application.services import TableAGenerationService
from peru_susalud_seti.domain.types import Observer

def test_mapper_conversion():
    """El mapper debe convertir strings numéricos a int y manejar nulos."""
    raw_data = {
        "periodo": "202310",
        "codigo_ipress": "12345678",
        "codigo_ugipress": "87654321",
        "consultorios_fisicos": "15", # String
        "consultorios_funcionales": None # None debe ser 0
        # Faltan campos, deben ser 0
    }
    entity = TableAMapper.map_from_dict(raw_data)
    assert entity.physical_consulting_rooms == 15
    assert entity.functional_consulting_rooms == 0
    assert entity.operative_ambulances == 0

def test_mapper_error_propagation():
    """El mapper debe lanzar ValueError con contexto si los datos están mal."""
    raw_data = {
        "periodo": "202310",
        "codigo_ipress": "12345678",
        "consultorios_fisicos": "NO_ES_NUMERO" # Esto fallará la conversión int
    }
    with pytest.raises(ValueError, match="Error al procesar datos para IPRESS"):
        TableAMapper.map_from_dict(raw_data)

class MockObserver(Observer):
    def __init__(self):
        self.events = []
    def update(self, event_type, message, data=None):
        self.events.append((event_type, message))

def test_service_flow_success(tmp_path):
    """Prueba el flujo completo del servicio con el patrón Observer."""
    service = TableAGenerationService()
    observer = MockObserver()
    service.attach(observer)
    
    raw_data = [{
        "periodo": "202310",
        "codigo_ipress": "00004567",
        "codigo_ugipress": "10004567",
        "consultorios_fisicos": 10
    }]
    
    output_file = service.process_data(raw_data, str(tmp_path))
    
    # Verificaciones
    assert "00004567_2023_10_TAA0.TXT" in output_file
    
    # Verificar que el Observer recibió eventos
    event_types = [e[0] for e in observer.events]
    assert "START" in event_types
    assert "SUCCESS" in event_types
    
    service.detach(observer) # Limpieza

def test_service_validation_error_notification(tmp_path):
    """
    Si una fila falla, el servicio debe notificar ERROR pero continuar 
    (o fallar al final si no quedan registros válidos).
    """
    service = TableAGenerationService()
    observer = MockObserver()
    service.attach(observer)
    
    raw_data = [
        {"periodo": "BAD", "codigo_ipress": "123"}, # Fila mala
    ]
    
    # Como no hay ninguna fila válida, al final debe lanzar excepción
    with pytest.raises(ValueError, match="No se encontraron registros válidos"):
        service.process_data(raw_data, str(tmp_path))
        
    # Verificamos que se notificó el error de la fila
    event_types = [e[0] for e in observer.events]
    assert "ERROR" in event_types
    assert "CRITICAL" in event_types