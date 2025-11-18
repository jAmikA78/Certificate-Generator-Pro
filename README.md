# Certificate Generator Pro

## Project Summary
Certificate Generator Pro is a simple, lightweight desktop tool that helps you create personalized certificates in bulk. Just load a template image, pick your fonts, position the text with a live preview, and enter a list of names—it handles the rest, saving each one as a PNG file.

## Key Features
- Easy-to-use graphical interface built with Python's Tkinter.
- Supports PNG and JPG certificate templates.
- Choose custom fonts (TTF or OTF files) and text colors.
- Live preview with zoom and click-to-place text positioning.
- Bulk generation from a list of names, with automatic filename cleanup.
- Progress bar to track your batch.

## Project Structure
- `main.py`: The heart of the app—handles the GUI, image processing, and certificate creation.

## Steps to Clone the Repository
1. Open your terminal or command prompt.
2. Run: `git clone https://github.com/jAmikA78/Certificate-Generator-Pro.git`
3. Navigate into the folder: `cd Certificate-Generator-Pro`

## Installation Instructions
1. Make sure you have Python 3.8 or higher installed.
2. It's a good idea to create a virtual environment: `python -m venv cert_env` (then activate it with `source cert_env/bin/activate` on macOS/Linux or `cert_env\Scripts\activate` on Windows).
3. Install the only needed library: `pip install Pillow`.
4. Note: Tkinter comes with Python, but on some Linux systems, you might need to install it via your package manager (e.g., `sudo apt install python3-tk`).

## Usage Instructions
1. Launch the app: `python main.py`.
2. Select your certificate template image (PNG or JPG).
3. Pick a font file (TTF or OTF) and choose the text color.
4. In the preview window, zoom in/out and click where you want the name placed—adjust size and style as needed.
5. Enter names in the text box (one per line for bulk) or just one for a single certificate.
6. Hit "Generate Certificates"—watch the progress bar, and find your new PNG files in the output folder.

**Quick Example**:  
Paste two names like:  
```
Ahmed Ibrahim
Ahmed Hamam 
```
Click generate, and you'll get files named `John_Doe_certificate.png` and `Jane_Smith_certificate.png`.

**Tips**: Use high-res templates for crisp results, and stick to clear, readable fonts.

## Requirements/Prerequisites
- Python 3.8+
- Pillow library (for image handling)
- Tkinter (standard in Python, but check Linux setup)

---

*Licensed under the MIT License.*
