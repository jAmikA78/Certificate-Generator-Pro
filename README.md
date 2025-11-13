# Certificate Generator Pro

A lightweight GUI tool to generate personalized certificates in bulk using a certificate template image, custom fonts, and an adjustable text placement preview.

---

## At a glance

- Project: Certificate Generator Pro
- Language: Python (Tkinter GUI)
- Minimum Python: 3.8+
- Key libraries: Pillow (PIL), tkinter (standard library)
- Current version: 2.3

This tool lets you load a certificate template image, position and style text (name), preview it on the template with zoom and custom color/font, then generate PNG certificate files for a list of names.

## Features

- Graphical UI built with Tkinter
- Load PNG/JPG certificate templates
- Select TrueType/OpenType fonts (.ttf / .otf)
- Live preview with zoom and click-to-set position
- Predefined and custom hex color selection for text
- Enter multiple names (one-per-line) and generate certificates in bulk
- Filename sanitization and collision handling
- Progress bar and basic input validation

## Installation

Recommended: create and activate a virtual environment, then install dependencies.

```bash
# create venv (optional but recommended)
python -m venv .venv
source .venv/bin/activate    # on Windows (Git Bash): source .venv/Scripts/activate

# install required package
pip install Pillow
```

Note: Tkinter is included in the standard library for most Python distributions. On some Linux distributions you may need to install a system package (for example `python3-tk`).

## Usage

1. Launch the app:

```bash
python main.py
```

2. UI workflow:

- Click "Browse Image" and choose your certificate template (PNG/JPG).
- Optionally click "Select Font" to choose a .ttf/.otf font (recommended for better typography).
- Use the Zoom slider to adjust the preview.
- Choose "Center" or "Custom Position" for the text. If Custom, click on the preview to set X/Y coordinates or enter them manually.
- Set font size and color (predefined or custom hex color). Use the color picker for convenience.
- Enter names (one per line) into the "Enter Names" textbox.
- Click "Generate Certificates" and choose an output folder. Generated files are saved as PNGs in the selected folder.

Tips:

- Keep your certificate image high resolution for best results.
- Use fonts with clear glyph shapes for readability when saving as PNG.

## Example

- If you enter two names:

```
Jane Doe
John Smith
```

The app will generate `certificate_Jane_Doe.png` and `certificate_John_Smith.png` (unsafe characters removed and spaces replaced by underscores). If a file exists, the app appends a counter to avoid overwriting.

## Troubleshooting

- "No image loaded" — select a template image first.
- Font errors — select a compatible .ttf/.otf font or allow the app to fall back to the system/default font.
- Unable to write to folder — choose a folder with write permissions (for example your Downloads or Desktop folder).
- If preview looks different from final output: preview scales the image to a smaller size; generated files use the original image resolution.

## Development notes

- Main file: `main.py` — contains the GUI and core certificate generation logic.
- Key dependency: `Pillow` is used for image drawing and font rendering.
- The app sanitizes file names and guards against more than 1000 names at once.

## Contributing

Contributions are welcome. For small fixes and improvements:

1. Fork the repo
2. Create a branch with a clear name
3. Open a PR describing the change and rationale

Suggested improvements:

- Add CLI mode for headless generation
- Add unit tests around filename sanitization and text placement math
- Export to PDF in addition to PNG

## License

MIT
