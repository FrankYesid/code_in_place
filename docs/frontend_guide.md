# Requerimientos y Guía del Frontend

El frontend es una interfaz moderna de alta fidelidad ("Deluxe") construida para ofrecer la mejor experiencia de usuario.

## 📋 Requerimientos Técnicos
- **Entorno**: Node.js v18+ y npm.
- **Framework**: React v18 (con Hooks para gestión de estado).
- **Lenguaje**: TypeScript para tipado seguro.
- **Estilos**: Tailwind CSS v3 para diseño atómico y responsivo.
- **Iconos**: Lucide React.
- **Efectos**: Canvas Confetti.

## 🎨 Estilo Visual
- **Paleta de Colores**: Fondo oscuro (`#0f172a`), superficies (`#1e293b`), y acentos vibrantes en Indigo, Rosa y Ámbar.
- **UX**: Soporte para teclado físico (event listeners globales) y teclado virtual táctil.
- **Feedback**: Animaciones de victoria, vibración visual de letras y barras de vida dinámicas.

## 🛠️ Instalación y Configuración
1. Entrar a la carpeta: `cd frontend`
2. Instalar módulos: `npm install`
3. Ejecutar desarrollo: `npm run dev`

## 🔌 Conexión con Backend
La URL base está configurada en `App.tsx` como `http://localhost:8000`. Utiliza **Axios** para manejar las promesas y peticiones asíncronas de forma limpia.
