import pytest
from peru_susalud_seti.domain.types import Subject, Observer
from peru_susalud_seti.application.mappers import TableAMapper
from peru_susalud_seti.application.services import TableAGenerationService

# --- 1. Cubriendo 'detach' en Domain (types.py) ---
class MockObserver(Observer):
    def update(self, event_type, message, data=None):
        pass

def test_subject_detach_logic():
    """
    Verifica que un observador pueda ser removido y deje de recibir notificaciones.
    Cubre: Subject.detach()
    """
    subject = Subject()
    observer = MockObserver()
    
    # Attach and verify
    subject.attach(observer)
    assert observer in subject._observers
    
    # Detach and verify
    subject.detach(observer)
    assert observer not in subject._observers
    
    # Ensure no error if notifying without observers
    subject.notify("TEST", "Message")

# --- 2. Cubriendo 'except Exception' en Mapper (mappers.py) ---
def test_mapper_unexpected_exception():
    """
    Fuerza un error que NO sea ValueError para activar el bloque genérico 'except Exception'.
    Usamos una lista [] donde se espera un int, lo cual lanza TypeError en int().
    Cubre: application/mappers.py -> except Exception
    """
    raw_data = {
        "codigo_ipress": "00001234",
        # int([]) lanza TypeError, no ValueError. 
        # Esto caerá en el segundo bloque except del mapper.
        "consultorios_fisicos": [] 
    }
    
    with pytest.raises(ValueError, match="Error inesperado mapeando datos"):
        TableAMapper.map_from_dict(raw_data)

# --- 3. Cubriendo Error Crítico de Escritura en Service (services.py) ---
def test_service_critical_write_error(tmp_path, monkeypatch):
    """
    Simula una falla catastrófica en el sistema de archivos (ej. disco lleno o permisos)
    para activar el último bloque try/except del servicio.
    Cubre: application/services.py -> except Exception (CRITICAL)
    """
    service = TableAGenerationService()
    
    # Datos válidos
    raw_data = [{
        "periodo": "202310", 
        "codigo_ipress": "00004567", 
        "codigo_ugipress": "10004567",
        "consultorios_fisicos": 10
    }]

    # Usamos monkeypatch para sabotear el método write_table_a
    def mock_write_fail(*args, **kwargs):
        raise Exception("Disco Lleno / Error de Permisos")

    # Reemplazamos el método real del writer interno por nuestro mock fallido
    monkeypatch.setattr(service._writer, "write_table_a", mock_write_fail)
    
    # Esperamos que el servicio propague la excepción
    with pytest.raises(Exception, match="Disco Lleno"):
        service.process_data(raw_data, str(tmp_path))