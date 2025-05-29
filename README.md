# Premium Image Editor & Forest Guardian

This repository contains two Python applications showcasing GUI and game development:

1. **Premium Image Editor (Tkinter + OpenCV)**
2. **Forest Guardian (Pygame)**

---

## 1. Premium Image Editor (Tkinter + OpenCV)

A lightweight, modern image editing tool with a dark theme and common photo operations.

### Features

* Load and save PNG & JPEG images
* Undo/redo (up to 20 steps)
* Crop by click-and-drag on the canvas
* Zoom controls (slider & spinbox from 10% to 200%)
* Automatic fit-to-window on load
* Image operations:

  * Rotate 90°
  * Flip horizontally/vertically
  * Gaussian blur
  * Grayscale conversion
  * Color inversion
  * Sharpen filter
  * Brighten & darken adjustments
* Keyboard shortcuts (e.g., Ctrl+O to load, Ctrl+S to save, Ctrl+Z/Y to undo/redo)
* Status bar for action feedback
* Premium dark theme via ttk Styles

### Dependencies

* Python 3.8 or newer
* tkinter (built‑in)
* Pillow
* OpenCV (cv2)
* numpy

### Run

```bash
python image_editor.py
```

---

## 2. Forest Guardian (Pygame)

A side-scrolling action-platformer where you guide a stick-figure hero through three levels and face a boss.

### Features

* Smooth camera following with interpolation
* Platform collision and wrap-around world
* Player shooting with muzzle-flash and explosion particles
* Health, lives, and scoring system (50 pts per minion, 200 pts for boss)
* Three levels of enemy waves, culminating in a boss fight
* HUD displaying score and lives
* "Boss Incoming!" alert in level 3
* Game over screen and restart (press R)

### Dependencies

* Python 3.8 or newer
* Pygame 2.x

### Run

```bash
python forest_guardian.py
```

---

## Installation

1. **Clone** the repository:

   ```bash
   ```

git clone [https://github.com/yourusername/your-repo.git](https://github.com/yourusername/your-repo.git)
cd your-repo

````

2. **Create** and **activate** a virtual environment:

   ```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
````

3. **Install** dependencies:

   ```bash
   ```

pip install -r requirements.txt

```

4. **Run** the desired application as shown above.

---

## Project Structure

```

├── image\_editor.py       # Premium Image Editor application
├── forest\_guardian.py    # Forest Guardian game
├── README.md             # Project overview and instructions
├── requirements.txt      # Python dependencies
└── assets/               # Optional assets (icons, images)

```

*Happy coding!*

```
