# Barcode Generator (Desktop App)

A simple desktop application written in Python for generating barcodes with a GUI (Tkinter).  
Supports multiple barcode formats and exports in different file types (SVG, EPS, PNG, JPEG).

## Features

- Graphical user interface (Tkinter)
- Supports:
  - **EAN-13**
  - **Code 128**
- Export formats:
  - **SVG** (vector)
  - **EPS**
  - **PNG**
  - **JPEG**
- Basic validation for EAN-13 codes
- Works as a standalone `.exe` on Windows using PyInstaller

## Requirements

- Python 3.10+
- pip

Python dependencies:

```bash
pip install python-barcode pillow
