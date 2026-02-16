import pytest
from peru_susalud_seti.domain.models import HealthResourceTableA

def test_create_valid_table_a_entity():
    """Debe crear la entidad correctamente si los datos son válidos."""
    entity = HealthResourceTableA(
        period="202310",
        ipress_code="12345678",
        ugipress_code="87654321",
        physical_consulting_rooms=10,
        functional_consulting_rooms=0,
        hospital_beds=5,
        total_physicians=2,
        serums_physicians=1,
        resident_physicians=0,
        nurses=5,
        dentists=1,
        psychologists=0,
        nutritionists=0,
        medical_technologists=0,
        midwives=0,
        pharmacists=1,
        support_staff=0,
        other_professionals=0,
        operative_ambulances=1
    )
    assert entity.period == "202310"
    assert entity.hospital_beds == 5

def test_invalid_period_format():
    """Debe fallar si el periodo no es AAAAMM o no es numérico."""
    with pytest.raises(ValueError, match="El periodo 'ABC' es inválido"):
        HealthResourceTableA(
            period="ABC", # Inválido
            ipress_code="12345678",
            ugipress_code="12345678",
            physical_consulting_rooms=0, functional_consulting_rooms=0, hospital_beds=0,
            total_physicians=0, serums_physicians=0, resident_physicians=0, nurses=0,
            dentists=0, psychologists=0, nutritionists=0, medical_technologists=0,
            midwives=0, pharmacists=0, support_staff=0, other_professionals=0,
            operative_ambulances=0
        )

def test_invalid_ipress_length():
    """Debe fallar si el código IPRESS no tiene 8 caracteres."""
    with pytest.raises(ValueError, match="debe tener 8 caracteres"):
        HealthResourceTableA(
            period="202310",
            ipress_code="123", # Inválido
            ugipress_code="12345678",
            physical_consulting_rooms=0, functional_consulting_rooms=0, hospital_beds=0,
            total_physicians=0, serums_physicians=0, resident_physicians=0, nurses=0,
            dentists=0, psychologists=0, nutritionists=0, medical_technologists=0,
            midwives=0, pharmacists=0, support_staff=0, other_professionals=0,
            operative_ambulances=0
        )

def test_negative_values():
    """Debe fallar si hay valores numéricos negativos."""
    with pytest.raises(ValueError, match="no puede ser negativo"):
        HealthResourceTableA(
            period="202310",
            ipress_code="12345678",
            ugipress_code="12345678",
            physical_consulting_rooms=-5, # Inválido
            functional_consulting_rooms=0, hospital_beds=0,
            total_physicians=0, serums_physicians=0, resident_physicians=0, nurses=0,
            dentists=0, psychologists=0, nutritionists=0, medical_technologists=0,
            midwives=0, pharmacists=0, support_staff=0, other_professionals=0,
            operative_ambulances=0
        )