# Frontend Requirements and Guide

The frontend is a modern high-fidelity ("Deluxe") interface built to provide the best user experience.

## 📋 Technical Requirements
- **Environment**: Node.js v18+ and npm.
- **Framework**: React v18 (using Hooks for state management).
- **Language**: TypeScript for type safety.
- **Styles**: Tailwind CSS v3 for atomic and responsive design.
- **Icons**: Lucide React.
- **Effects**: Canvas Confetti.

## 🎨 Visual Style
- **Color Palette**: Dark background (`#0f172a`), surfaces (`#1e293b`), and vibrant Indigo, Pink, and Amber accents.
- **UX**: Global event listeners for physical keyboard support and a touch-friendly virtual keyboard.
- **Feedback**: Victory animations, letter visual shakes, and dynamic health bars.

## 🛠️ Installation and Setup
1. Enter the folder: `cd frontend`
2. Install modules: `npm install`
3. Run development mode: `npm run dev`

## 🔌 Backend Connection
The base URL is configured in `App.tsx` as `http://localhost:8000`. It uses **Axios** to handle promises and asynchronous HTTP requests cleanly.
