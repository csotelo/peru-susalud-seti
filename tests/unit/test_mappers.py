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
    TableD2Mapper,
    TableEMapper,
    TableFMapper,
    TableHMapper
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
    """Valida mapeo de Producción de Emergencia (D1)."""
    raw_data = {
        "period": "202602",
        "ipress_code": "00001234",
        "ups_code": "301602",
        "total_appointments": 20
    }
    entity = TableD1Mapper.map_from_dict(raw_data)
    assert entity.ups_code == "301602"
    assert entity.total_appointments == 20

def test_table_d2_mapper_success():
    """Valida mapeo de Morbilidad de Emergencia (D2)."""
    raw_data = {
        "period": "202602",
        "ipress_code": "00001234",
        "icd10_code": "R10", # Dolor abdominal
        "diagnosis_type": "P",
        "total_cases": 5
    }
    entity = TableD2Mapper.map_from_dict(raw_data)
    assert entity.icd10_code == "R10"
    assert entity.diagnosis_type == "P"
    assert entity.total_cases == 5

def test_table_e_mapper_success():
    """Valida mapeo de Tabla E (Partos Consolidado)."""
    raw_data = {
        "period": "202602",
        "ipress_code": "00001234",
        "total_deliveries": 100,
        "complicated_deliveries": 20,
        "live_births": 98,
        "still_births": 2
    }
    entity = TableEMapper.map_from_dict(raw_data)
    assert entity.total_deliveries == 100
    assert entity.still_births == 2

def test_table_h_mapper_success():
    """Valida mapeo de Tabla H (Quirúrgica)."""
    raw_data = {
        "period": "202602",
        "ipress_code": "00001234",
        "total_interventions": 5
    }
    entity = TableHMapper.map_from_dict(raw_data)
    assert entity.total_interventions == 5

def test_table_f_mapper_success():
    """Valida mapeo de Tabla F (Vigilancia)."""
    raw_data = {
        "period": "202602",
        "ipress_code": "00001234",
        "surveillance_code": "I01", # Infección Herida Operatoria
        "event_count": 3
    }
    entity = TableFMapper.map_from_dict(raw_data)
    assert entity.surveillance_code == "I01"
    assert entity.event_count == 3