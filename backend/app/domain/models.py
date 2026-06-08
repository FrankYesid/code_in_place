# =============================================================================
# Word Guess Models - Modelos de Dominio
# =============================================================================
# Estos modelos definen el estado y las constantes del juego.
# Son objetos puros de Python (usando Pydantic para validación).
# =============================================================================

from pydantic import BaseModel
from typing import List

class GameState(BaseModel):
    """
    Representa el estado completo de una partida de Word Guess.
    Esta clase es el 'corazón' de la información en nuestro dominio.
    """
    secret_word: str      # La palabra que el jugador debe adivinar
    guessed_word: str     # Representación con guiones (ej. "P-TH-N")
    guesses_left: int     # Intentos restantes antes del Game Over
    used_letters: List[str] # Letras que el jugador ya ha intentado
    score: int            # Puntaje acumulado en la partida
    correct_guesses: int  # Contador de letras acertadas
    wrong_guesses: int    # Contador de letras fallidas
    hints_used: int       # Cuántas pistas se han solicitado
    game_over: bool = False # Indica si la partida ha terminado
    won: bool = False       # Indica si el jugador ganó
    theme: str = "General"  # Temática de la palabra actual

class GameConstants:
    """
    Valores fijos que definen las reglas de puntuación y dificultad.
    Centralizarlos aquí facilita ajustar el balance del juego.
    """
    INITIAL_GUESSES = 8       # Vidas iniciales
    HINT_COST = 10            # Costo en puntos por usar una pista
    CORRECT_POINTS = 10       # Puntos ganados por acierto
    WRONG_POINTS = -2         # Puntos perdidos por fallo
    WIN_BONUS = 50            # Bono por adivinar la palabra completa
    REMAINING_GUESS_BONUS = 5 # Bono por cada vida restante al ganar
