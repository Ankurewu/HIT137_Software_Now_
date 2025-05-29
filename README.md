# HIT137_Software_Now_
This repository is created for 'Assignment 3' of the HIT137 Software Now unit.
# Forest Guardian & Premium Image Editor

This repository contains two Python applications demonstrating GUI and game development skills:

1. **Forest Guardian**: A side-scrolling action game built with Pygame.
2. **Premium Image Editor**: A Tkinter-based image editor with modern styling and common editing tools.

---

## 1. Forest Guardian (Pygame)

**Overview**: Guide your stick-figure hero through three levels of platforming action. Defeat enemies, collect health pickups, and face off against a boss in the final stage.

**Features**:

* Smooth camera that follows the player with lerp-based smoothing
* Platform collisions, wrap-around world
* Player projectiles with muzzle-flash and explosion particles
* Health, lives, and scoring system (50 points per minion, 200 for boss)
* Level progression: spawn increasingly challenging enemies, culminates in a boss encounter
* HUD displaying score and lives, with a “Boss Incoming!” alert in level 3
* Game over screen and restart (press R)

**Dependencies**:

* Python 3.8+
* Pygame 2.x

**Run**:

```bash
python forest_guardian.py
```

---

## 2. Premium Image Editor (Tkinter + OpenCV)

**Overview**: A lightweight photo editor featuring load/save, undo/redo, cropping, resizing, and filters—all wrapped in a dark, modern interface.

**Features**:

* Load/save PNG & JPEG images
* Undo/redo history (up to 20 steps)
* Crop by click-and-drag on canvas
* Zoom slider and spinbox (10%–200%) with fit-to-window on load
* Operations: Rotate 90°, Flip H/V, Blur, Grayscale, Invert, Sharpen, Brighten/Darken
* Keyboard shortcuts (e.g. Ctrl+O to load, Ctrl+S to save, Ctrl+Z/Y to undo/redo)
* Status bar for operation feedback
* Premium dark theme using ttk Styles

**Dependencies**:

* Python 3.8+
* tkinter (built-in)
* Pillow
* OpenCV (cv2)
* numpy

**Run**:

```bash
python image_editor.py
```

---

## Installation

1. Clone this repository:

   ```bash
   ```

git clone [https://github.com/yourusername/forest-and-editor.git](https://github.com/yourusername/forest-and-editor.git)
cd forest-and-editor

````

2. Create and activate a virtual environment:
   ```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\\Scripts\\activate  # Windows
````

3. Install dependencies:

   ```bash
   ```

pip install -r requirements.txt

```

4. Run either application as shown above.

---

## Project Structure

```

forest-and-editor/
├── forest\_guardian.py   # Pygame action game
├── image\_editor.py      # Tkinter-based image editor
├── README.md            # This file
├── requirements.txt     # pip dependencies
└── assets/              # (Optional) images, icons, etc.

```

---


*Happy coding!*

```
