# Ahora sí, Estando dentro de peru_susalud_seti/, Python entiende el punto:
from .application.services import TableAGenerationService
from .domain.types import Observer

__version__ = "0.1.0"
__all__ = ["TableAGenerationService", "Observer"]