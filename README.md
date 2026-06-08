# Word Guess Deluxe - Final Project Code in Place 2026

Welcome to **Word Guess Deluxe**! An evolved, scalable, and visually stunning version of the classic word guessing game. This project has been designed following high software engineering standards, utilizing **Hexagonal Architecture** and modern web development technologies.

## 🌟 What's New: Dynamic Theme System
Unlike traditional versions, this project includes a **Massive Lexicon System by Themes**:
- **Real Categories**: Technology, Animals, Countries, and more.
- **Auto-Loading**: Just add a `.txt` file to the `lexicons` folder, and the game will recognize it instantly.
- **Interactive Selector**: A dedicated home screen to choose your challenge.

## 🏗️ Project Structure

The project is divided into two major ecosystems:

### 1. Backend (`/backend`) - The Brain
Implemented with **FastAPI** and following **Hexagonal Architecture** principles:
- **Domain**: Pure business rules (Scoring, Game Logic).
- **Ports**: Interfaces for data access.
- **Adapters**: Real implementations (REST API and File Persistence).
- **Lexicons**: Folder with word files organized by topics.

### 2. Frontend (`/frontend`) - The Experience
A "Deluxe" interface built with:
- **React 18 + TypeScript**: Robust component logic.
- **Tailwind CSS**: Dark style with neon accents and responsive design.
- **Canvas Confetti**: Celebration animations for victories.
- **Keyboard Support**: Play using your physical keyboard or the on-screen virtual one.

## 🛠️ Requirements
- **Python 3.9+**
- **Node.js 18+**
- **npm** (installed with Node.js)

## 📖 Quick Start Guide

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```
> The API runs at `http://localhost:8000`. You can see the interactive documentation at `/docs`.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
> Access `http://localhost:5173` to start playing.

## 🎯 "Deluxe" Features
- **Smart Scoring**: Earn points for correct guesses and bonuses for remaining lives.
- **Hint System**: Reveal letters strategically (cost: 10 pts).
- **Detailed Statistics**: View your performance for each game.
- **Fluid Navigation**: Change themes at any time using the Gamepad button.

---
*This project is the final result of the Code in Place 2026 course, demonstrating the integration of advanced programming logic and modern interface design.*
