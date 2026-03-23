import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from tkinter import filedialog

from app.core.ops import ImageEnhancer


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Image Enhancer Tool")
        self.geometry("1000x700")

        # Image storage variables
        self.original_image = None  # Original loaded image (BGR format from OpenCV)
        self.manual_result = None  # Manually enhanced image (brightness/contrast)
        self.ai_result = None  # AI enhanced image (super-resolution)

        # Configure grid layout for responsive design
        self.grid_columnconfigure(0, weight=1)  # Left panel (controls)
        self.grid_columnconfigure(1, weight=3)  # Right panel (images)
        self.grid_rowconfigure(0, weight=1)

        # ========== LEFT FRAME (Controls) ==========
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        # ========== RIGHT FRAME (Image Display) ==========
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # ========== CONTROL WIDGETS (Left Panel) ==========

        # Load Image Button
        self.btn_load = ctk.CTkButton(
            self.left_frame,
            text="Load Image",
            command=self.load_image
        )
        self.btn_load.pack(pady=10)

        # Brightness Control
        self.lbl_brightness = ctk.CTkLabel(self.left_frame, text="Brightness: 20")
        self.lbl_brightness.pack()

        self.brightness_slider = ctk.CTkSlider(
            self.left_frame,
            from_=-100,
            to=100,
            command=self.on_brightness_change  # Real-time update callback
        )
        self.brightness_slider.set(20)
        self.brightness_slider.pack(pady=5)

        # Contrast Control
        self.lbl_contrast = ctk.CTkLabel(self.left_frame, text="Contrast: 1.4")
        self.lbl_contrast.pack()

        self.contrast_slider = ctk.CTkSlider(
            self.left_frame,
            from_=0.5,
            to=3,
            command=self.on_contrast_change  # Real-time update callback
        )
        self.contrast_slider.set(1.4)
        self.contrast_slider.pack(pady=5)

        # AI Enhancement Button
        self.btn_ai = ctk.CTkButton(
            self.left_frame,
            text="🤖 AI Enhance",
            command=self.ai_enhance_image
        )
        self.btn_ai.pack(pady=10)

        # ========== SAVE OPTIONS (Left Panel) ==========

        self.lbl_save = ctk.CTkLabel(self.left_frame, text="💾 Save Options:")
        self.lbl_save.pack(pady=(20, 5))

        # Save Manual Enhanced Image
        self.btn_save_manual = ctk.CTkButton(
            self.left_frame,
            text="Save Manual (Brightness)",
            command=lambda: self.save_image('manual'),
            fg_color="#2E7D32"  # Green color
        )
        self.btn_save_manual.pack(pady=5)

        # Save AI Enhanced Image
        self.btn_save_ai = ctk.CTkButton(
            self.left_frame,
            text="Save AI Enhanced",
            command=lambda: self.save_image('ai'),
            fg_color="#1565C0"  # Blue color
        )
        self.btn_save_ai.pack(pady=5)

        # Save Both Images
        self.btn_save_both = ctk.CTkButton(
            self.left_frame,
            text="💾 Save Both Images",
            command=self.save_both_images,
            fg_color="#6A1B9A"  # Purple color
        )
        self.btn_save_both.pack(pady=5)

        # ========== IMAGE DISPLAY (Right Panel) ==========

        # Original Image Label
        self.label_before = ctk.CTkLabel(self.right_frame, text="Original")
        self.label_before.pack(pady=10)

        # Enhanced Image Label (shows manual or AI result)
        self.label_after = ctk.CTkLabel(self.right_frame, text="Enhanced (Manual)")
        self.label_after.pack(pady=10)

    # ========== EVENT HANDLERS ==========

    def on_brightness_change(self, value):
        """
        Callback when brightness slider changes.
        Updates the label text and refreshes the manual enhancement.
        """
        self.lbl_brightness.configure(text=f"Brightness: {int(value)}")
        self.update_manual()

    def on_contrast_change(self, value):
        """
        Callback when contrast slider changes.
        Updates the label text and refreshes the manual enhancement.
        """
        self.lbl_contrast.configure(text=f"Contrast: {value:.1f}")
        self.update_manual()

    def load_image(self):
        """
        Open file dialog to load an image.
        Supports: JPG, JPEG, PNG, BMP, TIFF formats.
        Resets previous enhancement results when new image is loaded.
        """
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )

        if path:
            # Load image using OpenCV (returns BGR format)
            self.original_image = cv2.imread(path)

            # Reset previous results
            self.manual_result = None
            self.ai_result = None

            # Reset display label to manual mode
            self.label_after.configure(text="Enhanced (Manual)")
            self.update_manual()

    def update_manual(self, event=None):
        """
        Apply manual enhancements (brightness/contrast/sharpen) to original image.
        Updates both display labels: original (left) and enhanced (right).
        Called automatically when sliders change.
        """
        if self.original_image is None:
            return

        # Get current slider values
        brightness = int(self.brightness_slider.get())
        contrast = float(self.contrast_slider.get())

        # Apply enhancements using ImageEnhancer class
        enhancer = ImageEnhancer(self.original_image)
        self.manual_result = enhancer.enhance(brightness, contrast)

        # Update display
        self.display_image(self.original_image, self.label_before, "Original")
        self.display_image(self.manual_result, self.label_after, "Enhanced (Manual)")

    def ai_enhance_image(self):
        """
        Apply AI super-resolution enhancement using Real-ESRGAN.
        This is computationally intensive and runs in the main thread
        (UI will freeze during processing - consider threading for production).
        """
        if self.original_image is None:
            return

        try:
            print("*" * 50)
            print("🤖 Starting AI Enhancement...")
            print("⏳ This may take a while...")
            print("*" * 50)

            # Disable button during processing to prevent multiple clicks
            self.btn_ai.configure(state="disabled", text="Processing...")

            # Run AI enhancement
            enhancer = ImageEnhancer(self.original_image)
            self.ai_result = enhancer.ai_enhance()

            if self.ai_result is not None:
                # Switch display to AI result
                self.label_after.configure(text="Enhanced (AI)")
                self.display_image(self.ai_result, self.label_after, "Enhanced (AI)")
                print("✅ AI Enhancement Complete!")
            else:
                print("❌ Error: AI returned None")

        except Exception as e:
            print("❌ AI Error:", e)
            import traceback
            traceback.print_exc()

        finally:
            # Re-enable button regardless of success/failure
            self.btn_ai.configure(state="normal", text="🤖 AI Enhance")

    # ========== SAVE FUNCTIONS ==========

    def save_image(self, image_type):
        """
        Save a specific enhanced image to disk.

        Args:
            image_type: 'manual' for brightness/contrast result,
                     'ai' for AI super-resolution result
        """
        # Determine which image to save
        if image_type == 'manual':
            image_to_save = self.manual_result
            default_name = "manual_enhanced.jpg"
            title = "Save Manual Enhanced Image"
        elif image_type == 'ai':
            image_to_save = self.ai_result
            default_name = "ai_enhanced.png"  # PNG preserves better quality for AI
            title = "Save AI Enhanced Image"
        else:
            return

        # Validate image exists
        if image_to_save is None:
            print(f"❌ No {image_type} result to save!")
            return

        # Open save dialog
        path = filedialog.asksaveasfilename(
            title=title,
            defaultextension=".jpg" if image_type == 'manual' else ".png",
            filetypes=[
                ("JPEG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ],
            initialfile=default_name
        )

        # Save if user selected a path
        if path:
            cv2.imwrite(path, image_to_save)
            print(f"✅ Saved {image_type} image: {path}")

    def save_both_images(self):
        """
        Save both manual and AI enhanced images to a selected folder.
        Files are named automatically: manual_enhanced.jpg and ai_enhanced.png
        """
        # Check if at least one result exists
        if self.manual_result is None and self.ai_result is None:
            print("❌ No images to save!")
            return

        # Ask user for destination folder
        folder = filedialog.askdirectory(title="Select folder to save both images")

        if not folder:
            return

        import os
        saved_count = 0

        # Save manual enhanced image (JPEG for smaller size)
        if self.manual_result is not None:
            manual_path = os.path.join(folder, "manual_enhanced.jpg")
            cv2.imwrite(manual_path, self.manual_result)
            print(f"✅ Saved: {manual_path}")
            saved_count += 1

        # Save AI enhanced image (PNG for lossless quality)
        if self.ai_result is not None:
            ai_path = os.path.join(folder, "ai_enhanced.png")
            cv2.imwrite(ai_path, self.ai_result)
            print(f"✅ Saved: {ai_path}")
            saved_count += 1

        print(f"✅ Total saved: {saved_count} images in {folder}")

    # ========== UTILITY FUNCTIONS ==========

    def display_image(self, img, label, title=""):
        """
        Display an OpenCV image (BGR format) in a CTkLabel.
        Handles color conversion, resizing, and memory management.

        Args:
            img: OpenCV image (numpy array, BGR format)
            label: CTkLabel widget to display image in
            title: Optional text to show above image
        """
        if img is None:
            return

        # Convert BGR (OpenCV) to RGB (PIL/Pillow)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Convert to PIL Image
        pil_img = Image.fromarray(img_rgb)

        # Resize for display (maintains aspect ratio but fits in 350x350)
        pil_img = pil_img.resize((350, 350))

        # Convert to CTkImage for customtkinter
        ctk_img = ctk.CTkImage(light_image=pil_img, size=(350, 350))

        # Update label with image and title
        label.configure(image=ctk_img, text=title)

        # Keep reference to prevent garbage collection
        label.image = ctk_img


# ========== MAIN ENTRY POINT ==========

if __name__ == "__main__":
    # Create and run the application
    app = App()
    app.mainloop()