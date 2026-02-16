import pytest
from peru_susalud_seti import TableAGenerationService

def test_library_is_importable_and_runs(tmp_path):
    """
    SMOKE TEST: 
    Verifica simplemente que la clase principal se pueda instanciar
    y ejecutar con un dato mínimo sin lanzar excepciones fatales.
    """
    try:
        service = TableAGenerationService()
        
        minimal_data = [{
            "periodo": "202401",
            "codigo_ipress": "99999999",
            "codigo_ugipress": "99999999",
            "consultorios_fisicos": 1
        }]
        
        # Solo nos importa que esto NO lance excepción
        service.process_data(minimal_data, str(tmp_path))
        
    except ImportError:
        pytest.fail("SMOKE: No se pudo importar la librería. ¿Está instalada?")
    except Exception as e:
        pytest.fail(f"SMOKE: La ejecución básica falló: {e}")