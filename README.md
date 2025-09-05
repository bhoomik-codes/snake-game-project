# 🐍 Snake Game

A classic Snake game built with **Python** and **Pygame**, featuring a main menu, difficulty levels, pause functionality, and a high-score logging system with player names and timestamps. I plan to make a C++ and unity version of the game too

---

## 🎮 Features

* **Classic Gameplay**: Move the snake, eat food, and grow longer while avoiding collisions.
* **Difficulty Levels**: Choose between `Easy`, `Medium`, and `Hard` (different snake speeds).
* **High Scores**: Stores player name, score, and date-time in a log file.
* **Pause/Resume**: Press **P** to pause or resume the game.
* **Menu System**:

  * Start Game
  * Select Difficulty
  * View High Scores (last 5 shown)
  * Quit

---

## 🖥️ Requirements

Make sure you have the following installed:

* Python 3.x
* [Pygame](https://www.pygame.org/)
  Install using:

  ```bash
  pip install pygame
  ```

---

## ▶️ How to Run

1. Clone or download this repository.
2. Run the `main.py` file:

   ```bash
   python main.py
   ```
3. Use the menu to start the game and enjoy!

---

## 🎹 Controls

| Key                   | Action                                 |
| --------------------- | -------------------------------------- |
| **Arrow Keys / WASD** | Move Snake                             |
| **P**                 | Pause / Resume                         |
| **Enter / Space**     | Select menu option                     |
| **Backspace**         | Delete character (while entering name) |

---

## 🏆 High Score System

* After **Game Over**, you’ll be asked to enter your name.
* High scores are stored in `highscores.log` in the format:

  ```
  PlayerName,YYYY-MM-DD HH:MM:SS,Score
  ```
* The **last 5 scores** are displayed in the menu under *High Scores*.

---

## 📂 Project Structure

```
Snake-Game/
│── main.py          # Main game script
│── highscores.log   # High score records (auto-created after first game)
│── highscores.txt   # High score records (in the txt format for easy readability)
│── README.md        # Project documentation
```

---

## 🚀 Future Improvements

* Add sound effects & background music
* Power-ups and obstacles
* Multiplayer mode
* Online leaderboard

---
