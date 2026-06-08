# =============================================================================
# Word Guess Service - Lógica de Negocio
# =============================================================================
# Este servicio contiene las reglas de negocio del juego.
# En Arquitectura Hexagonal, el Dominio no sabe nada de APIs ni de Archivos.
# Solo sabe CÓMO se juega al Word Guess.
# =============================================================================

import random
from .models import GameState, GameConstants

class WordGuessService:
    """
    Servicio de dominio que contiene la lógica de negocio del juego.
    """

    def create_new_game(self, secret_word: str, theme: str = "General") -> GameState:
        """
        Inicializa un nuevo estado de juego a partir de una palabra secreta y su temática.
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
        Procesa el intento de un jugador al elegir una letra.
        Aplica las reglas de puntuación y actualiza el estado.
        """
        letter = letter.upper()

        # Evitar procesar si el juego terminó o la letra ya se usó
        if state.game_over or letter in state.used_letters or len(letter) != 1:
            return state

        state.used_letters.append(letter)

        if letter in state.secret_word:
            # Lógica para acierto
            state.guessed_word = self._update_word(state.secret_word, state.guessed_word, letter)
            state.correct_guesses += 1
            state.score += GameConstants.CORRECT_POINTS
        else:
            # Lógica para fallo
            state.guesses_left -= 1
            state.wrong_guesses += 1
            state.score += GameConstants.WRONG_POINTS

        # Actualizar estado de victoria/derrota
        self._check_game_status(state)
        
        return state

    def use_hint(self, state: GameState) -> GameState:
        """
        Revela una letra que el jugador aún no ha adivinado.
        Cuesta puntos pero ayuda a avanzar.
        """
        if state.game_over:
            return state

        # Buscar índices de letras que aún no han sido reveladas
        hidden_indices = [i for i, char in enumerate(state.guessed_word) if char == "-"]
        
        if hidden_indices:
            idx = random.choice(hidden_indices)
            hint_letter = state.secret_word[idx]
            
            # Revelar la letra en todas sus posiciones
            state.guessed_word = self._update_word(state.secret_word, state.guessed_word, hint_letter)
            state.hints_used += 1
            state.score -= GameConstants.HINT_COST
            
            self._check_game_status(state)

        return state

    def _update_word(self, secret: str, guessed: str, letter: str) -> str:
        """
        Método interno para actualizar la representación visual de la palabra.
        """
        new_word = list(guessed)
        for i, char in enumerate(secret):
            if char == letter:
                new_word[i] = letter
        return "".join(new_word)

    def _check_game_status(self, state: GameState):
        """
        Determina si el jugador ha ganado o se ha quedado sin vidas.
        """
        if state.guessed_word == state.secret_word:
            state.game_over = True
            state.won = True
            # Bonificaciones finales
            state.score += GameConstants.WIN_BONUS
            state.score += state.guesses_left * GameConstants.REMAINING_GUESS_BONUS
        elif state.guesses_left <= 0:
            state.game_over = True
            state.won = False
