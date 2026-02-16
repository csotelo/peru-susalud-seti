"""
Unit tests for Table Mappers.
Focusing on fixing regex mismatches and error handling.
"""
import pytest
from peru_susalud_seti.application.mappers import TableAMapper, TableB1Mapper, TableB2Mapper

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