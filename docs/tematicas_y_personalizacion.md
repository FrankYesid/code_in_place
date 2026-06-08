# Guía de Temáticas y Personalización de Palabras

Word Guess Deluxe permite expandir el juego fácilmente añadiendo nuevas palabras y categorías.

## 📁 Estructura de Archivos
Las palabras están organizadas en la carpeta `backend/lexicons/`. Cada archivo `.txt` en esta carpeta se convierte automáticamente en una **Temática** dentro del juego.

### Cómo agregar un nuevo tema
1. Crea un archivo `.txt` en `backend/lexicons/`.
2. El nombre del archivo será el nombre del tema (ej. `Deportes.txt`).
3. Agrega una palabra por línea. El sistema las convertirá automáticamente a mayúsculas y limpiará espacios en blanco.

## ⚙️ Cómo funciona el Proceso
1. **Escaneo Automático**: Al iniciar el backend, el adaptador `FileWordRepository` escanea la carpeta y carga todos los temas en memoria.
2. **Selección Dinámica**: El frontend consulta el endpoint `/themes` para mostrar los botones de selección al usuario.
3. **Escalabilidad**: Puedes tener cientos de archivos y miles de palabras sin afectar el rendimiento, ya que solo se elige una al azar por partida.

## 💡 Ideas para Temáticas
- **Películas**: Matrix, Inception, Gladiator.
- **Comida**: Pizza, Hamburguesa, Sushi.
- **Programación Avanzada**: Microservicios, Kubernetes, Docker.

## 🛠️ Modificación de Reglas
Si deseas cambiar la dificultad por tema (ej. menos vidas para temas difíciles), puedes modificar el `WordGuessService` para aceptar configuraciones personalizadas basadas en el nombre del tema.
