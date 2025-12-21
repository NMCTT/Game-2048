# Game 2048
<img width="1943" height="1215" alt="image" src="https://github.com/user-attachments/assets/38d466a4-49c0-452e-b177-4e5a67de547a" />
# 🎮 2048 Game - Project by 404 Not Found

![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white) ![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg?style=for-the-badge) ![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)

This is a complete 2048 puzzle game implemented in Python using the Pygame library. Developed by team **404 Not Found**, the project features a modular object-oriented design and optimized matrix algorithms.

---

## ✨ Key Features

* **Optimized Game Logic:** Efficient matrix manipulation for tile compression and merging.
* **Graphical UI:** Smooth rendering with custom color palettes for different tile values.
* **Game States:** Includes "Game Over" and "Win" detection with interactive dialogs.
* **Score Tracking:** Real-time score calculation as you merge tiles.
* **Full Screen Support:** Optimized for immersive gameplay.

---

## 📂 Project Structure

The project is organized into dedicated modules for better maintainability:

```bash
2048_Project/
├── main.py          # Entry point; initializes and launches the application.
├── app.py           # Core application class; manages the main loop and scenes.
├── game.py          # UI Controller; handles rendering and game state updates.
├── logic.py         # The "Brain"; handles matrix movement and merging logic.
├── settings.py      # Configuration; defines screen, colors, and constants.
├── assets/          # Resources; stores images, fonts, and sounds.
└── README.md        # Project documentation.
🛠 Core Algorithms
The game's intelligence lies in logic.py, which processes movements through three main steps:

Compress: Shifts all non-zero tiles to the target direction.

Merge: Combines adjacent tiles of the same value and updates the score.

Double Compress: Re-aligns tiles after merging to ensure no gaps remain.
