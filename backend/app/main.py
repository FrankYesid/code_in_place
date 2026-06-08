# =============================================================================
# Word Guess Deluxe - Backend (Web Adapter)
# =============================================================================
# Este archivo actúa como el Adaptador Web en nuestra Arquitectura Hexagonal.
# Utiliza FastAPI para exponer los puertos de entrada a través de una API REST.
# =============================================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional, List
import uuid

# Importaciones del Dominio y Puertos
from .domain.models import GameState
from .domain.services import WordGuessService
from .adapters.persistence.file_repository import FileWordRepository

app = FastAPI(
    title="Word Guess Deluxe API",
    description="API para el juego de adivinar palabras con arquitectura hexagonal y temáticas."
)

# Configuración de CORS: Permite que el Frontend (React) se comunique con este Backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicialización de Componentes (Inyección de Dependencias Manual)
# El servicio contiene la lógica de negocio pura.
# El repositorio se encarga de escanear la carpeta 'lexicons' para cargar los temas.
word_service = WordGuessService()
word_repo = FileWordRepository("lexicons")

# Almacenamiento de estado en memoria (In-Memory Storage)
# Clave: game_id (UUID), Valor: Objeto GameState
games: Dict[str, GameState] = {}

# --- Modelos de Petición (Request Models) ---

class NewGameRequest(BaseModel):
    """Modelo para solicitar un nuevo juego con una temática opcional."""
    theme: Optional[str] = None

class GuessRequest(BaseModel):
    """Modelo para procesar un intento de letra."""
    game_id: str
    letter: str

class HintRequest(BaseModel):
    """Modelo para solicitar una pista."""
    game_id: str

# --- Endpoints / Rutas de la API ---

@app.get("/themes", summary="Obtener temáticas disponibles")
async def get_themes():
    """
    Escanea el repositorio y devuelve todos los nombres de temas cargados (.txt).
    """
    return word_repo.get_themes()

@app.post("/game/new", summary="Iniciar nueva partida")
async def create_game(request: Optional[NewGameRequest] = None):
    """
    Crea una nueva instancia de juego.
    1. Obtiene una palabra al azar (del tema elegido o aleatorio).
    2. Genera un ID único para la sesión.
    3. Inicializa el estado del juego mediante el Servicio de Dominio.
    """
    selected_theme = request.theme if request and request.theme else None
    
    # El repositorio maneja la lógica de elegir la palabra correcta
    secret_word = word_repo.get_random_word(selected_theme)
    
    # Determinar qué tema se terminó usando realmente
    actual_theme = selected_theme if selected_theme in word_repo.get_themes() else "Azar"

    game_id = str(uuid.uuid4())
    # El servicio de dominio crea el objeto de estado inicial
    state = word_service.create_new_game(secret_word, theme=actual_theme)
    games[game_id] = state
    
    return {"game_id": game_id, "state": state}

@app.get("/game/{game_id}", summary="Consultar estado de la partida")
async def get_game(game_id: str):
    """
    Recupera el estado actual de una partida específica usando su ID único.
    """
    if game_id not in games:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    return games[game_id]

@app.post("/game/guess", summary="Realizar una adivinanza")
async def make_guess(request: GuessRequest):
    """
    Procesa el intento de un jugador.
    1. Valida que el juego exista.
    2. Delega la lógica de 'adivinar' al Servicio de Dominio.
    3. Actualiza el almacenamiento en memoria.
    """
    if request.game_id not in games:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    
    current_state = games[request.game_id]
    # El servicio de dominio aplica las reglas de negocio (puntos, vidas, etc.)
    updated_state = word_service.make_guess(current_state, request.letter)
    games[request.game_id] = updated_state
    
    return updated_state

@app.post("/game/hint", summary="Solicitar una pista")
async def get_hint(request: HintRequest):
    """
    Revela una letra de la palabra secreta.
    1. Valida existencia del juego.
    2. Delega al servicio de dominio la lógica de revelación y penalización.
    """
    if request.game_id not in games:
        raise HTTPException(status_code=404, detail="Juego no encontrado")
    
    current_state = games[request.game_id]
    # El dominio se encarga de elegir la letra oculta y restar el costo de la pista
    updated_state = word_service.use_hint(current_state)
    games[request.game_id] = updated_state
    
    return updated_state

if __name__ == "__main__":
    import uvicorn
    # Lanzamiento del servidor Uvicorn en el puerto 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
