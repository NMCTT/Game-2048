# Game 2048

<img width="1943" height="1215" alt="image" src="https://github.com/user-attachments/assets/38d466a4-49c0-452e-b177-4e5a67de547a" />
# 🎮 2048 Game - Project by 404 Not Found

![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white) ![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg?style=for-the-badge) ![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)

This is a complete 2048 puzzle game implemented in Python using the Pygame library. Developed by team **404 Not Found**, the project features a modular object-oriented design and optimized matrix algorithms.

---

## Key Features

- **Optimized Game Logic:** Efficient matrix manipulation for tile compression and merging.
- **Graphical UI:** Smooth rendering with custom color palettes for different tile values.
- **Game States:** Includes "Game Over" and "Win" detection with interactive dialogs.
- **Score Tracking:** Real-time score calculation as you merge tiles.
- **Full Screen Support:** Optimized for immersive gameplay.

---

## Project Structure

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
```

## Core Algorithms

The "brain" of the game is implemented in `logic.py`, which handles the 4x4 matrix transformations. The movement logic is processed through a sequential pipeline:

1. **Compress**: Shift all non-zero tiles to the target edge, removing empty gaps.
2. **Merge**: Combine adjacent tiles of equal value and update the game score.
3. **Second Compress**: Re-align tiles after merging to ensure no gaps remain.
4. **Spawn**: Randomly add a new tile (2 or 4) to an empty spot if the board changed.

### Logic Implementation Preview:

Here is a simplified look at how the `merge` function works in `logic.py`:

```python
def merge(mat, score):
    for i in range(4):
        for j in range(3):
            # If adjacent tiles are the same and not zero
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                mat[i][j] *= 2      # Double the value
                mat[i][j + 1] = 0   # Clear the merged tile
                score += mat[i][j]   # Update score
                changed = True
    return mat, changed, score
```

## Installation & Usage

### 1. Requirements

Before running the game, ensure you have the following installed:

- **Python 3.8+**: The core programming language.
- **Pygame library**: Used for rendering the game interface and handling events.

### 2. Setup

Follow these steps to set up the project on your local machine:

```bash
# Clone the repository
git clone [https://github.com/404-not-found/2048-python.git](https://github.com/404-not-found/2048-python.git)

# Navigate to the project directory
cd 2048-python

# Install the required Pygame library
pip install pygame
```
