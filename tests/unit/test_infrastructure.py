import pytest
from pathlib import Path
from peru_susalud_seti.infrastructure.writers import SetiFileWriter
from peru_susalud_seti.domain.models import HealthResourceTableA

# Fixture para crear una entidad válida rápidamente
@pytest.fixture
def valid_entity():
    return HealthResourceTableA(
        period="202310", ipress_code="00004567", ugipress_code="10004567",
        physical_consulting_rooms=10, functional_consulting_rooms=0, hospital_beds=0,
        total_physicians=0, serums_physicians=0, resident_physicians=0, nurses=0,
        dentists=0, psychologists=0, nutritionists=0, medical_technologists=0,
        midwives=0, pharmacists=0, support_staff=0, other_professionals=0,
        operative_ambulances=0
    )

def test_writer_filename_generation(valid_entity, tmp_path):
    """Verifica que el nombre del archivo siga el patrón Codigo_Año_Mes_TAA0.TXT"""
    writer = SetiFileWriter()
    # tmp_path es un directorio temporal proveído por pytest
    file_path = writer.write_table_a([valid_entity], str(tmp_path))
    
    expected_name = "00004567_2023_10_TAA0.TXT"
    assert Path(file_path).name == expected_name
    assert Path(file_path).exists()

def test_writer_content_format(valid_entity, tmp_path):
    """Verifica que el contenido use pipes y no tenga espacios extra."""
    writer = SetiFileWriter()
    file_path = writer.write_table_a([valid_entity], str(tmp_path))
    
    with open(file_path, "r", encoding="cp1252") as f:
        content = f.read().strip()
    
    # Reconstruimos lo que esperamos
    parts = content.split("|")
    assert len(parts) == 19 # Debe haber 19 campos
    assert parts[0] == "202310"
    assert parts[3] == "10" # physical_consulting_rooms

def test_writer_empty_list_error(tmp_path):
    """Debe lanzar error si la lista de datos está vacía."""
    writer = SetiFileWriter()
    with pytest.raises(ValueError, match="No hay datos"):
        writer.write_table_a([], str(tmp_path))

def test_writer_encoding_error(valid_entity, tmp_path):
    """
    Intenta forzar un error de codificación ANSI (cp1252).
    Usamos un caracter que no existe en ANSI (ej. emoji o caracter raro unicode)
    para disparar la excepción UnicodeEncodeError controlada.
    """
    # Hack: inyectamos un valor inválido a la fuerza usando bypass de dataclass (solo para test)
    object.__setattr__(valid_entity, 'ugipress_code', "TEST😊") 
    
    writer = SetiFileWriter()
    with pytest.raises(ValueError, match="Error de codificación"):
        writer.write_table_a([valid_entity], str(tmp_path))