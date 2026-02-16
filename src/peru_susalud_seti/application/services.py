from typing import List, Dict, Any
from ..domain.types import Subject
from ..infrastructure.writers import SetiFileWriter
from .mappers import TableAMapper, TableB1Mapper, TableB2Mapper

class SetiGenerationService(Subject):
    """
    Orchestrates the generation of multiple SUSALUD tables.
    Uses a mapping strategy to remain open for new table types.
    """

    def __init__(self):
        super().__init__()
        self._writer = SetiFileWriter()
        # Strategy pattern for mappers
        self._mappers = {
            "A": TableAMapper.map_from_dict,
            "B1": TableB1Mapper.map_from_dict,
            "B2": TableB2Mapper.map_from_dict
        }

    def generate_table(self, table_id: str, raw_data: List[Dict[str, Any]], output_dir: str) -> str:
        """
        Validates and generates a specific TXT table from JSON-like data.
        """
        if table_id not in self._mappers:
            raise ValueError(f"La tabla {table_id} no está soportada actualmente.")

        self.notify("START", f"Iniciando proceso para Tabla {table_id}")
        
        mapper_func = self._mappers[table_id]
        validated_records = []

        for index, item in enumerate(raw_data):
            try:
                entity = mapper_func(item)
                validated_records.append(entity)
            except Exception as e:
                self.notify("ERROR", f"Fila {index + 1}: {str(e)}")

        if not validated_records:
            raise ValueError(f"No hay registros válidos para la Tabla {table_id}")

        file_path = self._writer.write_records(validated_records, output_dir)
        self.notify("SUCCESS", f"Archivo {table_id} generado en {file_path}")
        
        return file_path