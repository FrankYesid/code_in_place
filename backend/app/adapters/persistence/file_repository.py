# =============================================================================
# File Repository Adapter - Persistence Adapter
# =============================================================================
# This adapter implements the 'WordRepository' port.
# It handles communication with the file system (lexicons/ folder).
# If we want to use a Database in the future, we only create a new 
# adapter without changing the rest of the system.
# =============================================================================

import random
import os
from typing import List, Dict
from ...ports.repositories import WordRepository

class FileWordRepository(WordRepository):
    """
    Adapter that reads words from .txt files in a lexicons folder.
    Each file represents a theme.
    """
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.backup_words = ["PYTHON", "CODE", "INPLACE", "HEXAGONAL"]
        self._cache: Dict[str, List[str]] = {}
        self._load_all_lexicons()

    def _load_all_lexicons(self):
        """Loads all .txt files from the lexicons folder."""
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path, exist_ok=True)
            return

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".txt"):
                theme_name = filename[:-4]  # Remove .txt extension
                file_path = os.path.join(self.folder_path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        words = [line.strip().upper() for line in f if line.strip()]
                        if words:
                            self._cache[theme_name] = words
                except Exception as e:
                    print(f"Error loading lexicon {theme_name}: {e}")

    def get_themes(self) -> List[str]:
        """Returns the names of the loaded themes."""
        return list(self._cache.keys())

    def get_random_word(self, theme: str = None) -> str:
        """Gets a random word from a specific theme or at random."""
        if not self._cache:
            return random.choice(self.backup_words)

        selected_theme = theme if theme in self._cache else random.choice(list(self._cache.keys()))
        return random.choice(self._cache[selected_theme])
