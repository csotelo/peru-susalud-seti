"""
Unit tests for Infrastructure Writers.
Targeting 100% coverage for infrastructure/writers.py
"""
import pytest
from peru_susalud_seti.infrastructure.writers import SetiFileWriter
from peru_susalud_seti.domain.models import (
    HealthResourceTableA, 
    OutpatientTableB1, 
    EmergencyTableB2, 
    InpatientTableC1,
    StayTableC2,
    EmergencyProductionD1,
    EmergencyMorbidityD2,
    ChildbirthTableE,
    SurveillanceTableF,
    ProceduresTableG,
    SurgeryTableH,
    ReferralTableI,
    ExpenditureTableJ
)

def test_writer_unsupported_entity():
    """Verifies error when an unknown entity type is passed."""
    writer = SetiFileWriter()
    with pytest.raises(ValueError, match="Tipo de entidad no soportado"):
        writer._get_file_metadata("not_an_entity")

def test_writer_empty_data(tmp_path):
    """Verifies error when data list is empty."""
    writer = SetiFileWriter()
    with pytest.raises(ValueError, match="No hay datos para generar"):
        writer.write_records([], str(tmp_path))

def test_writer_format_all_types():
    """
    Executes formatting for all supported entities to ensure 100% branch coverage.
    """
    writer = SetiFileWriter()
    
    # 1. Setup entities
    records = [
        HealthResourceTableA(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            physical_consulting_rooms=1, functional_consulting_rooms=1, hospital_beds=1,
            total_physicians=1, serums_physicians=0, resident_physicians=0, nurses=1,
            dentists=0, psychologists=0, nutritionists=0, medical_technologists=0,
            midwives=0, pharmacists=1, support_staff=1, other_professionals=0,
            operative_ambulances=0
        ),
        OutpatientTableB1(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            ups_code="301601", age_group="05", gender="1",
            total_patients=10, total_appointments=10,
            poverty_level="3", funding_source="4"
        ),
        EmergencyTableB2(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            ups_code="301602", age_group="05", gender="1",
            total_patients=5, total_appointments=5,
            priority="1", destination="1",
            poverty_level="3", funding_source="4"
        ),
        InpatientTableC1(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            ups_code="301101", age_group="05", gender="1",
            total_patients=5, total_appointments=5,
            poverty_level="3", funding_source="4", exit_type="1"
        ),
        StayTableC2(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            ups_code="301101", age_group="05", gender="1",
            total_patients=5, total_appointments=5,
            poverty_level="3", funding_source="4", stay_days=15
        ),
        EmergencyProductionD1(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            ups_code="301602", age_group="05", gender="1",
            total_patients=10, total_appointments=10,
            poverty_level="3", funding_source="4"
        ),
        EmergencyMorbidityD2(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            ups_code="301602", age_group="05", gender="1",
            icd10_code="A09", diagnosis_type="D", total_cases=5,
            poverty_level="3", funding_source="4"
        ),
        ChildbirthTableE(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            total_deliveries=50, complicated_deliveries=10,
            live_births=49, still_births=1
        ),
        SurveillanceTableF(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            ups_code="202201", surveillance_code="I02", event_count=2
        ),
        ProceduresTableG(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            ups_code="302301", age_group="05", gender="2",
            total_patients=10, total_procedures=50,
            poverty_level="3", funding_source="4"
        ),
        SurgeryTableH(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            ups_code="301602", age_group="05", gender="1",
            total_patients=3, total_interventions=3,
            poverty_level="3", funding_source="4"
        ),
        ReferralTableI(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            ups_code="301602", age_group="05", gender="2",
            total_patients=5, total_referrals=5,
            poverty_level="3", funding_source="4"
        ),
        ExpenditureTableJ(
            period="202602", ipress_code="12345678", ugipress_code="12345678",
            funding_source="1", budget_category="2.3.1", executed_amount=5000.00
        )
    ]
    
    # 2. Execute formatting for each (covering all if/elif branches)
    for record in records:
        line = writer._format_line(record)
        assert "|" in line
        assert "202602" in line


def test_writer_format_lines():
    """
    Validates formatting for all current entities to close all logical branches.
    """
    writer = SetiFileWriter()
    
    # Setup instances for all supported tables
    table_a = HealthResourceTableA(
        period="202602", ipress_code="12345678", ugipress_code="12345678",
        physical_consulting_rooms=1, functional_consulting_rooms=1, hospital_beds=1,
        total_physicians=1, serums_physicians=0, resident_physicians=0, nurses=1,
        dentists=0, psychologists=0, nutritionists=0, medical_technologists=0,
        midwives=0, pharmacists=1, support_staff=1, other_professionals=0,
        operative_ambulances=0
    )
    table_b1 = OutpatientTableB1(
        period="202602", ipress_code="12345678", ugipress_code="12345678",
        ups_code="301601", age_group="05", gender="1",
        total_patients=10, total_appointments=10,
        poverty_level="3", funding_source="4"
    )
    table_b2 = EmergencyTableB2(
        period="202602", ipress_code="12345678", ugipress_code="12345678",
        ups_code="301602", age_group="05", gender="1",
        total_patients=5, total_appointments=5,
        priority="1", destination="1",
        poverty_level="3", funding_source="4"
    )

    # Executing each formatting to cover all if/elif/exit branches
    assert "|" in writer._format_line(table_a)
    assert "|" in writer._format_line(table_b1)
    assert "|" in writer._format_line(table_b2)

