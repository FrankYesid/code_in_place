# Arquitectura del Proyecto: Word Guess Deluxe

Este proyecto utiliza una **Arquitectura Hexagonal** (también conocida como Puertos y Adaptadores). El objetivo principal es desacoplar la lógica de negocio central de las tecnologías externas.

## 🏗️ Cómo está construido

### 1. El Núcleo (Dominio)
Ubicado en `backend/app/domain/`. Es la parte más importante y no tiene dependencias externas.
- **Modelos (`models.py`)**: Define qué es un juego, su estado y las constantes de puntuación.
- **Servicios (`services.py`)**: Implementa las reglas del juego (cómo se procesa una letra, cuándo se gana, cómo funcionan las pistas).

### 2. Puertos (Interfaces)
Ubicados en `backend/app/ports/`. Definen el "contrato" de lo que el sistema necesita para funcionar.
- **WordRepository**: Define que necesitamos obtener palabras, pero no le importa si vienen de un archivo, una base de datos o una nube.

### 3. Adaptadores (Implementaciones)
Ubicados en `backend/app/adapters/`. Son los que conectan el núcleo con el mundo real.
- **Adaptador de Persistencia (`file_repository.py`)**: Implementa el puerto usando el sistema de archivos local (`Lexicon.txt`).
- **Adaptador de Entrada (API REST en `main.py`)**: Utiliza FastAPI para exponer el juego al frontend.

## 🔄 Flujo de Datos
1. El **Frontend** (React) envía una acción (ej. adivinar una letra).
2. El **Adaptador Web** (FastAPI) recibe la petición y llama al **Servicio de Dominio**.
3. El **Dominio** procesa la regla de negocio y actualiza el estado.
4. Si se necesita una palabra nueva, el Dominio usa un **Puerto**, que es ejecutado por el **Adaptador de Archivo**.
5. El resultado vuelve al Frontend para ser visualizado de forma atractiva.
