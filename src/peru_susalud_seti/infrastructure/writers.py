import os
from typing import List
from pathlib import Path
from ..domain.models import HealthResourceTableA

class SetiFileWriter:
    """
    Responsible for writing domain objects into flat text files 
    compliant with SUSALUD technical specifications (ANSI, Pipe delimited).
    """

    def _generate_filename(self, record: HealthResourceTableA) -> str:
        """
        Generates the filename based on the pattern: CodigoIPRESS_YYYY_MM_TAA0.TXT
        Example: 00000456_2018_05_TAA0.TXT
        """
        year = record.period[:4]
        month = record.period[4:]
        # According to manual: IPRESS_Year_Month_TableCode.TXT
        return f"{record.ipress_code}_{year}_{month}_TAA0.TXT"

    def write_table_a(self, data: List[HealthResourceTableA], output_dir: str) -> str:
        """
        Writes a list of HealthResourceTableA objects to a .txt file.
        
        Args:
            data: List of validated records.
            output_dir: Directory where the file will be saved.
            
        Returns:
            The full path of the generated file.
        """
        if not data:
            raise ValueError("No hay datos para generar el archivo de la Tabla A.")

        # We assume all records belong to the same period/ipress for the file grouping.
        # Taking the first record to determine the filename.
        first_record = data[0]
        filename = self._generate_filename(first_record)
        file_path = Path(output_dir) / filename

        # SUSALUD requires ANSI encoding (often cp1252 in Windows environments)
        # Using 'newline=""' to handle line endings correctly across OS
        try:
            with open(file_path, mode='w', encoding='cp1252', newline='') as f:
                for record in data:
                    line = self._format_record(record)
                    f.write(line + "\n")
        except UnicodeEncodeError:
            # Fallback or error if characters usually supported by ANSI fail
            raise ValueError("Error de codificación: Se detectaron caracteres no compatibles con ANSI.")

        return str(file_path)

    def _format_record(self, record: HealthResourceTableA) -> str:
        """
        Converts a record object into a pipe-delimited string.
        Order must match the official structure strictly.
        """
        fields = [
            record.period,
            record.ipress_code,
            record.ugipress_code,
            str(record.physical_consulting_rooms),
            str(record.functional_consulting_rooms),
            str(record.hospital_beds),
            str(record.total_physicians),
            str(record.serums_physicians),
            str(record.resident_physicians),
            str(record.nurses),
            str(record.dentists),
            str(record.psychologists),
            str(record.nutritionists),
            str(record.medical_technologists),
            str(record.midwives),
            str(record.pharmacists),
            str(record.support_staff),
            str(record.other_professionals),
            str(record.operative_ambulances)
        ]
        
        # Join with pipe ('|')
        return "|".join(fields)