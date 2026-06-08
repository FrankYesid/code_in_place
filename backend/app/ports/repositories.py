# =============================================================================
# Repositories Ports - Puertos de Salida
# =============================================================================
# En Arquitectura Hexagonal, un Puerto es una interfaz que define una 
# capacidad necesaria para el sistema, pero sin decir cómo se implementa.
# Aquí definimos cómo queremos obtener las palabras del juego.
# =============================================================================

from abc import ABC, abstractmethod
from typing import List

class WordRepository(ABC):
    """
    Puerto para el acceso a las palabras del juego.
    Soporta múltiples temáticas.
    """
    
    @abstractmethod
    def get_themes(self) -> List[str]:
        """Devuelve la lista de temáticas disponibles."""
        pass

    @abstractmethod
    def get_random_word(self, theme: str = None) -> str:
        """
        Elige una palabra al azar. Si se proporciona una temática,
        la palabra pertenecerá a esa temática.
        """
        pass
