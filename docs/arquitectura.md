# Project Architecture: Word Guess Deluxe

This project utilizes **Hexagonal Architecture** (also known as Ports and Adapters). The main goal is to decouple the core business logic from external technologies.

## 🏗️ How it's Built

### 1. The Core (Domain)
Located in `backend/app/domain/`. It is the most important part and has no external dependencies.
- **Models (`models.py`)**: Defines what a game is, its state, and scoring constants.
- **Services (`services.py`)**: Implements game rules (how a letter is processed, when a win occurs, how hints work).

### 2. Ports (Interfaces)
Located in `backend/app/ports/`. They define the "contract" of what the system needs to function.
- **WordRepository**: Defines that we need to retrieve words, but doesn't care if they come from a file, a database, or an external API.

### 3. Adapters (Implementations)
Located in `backend/app/adapters/`. These connect the core with the real world.
- **Persistence Adapter (`file_repository.py`)**: Implements the port using the local file system (`lexicons/` folder).
- **Input Adapter (REST API in `main.py`)**: Uses FastAPI to expose the game to the frontend.

## 🔄 Data Flow
1. The **Frontend** (React) sends an action (e.g., guessing a letter).
2. The **Web Adapter** (FastAPI) receives the request and calls the **Domain Service**.
3. The **Domain** processes the business rule and updates the state.
4. If a new word is needed, the Domain uses a **Port**, which is executed by the **File Adapter**.
5. The result returns to the Frontend to be visually displayed.
