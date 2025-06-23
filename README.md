# Folder Flattener

**I was frustrated by ChatGPT's lack of multi-folder upload, so I made this.**


A quick, techy solution to flatten files from multiple folders into a single directory, no matter how nested your source folders are.

## What is it?

A dual-interface tool (GUI and web) to flatten files from multiple folders into one.

- **`flat.py`**: Native desktop app using wxPython for folder selection dialogs.
- **`flat_app.py`**: Streamlit web app for drag-and-drop flattening.

## Features

- Select multiple folders (desktop) or drag and drop (web) and flatten all contents into a single destination.
- Handles filename collisions by auto-renaming.
- Skips hidden folders and `__pycache__`.
- Simple, no-nonsense UI.

## Usage

### Desktop (wxPython)

```bash
pip install wxPython
python flat.py
```

Follow the dialogs to select source folders and a destination.

### Web (Streamlit)

```bash
https://un-folder-dk7aqxrcjrqwoxvyyxfayu.streamlit.app/
```

Drag and drop files, set a destination, and flatten!

## Requirements

- Python 3.x
- `wxPython` (for desktop)
- `streamlit` (for web)
