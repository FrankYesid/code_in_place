# Themes and Word Customization Guide

Word Guess Deluxe allows you to easily expand the game by adding new words and categories.

## 📁 File Structure
Words are organized in the `backend/lexicons/` folder. Each `.txt` file in this folder automatically becomes a **Theme** in the game.

### How to add a new theme
1. Create a `.txt` file in `backend/lexicons/`.
2. The file name will be the theme name (e.g., `Sports.txt`).
3. Add one word per line. The system will automatically convert them to uppercase and trim whitespace.

## ⚙️ How the Process Works
1. **Automatic Scanning**: When the backend starts, the `FileWordRepository` adapter scans the folder and loads all themes into memory.
2. **Dynamic Selection**: The frontend queries the `/themes` endpoint to display selection buttons to the user.
3. **Scalability**: You can have hundreds of files and thousands of words without affecting performance, as only one is chosen at random per game.

## 💡 Theme Ideas
- **Movies**: Matrix, Inception, Gladiator.
- **Food**: Pizza, Burger, Sushi.
- **Advanced Programming**: Microservices, Kubernetes, Docker.

## 🛠️ Rule Modification
If you want to change difficulty per theme (e.g., fewer lives for hard themes), you can modify the `WordGuessService` to accept custom configurations based on the theme name.
