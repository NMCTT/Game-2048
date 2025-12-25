#  2048 Game - Project by 404 Not Found

![Python](https://img.shields.io/badge/python-3.10-blue.svg?style=for-the-badge&logo=python&logoColor=white) ![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg?style=for-the-badge) 

This is a complete 2048 puzzle game implemented in Python using the Pygame library. Developed by team **404 Not Found**, the project features a modular object-oriented design and optimized matrix algorithms.

---

## UI Overview

**Menu**

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a005ee2d-6458-45bf-993c-267e984c77fe" />

---

**Dialogs**

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/46ba6fb1-31ff-446c-a000-53419321d097" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3e188cf8-5504-47dd-92bb-1ff8415589d2" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/070195e1-f9cd-46d5-b4cb-8798cbc848e6" />

---

**Normal Match**

![1](https://github.com/user-attachments/assets/a38f7917-4488-4efe-9d3d-5193c05a86ed)

---

**AI Mode**

![2](https://github.com/user-attachments/assets/e6136145-891a-4d12-bc18-7300a54675cd)

## Key Features

- **Optimized Game Logic:** Efficient matrix manipulation for tile compression and merging.
- **Graphical UI:** Smooth rendering with custom color palettes for different tile values.
- **Game States:** Includes "Game Over" and "Win" detection with interactive dialogs.
- **Score Tracking:** Real-time score calculation as you merge tiles.
- **Full Screen Support:** Optimized for immersive gameplay.
- **AI Mode & Smart Solver:** Beyond manual play, the project features an **AI Mode** where the computer automatically makes decisions to reach the 2048 tile.
## Project Structure

The project is organized into dedicated modules for better maintainability:

```bash
Game-2048/
├── game/
│   ├── asset/images         # Contains all of the sprites and textures in the game.
│   ├── core/
│   │   └── env_2048.py      # OpenAI Gym wrapper
│   ├── rl/                  
│   │   ├── agent_dqn.py     # Class DQNAgent, the network learns how to act in a game or environment by trial and error.
│   │   ├── dqn_model.py     # Defines the deep Q-Network for 2048.
│   │   ├── memory.py        # Replay Buffer.
│   │   └── train_dqn.py     # For training the AI.
│   ├── scenes/
│   │   ├── asset.py         # Asset loader.
│   │   ├── board.py         # Main gameplay scene.
│   │   ├── intro.py         # Intro Scene (aka Menu).
│   │   ├── play_agent.py    # Main gameplay scene designed specifically for AI mode.
│   │   └── tile.py          # Contains the class Tile for animating moving tiles.
│   ├── settings.py          # System Configuration.
│   └── app.py               # Application Controller: Manages game flow, scene transitions (Intro, Board), and coordinates AI modes.
├── dqn_2048.pth             # Storing AI model's weights and parameters for AI mode.
├── main.py                  # Application entry point.
├── requirements.txt         # Requirements to run the game.
└── README.md                # Project documentation and setup guide.
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

- **Python 3.10**: The core programming language.
- **Pygame 2.5.2**: Used for rendering the game interface and handling events.
- **Torch 2.3.0 and Numpy 1.26.4**: Used for AI.
- **tqdm**: Library for rendering progress bars.

### 2. Setup

Follow these steps to set up the project on your local machine:

```bash
# Clone the repository
git clone https://github.com/NMCTT/Game-2048.git

# Navigate to the project directory
cd Game-2048

# Install all dependencies from requirements.txt
pip install -r requirements.txt

# Run the game
python main.py
```

## Project Timeline and Team Members

**Lecturer:** Lê Đức Khoan

| Members | Student ID |
| :--- | :--- |
| Nguyễn Vĩnh Phú | 25120220 |
| Trịnh Đặng Nhật Minh | 25120210 |
| Sok Minh | 25120209 |
| Đoàn Tấn Phát | 25120217 |
| Nguyễn Đức Thịnh | 25120232 |
| Đặng Phúc Lộc | 25120203 |

---

<img width="1943" height="1215" alt="image" src="https://github.com/user-attachments/assets/38d466a4-49c0-452e-b177-4e5a67de547a" />

---
