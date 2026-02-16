from dataclasses import dataclass, fields

@dataclass(frozen=True)
class HealthResourceTableA:
    """
    Represents a row in Table A (Health Resources).
    Immutable Data Class to ensure data integrity during processing.
    """
    period: str                 # YYYYMM
    ipress_code: str            # 8 digits
    ugipress_code: str          # 8 digits
    physical_consulting_rooms: int
    functional_consulting_rooms: int
    hospital_beds: int
    total_physicians: int
    serums_physicians: int
    resident_physicians: int
    nurses: int
    dentists: int
    psychologists: int
    nutritionists: int
    medical_technologists: int
    midwives: int
    pharmacists: int
    support_staff: int          # Auxiliares asistenciales
    other_professionals: int
    operative_ambulances: int

    def __post_init__(self):
        """
        Validates domain invariants immediately upon creation.
        Raises ValueError with Spanish messages for end-user feedback.
        """
        # Validate Period Format
        if len(self.period) != 6 or not self.period.isdigit():
             raise ValueError(f"El periodo '{self.period}' es inválido. Formato requerido: AAAAMM")
        
        # Validate IPRESS Code Length
        if len(self.ipress_code) != 8:
            raise ValueError(f"El código IPRESS '{self.ipress_code}' debe tener 8 caracteres.")

        # Validate Non-Negative Integers for all numeric fields
        # specific logic to iterate over integer fields only
        for field in fields(self):
            if field.type is int:
                value = getattr(self, field.name)
                if value < 0:
                    raise ValueError(f"El campo '{field.name}' no puede ser negativo: {value}")


@dataclass(frozen=True)
class BaseProductionTable:
    """
    Base class for SETI-IPRESS production tables.
    Contains common fields for B1 and B2 tables.
    """
    period: str
    ipress_code: str
    ugipress_code: str
    ups_code: str
    age_group: str
    gender: str
    total_patients: int
    total_appointments: int
    poverty_level: str
    funding_source: str

@dataclass(frozen=True)
class OutpatientTableB1(BaseProductionTable):
    """
    Represents Table B1: Outpatient Consultation Production.
    Fields match the official SUSALUD structure for TBB1.
    """
    pass

@dataclass(frozen=True)
class EmergencyTableB2(BaseProductionTable):
    """
    Represents Table B2: Emergency Services Production.
    Adds priority and destination fields as per SUSALUD specs.
    """
    priority: str
    destination: str

@dataclass(frozen=True)
class InpatientTableC1(BaseProductionTable):
    """
    Represents Table C1: Hospital Discharges (Egresos).
    """
    exit_type: str # Alta, Fallecido, Referido, etc.

@dataclass(frozen=True)
class StayTableC2(BaseProductionTable):
    """
    Represents Table C2: Hospital Stay (Estancia).
    """
    stay_days: int # Total de días estancia en el periodo


@dataclass(frozen=True)
class EmergencyProductionD1:
    """
    Represents Table D1: Emergency Production.
    Focuses on the volume of care (patients and appointments) in Emergency UPS.
    """
    period: str
    ipress_code: str
    ugipress_code: str
    ups_code: str
    age_group: str
    gender: str
    total_patients: int
    total_appointments: int
    poverty_level: str
    funding_source: str

@dataclass(frozen=True)
class EmergencyMorbidityD2:
    """
    Represents Table D2: Emergency Morbidity.
    Focuses on the causes of care (ICD-10 diagnoses).
    """
    period: str
    ipress_code: str
    ugipress_code: str
    ups_code: str
    age_group: str
    gender: str
    icd10_code: str       # Código CIE-10 (3 o 4 caracteres)
    diagnosis_type: str   # P (Presuntivo), D (Definitivo), R (Repetido)
    total_cases: int      # Cantidad de casos reportados
    poverty_level: str
    funding_source: str


@dataclass(frozen=True)
class SurgeryTableH:
    """
    Represents Table H: Surgical Interventions (Intervenciones Quirúrgicas).
    """
    period: str
    ipress_code: str
    ugipress_code: str
    ups_code: str
    age_group: str
    gender: str
    total_patients: int
    total_interventions: int # Cantidad de intervenciones realizadas
    poverty_level: str
    funding_source: str