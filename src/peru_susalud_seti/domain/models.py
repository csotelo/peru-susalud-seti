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