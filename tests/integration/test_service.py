import os
import pytest
from peru_susalud_seti import SetiGenerationService

@pytest.mark.parametrize("table_id, raw_row, expected_suffix", [
    ("A", {"period": "202602", "ipress_code": "00001234", "hospital_beds": 5}, "TAA0"),
    ("B1", {"period": "202602", "ipress_code": "00001234", "total_patients": 10}, "TBB1"),
    ("B2", {"period": "202602", "ipress_code": "00001234", "priority": "1"}, "TBB2"),
    ("C1", {"period": "202602", "ipress_code": "00001234", "exit_type": "1"}, "TCC1"),
    ("C2", {"period": "202602", "ipress_code": "00001234", "stay_days": 10}, "TCC2"),
    ("D1", {"period": "202602", "ipress_code": "12345678", "document_number": "10203040"}, "TDD1"),
    ("D2", {"period": "202602", "ipress_code": "12345678", "shift_date": "20260210"}, "TDD2"),
    ("H", {"period": "202602", "ipress_code": "12345678", "total_interventions": 3}, "THH0"),
])
def test_table_generation_flow(tmp_path, table_id, raw_row, expected_suffix):
    """
    Tests the end-to-end generation flow for different table types.
    Verifies file creation, naming convention, and ANSI encoding.
    """
    service = SetiGenerationService()
    output_dir = str(tmp_path)
    
    file_path = service.generate_table(table_id, [raw_row], output_dir)
    
    assert os.path.exists(file_path)
    assert f"_{expected_suffix}.TXT" in file_path
    
    with open(file_path, "r", encoding="cp1252") as f:
        content = f.read()
        assert raw_row["period"] in content
        assert raw_row["ipress_code"] in content


def test_service_unsupported_table():
    """Covers the validation for unsupported table IDs."""
    service = SetiGenerationService()
    with pytest.raises(ValueError, match="no está soportada"):
        service.generate_table("Z9", [], "output")

def test_service_row_error_notification(tmp_path):
    """Covers the notification of errors during row mapping (application/services.py)."""
    service = SetiGenerationService()
    # One valid row, one invalid row (None triggers Exception in mapper)
    raw_data = [
        {"period": "202602", "ipress_code": "12345678", "total_patients": 10},
        None 
    ]
    # Should generate the file with the valid row but notify error for the second
    path = service.generate_table("B1", raw_data, str(tmp_path))
    assert path is not None

def test_service_all_rows_fail_mapping(tmp_path):
    """
    Covers services.py line 42.
    Ensures ValueError is raised when every row in the input fails validation.
    """
    service = SetiGenerationService()
    # Sending data that will definitely fail mapping (None)
    with pytest.raises(ValueError, match="No hay registros válidos"):
        service.generate_table("A", [None, None], str(tmp_path))