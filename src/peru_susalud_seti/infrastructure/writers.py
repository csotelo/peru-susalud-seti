import os
from pathlib import Path
from typing import List, Union
from ..domain.models import (
    HealthResourceTableA, 
    OutpatientTableB1, 
    EmergencyTableB2,
    InpatientTableC1,
    StayTableC2,
    EmergencyProductionD1,
    EmergencyMorbidityD2
)

class SetiFileWriter:
    """
    Infrastructure service to write validated domain entities into 
    ANSI-encoded, pipe-delimited text files.
    """

    def _get_file_metadata(self, record: Union[HealthResourceTableA, OutpatientTableB1, EmergencyTableB2]) -> tuple:
        """
        Determines the filename suffix and formatting logic based on the entity type.
        """
        # Cambiamos el orden: Primero validamos el tipo, luego extraemos datos
        if isinstance(record, HealthResourceTableA):
            suffix = "TAA0"
        elif isinstance(record, OutpatientTableB1):
            suffix = "TBB1"
        elif isinstance(record, EmergencyTableB2):
            suffix = "TBB2"
        elif isinstance(record, InpatientTableC1):
            suffix = "TCC1"
        elif isinstance(record, StayTableC2):
            suffix = "TCC2"
        elif isinstance(record, EmergencyProductionD1):
            suffix = "TDD1"
        elif isinstance(record, EmergencyMorbidityD2):
            suffix = "TDD2"
        else:
            raise ValueError(f"Tipo de entidad no soportado para escritura: {type(record)}")

        year = record.period[:4]
        month = record.period[4:]
        return f"{record.ipress_code}_{year}_{month}_{suffix}.TXT", suffix

    def write_records(self, data: List[Union[HealthResourceTableA, OutpatientTableB1, EmergencyTableB2]], output_dir: str) -> str:
        """
        Writes a list of records to the appropriate SETI-IPRESS text file.
        """
        if not data:
            raise ValueError("No hay datos para generar el archivo.")

        filename, table_type = self._get_file_metadata(data[0])
        file_path = Path(output_dir) / filename

        with open(file_path, mode='w', encoding='cp1252', newline='') as f:
            for record in data:
                line = self._format_line(record)
                f.write(line + "\n")

        return str(file_path)

    def _format_line(self, record: Union[HealthResourceTableA, OutpatientTableB1, EmergencyTableB2]) -> str:
        """
        Converts an entity into a pipe-delimited string according to its specific structure.
        """
        if isinstance(record, HealthResourceTableA):
            fields = [
                record.period, record.ipress_code, record.ugipress_code,
                str(record.physical_consulting_rooms), str(record.functional_consulting_rooms),
                str(record.hospital_beds), str(record.total_physicians), str(record.serums_physicians),
                str(record.resident_physicians), str(record.nurses), str(record.dentists),
                str(record.psychologists), str(record.nutritionists), str(record.medical_technologists),
                str(record.midwives), str(record.pharmacists), str(record.support_staff),
                str(record.other_professionals), str(record.operative_ambulances)
            ]
        elif isinstance(record, OutpatientTableB1):
            fields = [
                record.period, record.ipress_code, record.ugipress_code, record.ups_code,
                record.age_group, record.gender, str(record.total_patients),
                str(record.total_appointments), record.poverty_level, record.funding_source
            ]
        elif isinstance(record, EmergencyTableB2):
            fields = [
                record.period, record.ipress_code, record.ugipress_code, record.ups_code,
                record.age_group, record.gender, str(record.total_patients),
                str(record.total_appointments), record.priority, record.destination,
                record.poverty_level, record.funding_source
            ]
        elif isinstance(record, InpatientTableC1):
            fields = [
                record.period, record.ipress_code, record.ugipress_code, record.ups_code,
                record.age_group, record.gender, str(record.total_patients),
                str(record.total_appointments), record.exit_type,
                record.poverty_level, record.funding_source
            ]
        elif isinstance(record, StayTableC2):
            fields = [
                record.period, record.ipress_code, record.ugipress_code, record.ups_code,
                record.age_group, record.gender, str(record.total_patients),
                str(record.total_appointments), str(record.stay_days),
                record.poverty_level, record.funding_source
            ]
        elif isinstance(record, EmergencyProductionD1):
            fields = [
                record.period, record.ipress_code, record.ugipress_code, record.ups_code,
                record.age_group, record.gender, str(record.total_patients),
                str(record.total_appointments), record.poverty_level, record.funding_source
            ]
        elif isinstance(record, EmergencyMorbidityD2):
            fields = [
                record.period, record.ipress_code, record.ugipress_code, record.ups_code,
                record.age_group, record.gender, record.icd10_code,
                record.diagnosis_type, str(record.total_cases),
                record.poverty_level, record.funding_source
            ]
        return "|".join(fields)