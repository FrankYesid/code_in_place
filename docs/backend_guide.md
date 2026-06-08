# Backend Requirements and Guide

The backend is designed to be lightweight, fast, and easy to extend using FastAPI and Hexagonal Architecture.

## 📋 Technical Requirements
- **Language**: Python 3.9 or higher.
- **Framework**: FastAPI (v0.111.0).
- **ASGI Server**: Uvicorn (v0.30.1).
- **Validation**: Pydantic (v2.7.4) for data models.

## 🛠️ Installation and Setup
1. Create a virtual environment: `python -m venv venv`
2. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## 📡 API Endpoints
- `GET /themes`: Retrieves the list of available themes from the `.txt` files.
- `POST /game/new`: Creates a new unique game session. Accepts an optional `theme`.
- `GET /game/{game_id}`: Retrieves the state of an active game.
- `POST /game/guess`: Processes a guessed letter. Requires `game_id` and `letter`.
- `POST /game/hint`: Reveals a letter in exchange for points. Requires `game_id`.

## 📁 Key Files
- `lexicons/`: Folder containing thematic word lists.
- `requirements.txt`: List of required libraries.
- `app/main.py`: Server entry point and CORS configuration.
