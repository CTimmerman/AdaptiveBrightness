# Adaptive Brightness
Changes display brightness to match webcam brightness.

## Installation

```
python -m venv .venv
```

If Bash: `source .venv/bin/activate`

If Windows: `.venv\Scripts\activate`

```
pip install -r requirements.txt
```

## Usage
```
python adaptive_brightness.py [device id] [debug]
```
Device id default is `-1` to `10`.
Adding `debug` shows the frames.

To exit the virtual environment, use:
```
deactivate
```