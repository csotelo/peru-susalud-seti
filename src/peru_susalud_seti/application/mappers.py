from typing import Dict, Any
from ..domain.models import HealthResourceTableA

class TableAMapper:
    """
    Translates raw dictionary data (from JSON input) into valid Domain Entities.
    """

    @staticmethod
    def map_from_dict(data: Dict[str, Any]) -> HealthResourceTableA:
        """
        Maps a single dictionary row to a HealthResourceTableA entity.
        
        Args:
            data: A dictionary containing raw input data.
            
        Raises:
            ValueError: If required fields are missing or formats are invalid.
        """
        try:
            # Helper to safely convert to int, default to 0 if None
            def to_int(val: Any) -> int:
                if val is None:
                    return 0
                return int(val)

            return HealthResourceTableA(
                period=str(data.get("periodo", "")).strip(),
                ipress_code=str(data.get("codigo_ipress", "")).strip(),
                ugipress_code=str(data.get("codigo_ugipress", "")).strip(),
                
                # Numeric fields conversion
                physical_consulting_rooms=to_int(data.get("consultorios_fisicos")),
                functional_consulting_rooms=to_int(data.get("consultorios_funcionales")),
                hospital_beds=to_int(data.get("camas_hospitalarias")),
                total_physicians=to_int(data.get("medicos_total")),
                serums_physicians=to_int(data.get("medicos_serums")),
                resident_physicians=to_int(data.get("medicos_residentes")),
                nurses=to_int(data.get("enfermeras")),
                dentists=to_int(data.get("odontologos")),
                psychologists=to_int(data.get("psicologos")),
                nutritionists=to_int(data.get("nutricionistas")),
                medical_technologists=to_int(data.get("tecnologos_medicos")),
                midwives=to_int(data.get("obstetrices")),
                pharmacists=to_int(data.get("quimicos_farmaceuticos")),
                support_staff=to_int(data.get("auxiliares_asistenciales")),
                other_professionals=to_int(data.get("otros_profesionales")),
                operative_ambulances=to_int(data.get("ambulancias_operativas"))
            )
        except ValueError as e:
            # Re-raise with context in Spanish
            raise ValueError(f"Error al procesar datos para IPRESS {data.get('codigo_ipress')}: Valor numérico inválido.") from e
        except Exception as e:
            raise ValueError(f"Error inesperado mapeando datos: {str(e)}")