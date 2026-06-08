# =============================================================================
# Word Guess Deluxe - Backend (Web Adapter)
# =============================================================================
# This file acts as the Web Adapter in our Hexagonal Architecture.
# It uses FastAPI to expose entry ports through a REST API.
# =============================================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List
import uuid

# Domain and Ports Imports
from .domain.models import GameState
from .domain.services import WordGuessService
from .adapters.persistence.file_repository import FileWordRepository

app = FastAPI(
    title="Word Guess Deluxe API",
    description="API for the word guessing game with hexagonal architecture and themes."
)

# CORS Configuration: Allows the Frontend (React) to communicate with this Backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Component Initialization (Manual Dependency Injection)
# The service contains pure business logic.
# The repository handles scanning the 'lexicons' folder to load themes.
word_service = WordGuessService()
word_repo = FileWordRepository("lexicons")

# In-memory state storage
# Key: game_id (UUID), Value: GameState object
games: Dict[str, GameState] = {}

# --- Request Models ---

class NewGameRequest(BaseModel):
    """Model to request a new game with an optional theme."""
    theme: Optional[str] = None

class GuessRequest(BaseModel):
    """Model to process a letter guess."""
    game_id: str
    letter: str

class HintRequest(BaseModel):
    """Model to request a hint."""
    game_id: str

# --- API Endpoints / Routes ---

@app.get("/themes", summary="Get available themes")
async def get_themes():
    """
    Scans the repository and returns all loaded theme names (.txt).
    """
    return word_repo.get_themes()

@app.post("/game/new", summary="Start new game")
async def create_game(request: Optional[NewGameRequest] = None):
    """
    Creates a new game instance.
    1. Gets a random word (from the chosen theme or random).
    2. Generates a unique ID for the session.
    3. Initializes the game state via the Domain Service.
    """
    selected_theme = request.theme if request and request.theme else None
    
    # The repository handles the logic of choosing the correct word
    secret_word = word_repo.get_random_word(selected_theme)
    
    # Determine which theme was actually used
    actual_theme = selected_theme if selected_theme in word_repo.get_themes() else "Random"

    game_id = str(uuid.uuid4())
    # The domain service creates the initial state object
    state = word_service.create_new_game(secret_word, theme=actual_theme)
    games[game_id] = state
    
    return {"game_id": game_id, "state": state}

@app.get("/game/{game_id}", summary="Check game status")
async def get_game(game_id: str):
    """
    Retrieves the current state of a specific game using its unique ID.
    """
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    return games[game_id]

@app.post("/game/guess", summary="Make a guess")
async def make_guess(request: GuessRequest):
    """
    Processes a player's attempt.
    1. Validates that the game exists.
    2. Delegates the 'guessing' logic to the Domain Service.
    3. Updates in-memory storage.
    """
    if request.game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    current_state = games[request.game_id]
    # The domain service applies business rules (points, lives, etc.)
    updated_state = word_service.make_guess(current_state, request.letter)
    games[request.game_id] = updated_state
    
    return updated_state

@app.post("/game/hint", summary="Request a hint")
async def get_hint(request: HintRequest):
    """
    Reveals a letter of the secret word.
    1. Validates game existence.
    2. Delegates to the domain service for revelation and penalty logic.
    """
    if request.game_id not in games:
        raise HTTPException(status_code=404, detail="Game not found")
    
    current_state = games[request.game_id]
    # The domain handles choosing the hidden letter and subtracting the hint cost
    updated_state = word_service.use_hint(current_state)
    games[request.game_id] = updated_state
    
    return updated_state

if __name__ == "__main__":
    import uvicorn
    # Launching Uvicorn server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
