from typing import Dict, Any
from ..domain.models import HealthResourceTableA
from ..domain.models import OutpatientTableB1, EmergencyTableB2

class TableAMapper:
    """
    Translates raw dictionary data (from JSON input) into valid Domain Entities.
    """

    @staticmethod
    def map_from_dict(data: Dict[str, Any]) -> HealthResourceTableA:
        """
        Maps a single dictionary row to a HealthResourceTableA entity.
        """
        try:
            def to_int(val: Any) -> int:
                if val is None or val == "":
                    return 0
                return int(val)

            return HealthResourceTableA(
                # Usamos llaves en inglés para consistencia con el código
                period=str(data.get("period", "")).strip(),
                ipress_code=str(data.get("ipress_code", "")).strip(),
                ugipress_code=str(data.get("ugipress_code", "")).strip(),
                
                physical_consulting_rooms=to_int(data.get("physical_consulting_rooms")),
                functional_consulting_rooms=to_int(data.get("functional_consulting_rooms")),
                hospital_beds=to_int(data.get("hospital_beds")),
                total_physicians=to_int(data.get("total_physicians")),
                serums_physicians=to_int(data.get("serums_physicians")),
                resident_physicians=to_int(data.get("resident_physicians")),
                nurses=to_int(data.get("nurses")),
                dentists=to_int(data.get("dentists")),
                psychologists=to_int(data.get("psychologists")),
                nutritionists=to_int(data.get("nutritionists")),
                medical_technologists=to_int(data.get("medical_technologists")),
                midwives=to_int(data.get("midwives")),
                pharmacists=to_int(data.get("pharmacists")),
                support_staff=to_int(data.get("support_staff")),
                other_professionals=to_int(data.get("other_professionals")),
                operative_ambulances=to_int(data.get("operative_ambulances"))
            )
        except (ValueError, TypeError, AttributeError) as e:
            raise ValueError(f"Error en mapeo TablaA: {str(e)}")



class TableB1Mapper:
    """
    Translates raw dictionary data into OutpatientTableB1 entities.
    """

    @staticmethod
    def map_from_dict(data: Dict[str, Any]) -> OutpatientTableB1:
        """
        Maps dictionary to OutpatientTableB1 (TBB1).
        """
        try:
            return OutpatientTableB1(
                period=str(data.get("period", "")).strip(),
                ipress_code=str(data.get("ipress_code", "")).strip(),
                ugipress_code=str(data.get("ugipress_code", "")).strip(),
                ups_code=str(data.get("ups_code", "")).strip(),
                age_group=str(data.get("age_group", "01")).zfill(2),
                gender=str(data.get("gender", "1")),
                total_patients=int(data.get("total_patients", 0)),
                total_appointments=int(data.get("total_appointments", 0)),
                poverty_level=str(data.get("poverty_level", "3")),
                funding_source=str(data.get("funding_source", "4"))
            )
        except (ValueError, TypeError, AttributeError) as e:
            raise ValueError(f"Error en mapeo TablaB1: {str(e)}")

class TableB2Mapper:
    """
    Translates raw dictionary data into EmergencyTableB2 entities.
    """

    @staticmethod
    def map_from_dict(data: Dict[str, Any]) -> EmergencyTableB2:
        """
        Maps dictionary to EmergencyTableB2 (TBB2).
        """
        try:
            return EmergencyTableB2(
                period=str(data.get("period", "")).strip(),
                ipress_code=str(data.get("ipress_code", "")).strip(),
                ugipress_code=str(data.get("ugipress_code", "")).strip(),
                ups_code=str(data.get("ups_code", "")).strip(),
                age_group=str(data.get("age_group", "01")).zfill(2),
                gender=str(data.get("gender", "1")),
                total_patients=int(data.get("total_patients", 0)),
                total_appointments=int(data.get("total_appointments", 0)),
                poverty_level=str(data.get("poverty_level", "3")),
                funding_source=str(data.get("funding_source", "4")),
                priority=str(data.get("priority", "3")),
                destination=str(data.get("destination", "1"))
            )
        except (ValueError, TypeError, AttributeError) as e:
            raise ValueError(f"Error en mapeo TablaB2: {str(e)}")