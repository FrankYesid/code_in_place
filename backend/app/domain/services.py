# =============================================================================
# Word Guess Service - Business Logic
# =============================================================================
# This service contains the game's business rules.
# In Hexagonal Architecture, the Domain knows nothing about APIs or Files.
# It only knows HOW to play Word Guess.
# =============================================================================

import random
from .models import GameState, GameConstants

class WordGuessService:
    """
    Domain service containing the game's business logic.
    """

    def create_new_game(self, secret_word: str, theme: str = "General") -> GameState:
        """
        Initializes a new game state from a secret word and its theme.
        """
        return GameState(
            secret_word=secret_word.upper(),
            guessed_word="-" * len(secret_word),
            guesses_left=GameConstants.INITIAL_GUESSES,
            used_letters=[],
            score=0,
            correct_guesses=0,
            wrong_guesses=0,
            hints_used=0,
            theme=theme
        )

    def make_guess(self, state: GameState, letter: str) -> GameState:
        """
        Processes a player's attempt when choosing a letter.
        Applies scoring rules and updates the state.
        """
        letter = letter.upper()

        # Avoid processing if game ended or letter was already used
        if state.game_over or letter in state.used_letters or len(letter) != 1:
            return state

        state.used_letters.append(letter)

        if letter in state.secret_word:
            # Success logic
            state.guessed_word = self._update_word(state.secret_word, state.guessed_word, letter)
            state.correct_guesses += 1
            state.score += GameConstants.CORRECT_POINTS
        else:
            # Failure logic
            state.guesses_left -= 1
            state.wrong_guesses += 1
            state.score += GameConstants.WRONG_POINTS

        # Update win/loss status
        self._check_game_status(state)
        
        return state

    def use_hint(self, state: GameState) -> GameState:
        """
        Reveals a letter the player hasn't guessed yet.
        Costs points but helps progress.
        """
        if state.game_over:
            return state

        # Find indices of letters not yet revealed
        hidden_indices = [i for i, char in enumerate(state.guessed_word) if char == "-"]
        
        if hidden_indices:
            idx = random.choice(hidden_indices)
            hint_letter = state.secret_word[idx]
            
            # Reveal the letter in all its positions
            state.guessed_word = self._update_word(state.secret_word, state.guessed_word, hint_letter)
            state.hints_used += 1
            state.score -= GameConstants.HINT_COST
            
            self._check_game_status(state)

        return state

    def _update_word(self, secret: str, guessed: str, letter: str) -> str:
        """
        Internal method to update the visual representation of the word.
        """
        new_word = list(guessed)
        for i, char in enumerate(secret):
            if char == letter:
                new_word[i] = letter
        return "".join(new_word)

    def _check_game_status(self, state: GameState):
        """
        Determines if the player has won or run out of lives.
        """
        if state.guessed_word == state.secret_word:
            state.game_over = True
            state.won = True
            # Final bonuses
            state.score += GameConstants.WIN_BONUS
            state.score += state.guesses_left * GameConstants.REMAINING_GUESS_BONUS
        elif state.guesses_left <= 0:
            state.game_over = True
            state.won = False
