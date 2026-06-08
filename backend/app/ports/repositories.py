# =============================================================================
# Repositories Ports - Output Ports
# =============================================================================
# In Hexagonal Architecture, a Port is an interface that defines a 
# capability needed by the system, without saying how it's implemented.
# Here we define how we want to get the game's words.
# =============================================================================

from abc import ABC, abstractmethod
from typing import List

class WordRepository(ABC):
    """
    Port for game word access.
    Supports multiple themes.
    """
    
    @abstractmethod
    def get_themes(self) -> List[str]:
        """Returns the list of available themes."""
        pass

    @abstractmethod
    def get_random_word(self, theme: str = None) -> str:
        """
        Chooses a random word. If a theme is provided,
        the word will belong to that theme.
        """
        pass
