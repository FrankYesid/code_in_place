# Requerimientos y Guía del Backend

El backend está diseñado para ser ligero, rápido y fácil de extender gracias al uso de FastAPI y Arquitectura Hexagonal.

## 📋 Requerimientos Técnicos
- **Lenguaje**: Python 3.9 o superior.
- **Framework**: FastAPI (v0.111.0).
- **Servidor ASGI**: Uvicorn (v0.30.1).
- **Validación**: Pydantic (v2.7.4) para modelos de datos.

## 🛠️ Instalación y Configuración
1. Crear un entorno virtual: `python -m venv venv`
2. Activar entorno:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Instalar dependencias: `pip install -r requirements.txt`

## 📡 Endpoints de la API
- `POST /game/new`: Crea una nueva sesión de juego única.
- `GET /game/{game_id}`: Recupera el estado de una partida activa.
- `POST /game/guess`: Procesa una letra intentada. Requiere `game_id` y `letter`.
- `POST /game/hint`: Revela una letra a cambio de puntos. Requiere `game_id`.

## 📁 Archivos Clave
- `Lexicon.txt`: Base de datos de palabras en texto plano.
- `requirements.txt`: Lista de librerías necesarias.
- `app/main.py`: Punto de entrada del servidor y configuración de CORS.
