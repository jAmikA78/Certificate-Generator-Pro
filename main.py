import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import re
import sys

class CertificateGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Certificate Generator Pro")
        self.root.geometry("800x800")
        self.root.configure(bg="#e6ecf0")
        
        # Variables
        self.cert_image_path = tk.StringVar()
        self.font_path_var = tk.StringVar()
        self.preview_img = None
        self.original_img = None
        self.base_preview_size = (600, 400)  # Base size for 100% zoom
        self.zoom_level = tk.DoubleVar(value=100.0)  # Default 100%
        self.default_font_size = 72
        self.cursor_pos_var = tk.StringVar(value="X: 0, Y: 0")
        self.font_color_var = tk.StringVar(value="black")  # Default color
        self.hex_color_var = tk.StringVar(value="#000000")  # Default hex color (black)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main canvas for scrolling
        main_canvas = tk.Canvas(self.root, bg="#e6ecf0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        main_frame = ttk.Frame(main_canvas)
        
        main_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        main_canvas.bind_all("<Button-4>", lambda e: main_canvas.yview_scroll(-1, "units"))
        main_canvas.bind_all("<Button-5>", lambda e: main_canvas.yview_scroll(1, "units"))
        
        # Title
        ttk.Label(
            main_frame,
            text="📜 Certificate Generator Pro",
            style="Title.TLabel"
        ).pack(pady=(0, 20))
        
        # Style configuration
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 22, "bold"), foreground="#2c3e50")
        style.configure("Section.TLabel", font=("Helvetica", 14, "bold"), foreground="#2c3e50")
        style.configure("TButton", font=("Helvetica", 10, "bold"))
        style.configure("TLabel", font=("Helvetica", 10), background="#e6ecf0")
        
        # Certificate Image Section
        self.create_section(main_frame, "1. Select Certificate Template")
        img_frame = ttk.Frame(main_frame)
        img_frame.pack(fill=tk.X, pady=5)
        
        self.img_entry = ttk.Entry(
            img_frame,
            textvariable=self.cert_image_path,
            width=50,
            state="readonly"
        )
        self.img_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            img_frame,
            text="Browse Image",
            command=self.select_image,
            style="TButton"
        ).pack(side=tk.LEFT)
        
        # Preview Section
        preview_frame = ttk.LabelFrame(
            main_frame,
            text="Preview (Click to Set Position)",
            padding=10
        )
        preview_frame.pack(fill=tk.BOTH, pady=15)
        
        # Zoom control
        zoom_frame = ttk.Frame(preview_frame)
        zoom_frame.pack(fill=tk.X, pady=5)
        ttk.Label(zoom_frame, text="Zoom:").pack(side=tk.LEFT, padx=5)
        ttk.Scale(
            zoom_frame,
            from_=25,
            to=200,
            orient=tk.HORIZONTAL,
            variable=self.zoom_level,
            command=self.update_preview
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Label(
            zoom_frame,
            textvariable=self.zoom_level,
            text="100.0%"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Label(zoom_frame, text="%").pack(side=tk.LEFT)
        
        # Scrollable preview
        self.canvas = tk.Canvas(preview_frame, bg="white", highlightthickness=0)
        preview_scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=preview_scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.image_label = ttk.Label(
            self.scrollable_frame,
            text="📷 No image loaded\n\nClick 'Browse Image' to get started",
            foreground="#95a5a6",
            font=("Helvetica", 12),
            justify="center"
        )
        self.image_label.pack(padx=10, pady=10)
        
        # Cursor position display
        ttk.Label(
            preview_frame,
            textvariable=self.cursor_pos_var,
            font=("Helvetica", 9, "italic"),
            foreground="#7f8c8d"
        ).pack(anchor=tk.W, padx=10)
        
        # Position Settings Section
        self.create_section(main_frame, "2. Text Position")
        position_frame = ttk.Frame(main_frame)
        position_frame.pack(fill=tk.X, pady=5)
        
        self.position_mode = tk.StringVar(value="center")
        
        ttk.Radiobutton(
            position_frame,
            text="Center (Default)",
            variable=self.position_mode,
            value="center",
            command=self.toggle_position_inputs
        ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        ttk.Radiobutton(
            position_frame,
            text="Custom Position",
            variable=self.position_mode,
            value="custom",
            command=self.toggle_position_inputs
        ).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        custom_pos_frame = ttk.Frame(position_frame)
        custom_pos_frame.grid(row=1, column=0, columnspan=3, sticky=tk.W, padx=30, pady=5)
        
        ttk.Label(
            custom_pos_frame,
            text="X Position:"
        ).grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.x_position_entry = ttk.Entry(custom_pos_frame, width=10)
        self.x_position_entry.grid(row=0, column=1, padx=5)
        self.x_position_entry.insert(0, "0")
        self.x_position_entry.config(state="disabled")
        
        ttk.Label(
            custom_pos_frame,
            text="Y Position:"
        ).grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        
        self.y_position_entry = ttk.Entry(custom_pos_frame, width=10)
        self.y_position_entry.grid(row=0, column=3, padx=5)
        self.y_position_entry.insert(0, "0")
        self.y_position_entry.config(state="disabled")
        
        ttk.Label(
            custom_pos_frame,
            text="(in pixels from top-left corner, or click on preview)",
            font=("Helvetica", 8, "italic"),
            foreground="#7f8c8d"
        ).grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(2, 0))
        
        # Font Settings Section
        self.create_section(main_frame, "3. Font Settings")
        font_frame = ttk.Frame(main_frame)
        font_frame.pack(fill=tk.X, pady=5)

        ttk.Label(font_frame, text="Font File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.font_entry = ttk.Entry(
            font_frame,
            textvariable=self.font_path_var,
            width=40,
            state="readonly"
        )
        self.font_entry.grid(row=0, column=1, padx=10)
        
        ttk.Button(
            font_frame,
            text="Select Font",
            command=self.select_font
        ).grid(row=0, column=2)
        
        ttk.Label(font_frame, text="Font Size:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.font_size_entry = ttk.Spinbox(
            font_frame,
            from_=10,
            to=200,
            width=10
        )
        self.font_size_entry.delete(0, tk.END)
        self.font_size_entry.insert(0, str(self.default_font_size))
        self.font_size_entry.grid(row=1, column=1, sticky=tk.W, padx=10)
        
        ttk.Label(font_frame, text="Font Color:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        color_frame = ttk.Frame(font_frame)
        color_frame.grid(row=2, column=1, sticky=tk.W, padx=10)
        
        # Predefined color options
        colors = [("Black", "black"), ("Blue", "#1a5490"), ("Gold", "#d4af37"), ("Red", "#c0392b")]
        for col, (text, color) in enumerate(colors):
            ttk.Radiobutton(
                color_frame,
                text=text,
                variable=self.font_color_var,
                value=color,
                command=self.update_hex_from_radio
            ).grid(row=0, column=col, sticky=tk.W, padx=5)
        
        # Custom color option
        ttk.Radiobutton(
            color_frame,
            text="Custom",
            variable=self.font_color_var,
            value="custom",
            command=self.update_from_hex_entry
        ).grid(row=0, column=len(colors), sticky=tk.W, padx=5)
        
        # Hex color entry
        self.hex_color_entry = ttk.Entry(
            color_frame,
            textvariable=self.hex_color_var,
            width=10
        )
        self.hex_color_entry.grid(row=0, column=len(colors) + 1, padx=5)
        self.hex_color_entry.bind("<KeyRelease>", self.validate_hex_color)
        
        # Color wheel button
        ttk.Button(
            color_frame,
            text="🎨 Pick Color",
            command=self.open_color_chooser
        ).grid(row=0, column=len(colors) + 2, padx=5)
        
        # Preview Text Section
        self.create_section(main_frame, "4. Preview Text")
        ttk.Label(
            main_frame,
            text="Preview Name (for positioning):",
            font=("Helvetica", 9, "italic"),
            foreground="#7f8c8d"
        ).pack(anchor=tk.W)
        
        self.preview_text_var = tk.StringVar(value="Sample Name")
        ttk.Entry(
            main_frame,
            textvariable=self.preview_text_var,
            width=70
        ).pack(pady=5)
        
        ttk.Button(
            main_frame,
            text="Preview Text on Certificate",
            command=self.preview_text,
            style="TButton"
        ).pack(pady=5)
        
        # Names Section
        self.create_section(main_frame, "5. Enter Names")
        ttk.Label(
            main_frame,
            text="Enter one name per line (max 1000 names):",
            font=("Helvetica", 9, "italic"),
            foreground="#7f8c8d"
        ).pack(anchor=tk.W)
        
        self.names_entry = tk.Text(
            main_frame,
            height=6,
            width=70,
            font=("Helvetica", 11),
            relief="flat",
            bd=1,
            background="white"
        )
        self.names_entry.pack(pady=5)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.pack(pady=10)
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="🎓 Generate Certificates",
            command=self.generate_certificates,
            style="TButton"
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame,
            text="Reset All",
            command=self.reset_form,
            style="TButton"
        ).pack(side=tk.LEFT, padx=10)
        
        # Footer
        ttk.Label(
            main_frame,
            text="Made with ❤️ | v2.3 | Zoomable Preview",
            font=("Helvetica", 8),
            foreground="#95a5a6"
        ).pack(side=tk.BOTTOM, pady=10)
    
    def create_section(self, parent, title):
        """Create a section header"""
        ttk.Label(
            parent,
            text=title,
            style="Section.TLabel"
        ).pack(anchor=tk.W, pady=(15, 5))
    
    def toggle_position_inputs(self):
        """Enable/disable position input fields based on selection"""
        state = "normal" if self.position_mode.get() == "custom" else "disabled"
        self.x_position_entry.config(state=state)
        self.y_position_entry.config(state=state)
        if self.position_mode.get() == "custom":
            self.image_label.bind("<Motion>", self.update_cursor_position)
            self.image_label.bind("<Button-1>", self.set_position)
        else:
            self.image_label.unbind("<Motion>")
            self.image_label.unbind("<Button-1>")
            self.cursor_pos_var.set("X: 0, Y: 0")
        self.update_preview(None)  # Refresh preview to reflect position mode
    
    def update_cursor_position(self, event):
        """Update cursor position display when hovering over image"""
        if not self.original_img:
            return
        
        # Get canvas coordinates
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Scale to original image coordinates
        orig_width, orig_height = self.original_img.size
        zoom_factor = self.zoom_level.get() / 100.0
        prev_width, prev_height = self.preview_img.width(), self.preview_img.height()
        
        scale_x = orig_width / (prev_width / zoom_factor)
        scale_y = orig_height / (prev_height / zoom_factor)
        
        orig_x = int(canvas_x * scale_x)
        orig_y = int(canvas_y * scale_y)
        
        self.cursor_pos_var.set(f"X: {orig_x}, Y: {orig_y}")
    
    def set_position(self, event):
        """Set X/Y position entries when clicking on image"""
        if not self.original_img or self.position_mode.get() != "custom":
            return
        
        # Get canvas coordinates
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Scale to original image coordinates
        orig_width, orig_height = self.original_img.size
        zoom_factor = self.zoom_level.get() / 100.0
        prev_width, prev_height = self.preview_img.width(), self.preview_img.height()
        
        scale_x = orig_width / (prev_width / zoom_factor)
        scale_y = orig_height / (prev_height / zoom_factor)
        
        orig_x = int(canvas_x * scale_x)
        orig_y = int(canvas_y * scale_y)
        
        # Update entry fields
        self.x_position_entry.delete(0, tk.END)
        self.x_position_entry.insert(0, str(orig_x))
        self.y_position_entry.delete(0, tk.END)
        self.y_position_entry.insert(0, str(orig_y))
        
        # Trigger preview update
        self.preview_text()
    
    def update_preview(self, event):
        """Update preview image based on zoom level"""
        if not self.original_img:
            return
        
        try:
            zoom_factor = self.zoom_level.get() / 100.0
            new_size = (
                int(self.base_preview_size[0] * zoom_factor),
                int(self.base_preview_size[1] * zoom_factor)
            )
            
            img_copy = self.original_img.copy()
            img_copy.thumbnail(new_size, Image.Resampling.LANCZOS)
            self.preview_img = ImageTk.PhotoImage(img_copy)
            self.image_label.config(image=self.preview_img, text="")
            self.image_label.image = self.preview_img
            
            # Update scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Refresh preview text if applicable
            if self.preview_text_var.get().strip():
                self.preview_text()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update preview:\n{e}")
    
    def select_image(self):
        """Select certificate template image"""
        path = filedialog.askopenfilename(
            title="Select Certificate Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp"),
                ("PNG Files", "*.png"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("All Files", "*.*")
            ]
        )
        if not path:
            return
        
        self.cert_image_path.set(path)
        
        try:
            self.original_img = Image.open(path)
            self.update_preview(None)  # Update with current zoom level
            
            width, height = self.original_img.size
            messagebox.showinfo(
                "Image Loaded",
                f"✅ Image loaded successfully!\n\n"
                f"Dimensions: {width} x {height} pixels\n\n"
                f"Tip: If using custom position:\n"
                f"• X range: 0 to {width}\n"
                f"• Y range: 0 to {height}\n"
                f"• Click on preview to set position\n"
                f"• Use zoom slider to adjust view"
            )
            
            # Bind mouse events if in custom mode
            if self.position_mode.get() == "custom":
                self.image_label.bind("<Motion>", self.update_cursor_position)
                self.image_label.bind("<Button-1>", self.set_position)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{e}")
            self.cert_image_path.set("")
    
    def select_font(self):
        """Select custom font file"""
        path = filedialog.askopenfilename(
            title="Select Font File",
            filetypes=[
                ("TrueType Font", "*.ttf"),
                ("OpenType Font", "*.otf"),
                ("All Files", "*.*")
            ]
        )
        if path:
            self.font_path_var.set(path)
            self.preview_text()
    
    def update_hex_from_radio(self):
        """Update hex color entry when a predefined color is selected"""
        if self.font_color_var.get() != "custom":
            self.hex_color_var.set(self.font_color_var.get())
            self.hex_color_entry.config(foreground="black")
            self.preview_text()
    
    def update_from_hex_entry(self):
        """Update font color when hex entry is used or custom is selected"""
        if self.font_color_var.get() == "custom":
            self.validate_hex_color(None)
            self.preview_text()
    
    def validate_hex_color(self, event):
        """Validate hex color input and update font_color_var"""
        hex_color = self.hex_color_var.get().strip()
        if self.font_color_var.get() != "custom":
            return
        
        # Check if the input is a valid hex color
        if re.match(r'^#[0-9A-Fa-f]{6}$', hex_color):
            self.font_color_var.set(hex_color)
            self.hex_color_entry.config(foreground="black")
            self.preview_text()
        else:
            self.hex_color_entry.config(foreground="red")  # Indicate invalid input
            self.font_color_var.set("black")  # Fallback to black
            self.preview_text()
    
    def open_color_chooser(self):
        """Open color chooser dialog and update hex color"""
        color = colorchooser.askcolor(title="Choose Font Color")[1]  # Returns hex color or None
        if color:
            self.font_color_var.set("custom")
            self.hex_color_var.set(color.upper())
            self.validate_hex_color(None)
    
    def get_font_color(self):
        """Get valid font color, with fallback to black if invalid"""
        color = self.font_color_var.get()
        if color == "custom":
            color = self.hex_color_var.get()
        if re.match(r'^#[0-9A-Fa-f]{6}$', color) or color in ["black", "white"]:
            return color
        messagebox.showwarning("Warning", "Invalid color format. Using black as fallback.")
        return "black"
    
    def preview_text(self):
        """Preview text on certificate"""
        if not self.original_img:
            messagebox.showwarning("Warning", "Please select a certificate image first")
            return
        
        try:
            img = self.original_img.copy()
            draw = ImageDraw.Draw(img)
            
            font = self.get_font()
            font_color = self.get_font_color()
            preview_text = self.preview_text_var.get().strip() or "Sample Name"
            
            width, height = img.size
            bbox = draw.textbbox((0, 0), preview_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            if self.position_mode.get() == "custom":
                try:
                    x = int(self.x_position_entry.get()) - text_width / 2
                    y = int(self.y_position_entry.get()) - text_height / 2
                    if x < 0 or y < 0 or x > width or y > height:
                        messagebox.showwarning("Warning", "Position coordinates out of image bounds")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Invalid position coordinates")
                    return
            else:
                x = (width - text_width) / 2
                y = (height - text_height) / 2
            
            draw.text((x, y), preview_text, fill=font_color, font=font)
            
            zoom_factor = self.zoom_level.get() / 100.0
            new_size = (
                int(self.base_preview_size[0] * zoom_factor),
                int(self.base_preview_size[1] * zoom_factor)
            )
            
            img_copy = img.copy()
            img_copy.thumbnail(new_size, Image.Resampling.LANCZOS)
            self.preview_img = ImageTk.PhotoImage(img_copy)
            self.image_label.config(image=self.preview_img, text="")
            self.image_label.image = self.preview_img
            
            # Update scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview text:\n{e}")
    
    def get_font(self):
        """Get font with error handling"""
        try:
            font_size = int(self.font_size_entry.get())
            if font_size < 1 or font_size > 500:
                raise ValueError("Font size out of range")
                
            font_path = self.font_path_var.get().strip()
            if font_path and os.path.exists(font_path):
                return ImageFont.truetype(font_path, font_size)
            
            # Try system fonts
            system_fonts = ["arial.ttf", "times.ttf", "helvetica.ttf"]
            for sys_font in system_fonts:
                try:
                    return ImageFont.truetype(sys_font, font_size)
                except:
                    continue
                    
            # Fallback to default
            messagebox.showwarning(
                "Font Warning",
                "Using default font. For better results, select a custom font."
            )
            return ImageFont.load_default()
            
        except ValueError:
            messagebox.showerror("Error", "Font size must be a number between 1 and 500")
            raise
        except Exception as e:
            messagebox.showwarning("Font Error", f"Error loading font: {e}\nUsing default font.")
            return ImageFont.load_default()
    
    def validate_output_dir(self, output_dir):
        """Validate if output directory is writable"""
        try:
            test_file = os.path.join(output_dir, ".test_write")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            return True
        except:
            return False
    
    def generate_certificates(self):
        """Generate certificates for all names"""
        img_path = self.cert_image_path.get()
        if not img_path:
            messagebox.showerror("Error", "Please select a certificate image")
            return
        
        names_text = self.names_entry.get("1.0", "end").strip()
        if not names_text:
            messagebox.showerror("Error", "Please enter at least one name")
            return
        
        names = [n.strip() for n in names_text.split("\n") if n.strip()]
        if len(names) > 1000:
            messagebox.showerror("Error", "Maximum 1000 names allowed")
            return
        
        default_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        output_dir = filedialog.askdirectory(
            title="Select Save Location",
            initialdir=default_downloads
        )
        if not output_dir:
            messagebox.showinfo("Canceled", "No folder selected. Operation canceled.")
            return
        
        if not self.validate_output_dir(output_dir):
            messagebox.showerror("Error", "Selected folder is not writable")
            return
        
        try:
            font = self.get_font()
            font_color = self.get_font_color()
            success_count = 0
            failed_names = []
            total_names = len(names)
            
            self.progress_var.set(0)
            self.root.update()
            
            for i, name in enumerate(names):
                try:
                    img = Image.open(img_path).convert("RGB")
                    draw = ImageDraw.Draw(img)
                    width, height = img.size
                    
                    bbox = draw.textbbox((0, 0), name, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    if self.position_mode.get() == "custom":
                        try:
                            x = int(self.x_position_entry.get()) - text_width / 2
                            y = int(self.y_position_entry.get()) - text_height / 2
                            if x < 0 or y < 0 or x > width or y > height:
                                raise ValueError("Position coordinates out of bounds")
                        except ValueError as e:
                            failed_names.append(f"{name}: {str(e)}")
                            continue
                    else:
                        x = (width - text_width) / 2
                        y = (height - text_height) / 2
                    
                    draw.text((x, y), name, fill=font_color, font=font)
                    
                    safe_name = re.sub(r'[^\w\s-]', '', name).strip().replace(" ", "_")
                    save_path = os.path.join(output_dir, f"certificate_{safe_name}.png")
                    
                    counter = 1
                    base_path = save_path
                    while os.path.exists(save_path):
                        save_path = os.path.join(output_dir, f"certificate_{safe_name}_{counter}.png")
                        counter += 1
                    
                    img.save(save_path, "PNG", quality=95)
                    success_count += 1
                    
                    # Update progress
                    self.progress_var.set((i + 1) / total_names * 100)
                    self.root.update()
                    
                except Exception as e:
                    failed_names.append(f"{name}: {str(e)}")
            
            # Show results
            if success_count == total_names:
                messagebox.showinfo(
                    "Success! 🎉",
                    f"✅ All {success_count} certificates generated successfully!\n\n"
                    f"Saved to:\n{output_dir}"
                )
            elif success_count > 0:
                messagebox.showwarning(
                    "Partial Success",
                    f"✅ {success_count} certificates generated successfully\n"
                    f"❌ {len(failed_names)} failed\n\n"
                    f"Failed names:\n" + "\n".join(failed_names[:5])
                )
            else:
                messagebox.showerror(
                    "Failed",
                    f"❌ All certificates failed to generate\n\n"
                    f"Errors:\n" + "\n".join(failed_names[:5])
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
    
    def reset_form(self):
        """Reset all form inputs"""
        self.cert_image_path.set("")
        self.font_path_var.set("")
        self.position_mode.set("center")
        self.x_position_entry.delete(0, tk.END)
        self.x_position_entry.insert(0, "0")
        self.y_position_entry.delete(0, tk.END)
        self.y_position_entry.insert(0, "0")
        self.toggle_position_inputs()
        self.font_size_entry.delete(0, tk.END)
        self.font_size_entry.insert(0, str(self.default_font_size))
        self.font_color_var.set("black")
        self.hex_color_var.set("#000000")
        self.hex_color_entry.config(foreground="black")
        self.names_entry.delete("1.0", tk.END)
        self.preview_text_var.set("Sample Name")
        self.zoom_level.set(100.0)
        self.image_label.config(
            image="",
            text="📷 No image loaded\n\nClick 'Browse Image' to get started"
        )
        self.cursor_pos_var.set("X: 0, Y: 0")
        self.preview_img = None
        self.original_img = None
        self.progress_var.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = CertificateGenerator(root)
    root.mainloop()