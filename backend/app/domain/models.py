# =============================================================================
# Word Guess Models - Domain Models
# =============================================================================
# These models define the game state and constants.
# They are pure Python objects (using Pydantic for validation).
# =============================================================================

from pydantic import BaseModel
from typing import List

class GameState(BaseModel):
    """
    Represents the complete state of a Word Guess game session.
    This class is the 'heart' of the information in our domain.
    """
    secret_word: str      # The word the player must guess
    guessed_word: str     # Representation with dashes (e.g., "P-TH-N")
    guesses_left: int     # Remaining attempts before Game Over
    used_letters: List[str] # Letters the player has already tried
    score: int            # Accumulated score in the session
    correct_guesses: int  # Count of correct letter guesses
    wrong_guesses: int    # Count of incorrect letter guesses
    hints_used: int       # Number of hints requested
    game_over: bool = False # Indicates if the session has ended
    won: bool = False       # Indicates if the player won
    theme: str = "General"  # Topic of the current word

class GameConstants:
    """
    Fixed values that define scoring rules and difficulty.
    Centralizing them here makes it easy to adjust game balance.
    """
    INITIAL_GUESSES = 8       # Starting lives
    HINT_COST = 10            # Point cost for using a hint
    CORRECT_POINTS = 10       # Points earned for a correct guess
    WRONG_POINTS = -2         # Points lost for an incorrect guess
    WIN_BONUS = 50            # Bonus for guessing the entire word
    REMAINING_GUESS_BONUS = 5 # Bonus for each remaining life upon winning
