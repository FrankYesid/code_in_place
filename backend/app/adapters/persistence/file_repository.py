# =============================================================================
# File Repository Adapter - Adaptador de Persistencia
# =============================================================================
# Este adaptador implementa el puerto 'WordRepository'.
# Se encarga de la comunicación con el sistema de archivos (Lexicon.txt).
# Si en el futuro queremos usar una Base de Datos, solo crearíamos un nuevo
# adaptador sin cambiar el resto del sistema.
# =============================================================================

import random
import os
from typing import List, Dict
from ...ports.repositories import WordRepository

class FileWordRepository(WordRepository):
    """
    Adaptador que lee palabras desde archivos .txt en una carpeta de léxicos.
    Cada archivo representa una temática.
    """
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.backup_words = ["PYTHON", "CODE", "INPLACE", "HEXAGONAL"]
        self._cache: Dict[str, List[str]] = {}
        self._load_all_lexicons()

    def _load_all_lexicons(self):
        """Carga todos los archivos .txt de la carpeta de léxicos."""
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path, exist_ok=True)
            return

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".txt"):
                theme_name = filename[:-4]  # Quitar .txt
                file_path = os.path.join(self.folder_path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        words = [line.strip().upper() for line in f if line.strip()]
                        if words:
                            self._cache[theme_name] = words
                except Exception as e:
                    print(f"Error cargando léxico {theme_name}: {e}")

    def get_themes(self) -> List[str]:
        """Retorna los nombres de las temáticas cargadas."""
        return list(self._cache.keys())

    def get_random_word(self, theme: str = None) -> str:
        """Obtiene una palabra aleatoria de una temática específica o al azar."""
        if not self._cache:
            return random.choice(self.backup_words)

        selected_theme = theme if theme in self._cache else random.choice(list(self._cache.keys()))
        return random.choice(self._cache[selected_theme])
