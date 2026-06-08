# Word Guess Deluxe - Proyecto Final Code in Place 2026

¡Bienvenido a **Word Guess Deluxe**! Una versión evolucionada, escalable y visualmente impactante del clásico juego de adivinanza de palabras. Este proyecto ha sido diseñado siguiendo los estándares más altos de ingeniería de software, utilizando **Arquitectura Hexagonal** y tecnologías modernas de desarrollo web.

## 🌟 Lo Nuevo: Sistema de Temáticas Dinámico
A diferencia de las versiones tradicionales, este proyecto incluye un sistema de **Léxicos Masivos por Temáticas**:
- **Categorías Reales**: Tecnología, Animales, Países y más.
- **Carga Automática**: Solo agrega un archivo `.txt` en la carpeta `lexicons` y el juego lo reconocerá al instante.
- **Selector Interactivo**: Una pantalla de inicio dedicada para elegir tu desafío.

## 🏗️ Estructura del Proyecto

El proyecto se divide en dos grandes ecosistemas:

### 1. Backend (`/backend`) - El Cerebro
Implementado con **FastAPI** y siguiendo la **Arquitectura Hexagonal**:
- **Dominio**: Reglas de negocio puras (Puntuación, Lógica de Juego).
- **Puertos**: Interfaces para el acceso a datos.
- **Adaptadores**: Implementaciones reales (API REST y Persistencia en Archivos).
- **Lexicons**: Carpeta con archivos de palabras organizados por temas.

### 2. Frontend (`/frontend`) - La Experiencia
Una interfaz "Deluxe" construida con:
- **React 18 + TypeScript**: Lógica de componentes robusta.
- **Tailwind CSS**: Estilo oscuro con acentos neón y diseño responsivo.
- **Canvas Confetti**: Animaciones de celebración para victorias.
- **Soporte de Teclado**: Juega usando tu teclado físico o el virtual en pantalla.

## 🛠️ Requisitos
- **Python 3.9+**
- **Node.js 18+**
- **npm** (instalado con Node.js)

## 📖 Guía Rápida de Inicio

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```
> La API corre en `http://localhost:8000`. Puedes ver la documentación interactiva en `/docs`.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
> Accede a `http://localhost:5173` para empezar a jugar.

## 🎯 Características "Deluxe"
- **Puntuación Inteligente**: Gana puntos por aciertos y bonos por vidas restantes.
- **Sistema de Pistas**: Revela letras estratégicamente (costo de 10 pts).
- **Estadísticas Detalladas**: Visualiza tu rendimiento en cada partida.
- **Navegación Fluida**: Cambia de temática en cualquier momento desde el botón de la Gamepad.

---
*Este proyecto es el resultado final del curso Code in Place 2026, demostrando la integración de lógica de programación avanzada y diseño de interfaces modernas.*
