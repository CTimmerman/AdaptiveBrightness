# Adaptive Brightness
Changes display brightness to match webcam brightness.

## Installation

 - `python -m venv .venv`
 - Bash: `source .venv/bin/activate`
 - Windows: `.venv\Scripts\activate`
 - `pip install -r requirements.txt`

## Usage
```
python adaptive_brightness.py [camera id] [display id] [debug]
```
Camera id default is `0` to (not including) `10`. Display default is `0`.
Adding `debug` shows info and if supported, frames, the first of which is saved:
 - Bash: `xdg-open debug.jpg`
 - Windows: `start debug.jpg`

<kbd>Ctrl</kbd>+<kbd>Break</kbd> or <kbd>Ctrl</kbd>+<kbd>C</kbd> in the shell to exit.

To exit the virtual environment, use: `deactivate`
