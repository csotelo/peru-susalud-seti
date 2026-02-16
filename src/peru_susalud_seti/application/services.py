from typing import List, Dict, Any
from ..domain.types import Subject
from ..domain.models import HealthResourceTableA
from ..infrastructure.writers import SetiFileWriter
from .mappers import TableAMapper

class TableAGenerationService(Subject):
    """
    Main Use Case: Orchestrates the conversion from Raw Data -> Domain -> TXT File.
    Implements the Observer pattern to notify subscribers about the process.
    """

    def __init__(self):
        super().__init__()
        self._writer = SetiFileWriter()

    def process_data(self, raw_data: List[Dict[str, Any]], output_folder: str) -> str:
        """
        Process a list of dictionaries and generates the SUSALUD Table A file.

        Args:
            raw_data: List of dictionaries (parsed JSON).
            output_folder: Path to save the generated file.

        Returns:
            The path of the generated file.
        """
        valid_records: List[HealthResourceTableA] = []
        
        self.notify("START", "Iniciando proceso de generación para Tabla A.")

        for index, row in enumerate(raw_data):
            try:
                # 1. Map and Validate (Domain constraints applied here)
                entity = TableAMapper.map_from_dict(row)
                valid_records.append(entity)
                
            except ValueError as e:
                # Notify error but don't stop strictly unless desired? 
                # For strict compliance, one error usually invalidates the file.
                # Here we allow skipping but notify.
                self.notify("ERROR", f"Fila {index + 1}: {str(e)}")
                # Depending on strictness, you might want to: raise e

        if not valid_records:
            error_msg = "No se encontraron registros válidos para generar la trama."
            self.notify("CRITICAL", error_msg)
            raise ValueError(error_msg)

        try:
            # 2. Write File
            file_path = self._writer.write_table_a(valid_records, output_folder)
            self.notify("SUCCESS", f"Archivo generado exitosamente en: {file_path}")
            return file_path
            
        except Exception as e:
            self.notify("CRITICAL", f"Error escribiendo archivo: {str(e)}")
            raise