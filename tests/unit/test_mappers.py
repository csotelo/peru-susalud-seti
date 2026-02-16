"""
Unit tests for Table Mappers.
Focusing on fixing regex mismatches and error handling.
"""
import pytest
from peru_susalud_seti.application.mappers import(
    TableAMapper,
    TableB1Mapper,
    TableB2Mapper,
    TableC1Mapper,
    TableC2Mapper,
    TableD1Mapper,
    TableD2Mapper
)

def test_table_a_mapper_success():
    """Tests successful mapping for Table A."""
    raw_data = {
        "period": "202602",
        "ipress_code": "00001234",
        "hospital_beds": "15"
    }
    entity = TableAMapper.map_from_dict(raw_data)
    assert entity.ipress_code == "00001234"
    assert entity.hospital_beds == 15

def test_table_a_mapper_invalid_data():
    """Tests that domain validation errors are wrapped correctly."""
    raw_data = {
        "period": "BAD", 
        "ipress_code": "00001234"
    }
    # Sincronizado con el mensaje del código
    with pytest.raises(ValueError, match="Error en mapeo TablaA"):
        TableAMapper.map_from_dict(raw_data)

def test_table_a_mapper_exception():
    """Tests unexpected exceptions like None input."""
    with pytest.raises(ValueError, match="Error en mapeo TablaA"):
        TableAMapper.map_from_dict(None)

def test_table_b1_mapper_exception():
    """Tests exceptions in B1 mapper with list input."""
    raw_data = {"total_patients": []}
    with pytest.raises(ValueError, match="Error en mapeo TablaB1"):
        TableB1Mapper.map_from_dict(raw_data)

def test_table_b2_mapper_exception():
    """Tests exceptions in B2 mapper with None input."""
    with pytest.raises(ValueError, match="Error en mapeo TablaB2"):
        TableB2Mapper.map_from_dict(None)

def test_table_c1_mapper_success():
    """Tests successful mapping for Table C1 (Discharges)."""
    raw_data = {
        "period": "202602",
        "ipress_code": "00001234",
        "exit_type": "2" # Fallecido por ejemplo
    }
    entity = TableC1Mapper.map_from_dict(raw_data)
    assert entity.exit_type == "2"
    assert entity.total_patients == 0

def test_table_c2_mapper_success():
    """Tests successful mapping for Table C2 (Stay)."""
    raw_data = {
        "period": "202602",
        "ipress_code": "00001234",
        "stay_days": "45"
    }
    entity = TableC2Mapper.map_from_dict(raw_data)
    assert entity.stay_days == 45

def test_table_c1_mapper_exception():
    """Forces an exception in TableC1Mapper sending None."""
    with pytest.raises(ValueError, match="Error en mapeo TablaC1"):
        TableC1Mapper.map_from_dict(None)

def test_table_c2_mapper_exception():
    """Forces an exception in TableC2Mapper sending None."""
    with pytest.raises(ValueError, match="Error en mapeo TablaC2"):
        TableC2Mapper.map_from_dict(None)

def test_table_d1_mapper_success():
    """Valida el mapeo exitoso de disponibilidad de horas (D1)."""
    raw_data = {
        "period": "202602",
        "ipress_code": "00001234",
        "document_number": "44556677",
        "asistencial_hours": "150"
    }
    entity = TableD1Mapper.map_from_dict(raw_data)
    assert entity.document_number == "44556677"
    assert entity.asistencial_hours == 150

def test_table_d2_mapper_success():
    """Valida el mapeo exitoso de programación de turnos (D2)."""
    raw_data = {
        "period": "202602",
        "ipress_code": "00001234",
        "shift_date": "20260215",
        "hours_count": 6
    }
    entity = TableD2Mapper.map_from_dict(raw_data)
    assert entity.shift_date == "20260215"
    assert entity.hours_count == 6

def test_table_d1_mapper_exception():
    """Verifica captura de errores en D1."""
    with pytest.raises(ValueError, match="Error en mapeo TablaD1"):
        TableD1Mapper.map_from_dict(None)

def test_table_d2_mapper_exception():
    """Verifica captura de errores en D2."""
    with pytest.raises(ValueError, match="Error en mapeo TablaD2"):
        TableD2Mapper.map_from_dict(None)