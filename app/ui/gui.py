import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from tkinter import filedialog

from app.core.ops import ImageEnhancer


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Image Enhancer Tool")
        self.geometry("1000x700")

        self.image = None

        # Layout grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Frames
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # ===== Controls (LEFT) =====
        self.btn_load = ctk.CTkButton(self.left_frame, text="Load Image", command=self.load_image)
        self.btn_load.pack(pady=10)

        self.brightness_slider = ctk.CTkSlider(self.left_frame, from_=-100, to=100, command=self.update_image)
        self.brightness_slider.set(20)
        self.brightness_slider.pack(pady=10)

        self.contrast_slider = ctk.CTkSlider(self.left_frame, from_=0.5, to=3, command=self.update_image)
        self.contrast_slider.set(1.4)
        self.contrast_slider.pack(pady=10)




        self.btn_ai = ctk.CTkButton(self.left_frame, text="AI Enhance", command=self.ai_enhance_image)
        self.btn_ai.pack(pady=10)

        self.btn_save = ctk.CTkButton(self.left_frame, text="Save Image", command=self.save_image)
        self.btn_save.pack(pady=10)

        # ===== Images (RIGHT) =====
        self.label_before = ctk.CTkLabel(self.right_frame, text="Original")
        self.label_before.pack(pady=10)

        self.label_after = ctk.CTkLabel(self.right_frame, text="Enhanced")
        self.label_after.pack(pady=10)

    def save_image(self):
        if self.image is None:
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
        )

        if path:
            brightness = int(self.brightness_slider.get())
            contrast = float(self.contrast_slider.get())

            enhancer = ImageEnhancer(self.image)
            result = enhancer.enhance(brightness, contrast)

            cv2.imwrite(path, result)

    def load_image(self):
        path = filedialog.askopenfilename()

        if path:
            self.image = cv2.imread(path)
            self.update_image()

    def update_image(self, event=None):
        if self.image is None:
            return

        brightness = int(self.brightness_slider.get())
        contrast = float(self.contrast_slider.get())

        enhancer = ImageEnhancer(self.image)
        result = enhancer.enhance(brightness, contrast)

        self.display_image(self.image, self.label_before)
        self.display_image(result, self.label_after)


    def ai_enhance_image(self):
        if self.image is None:
            return

        try:
            print("*"*40)
            print("starting")
            print("*" * 40)
            enhancer = ImageEnhancer(self.image)
            result = enhancer.ai_enhance()

            self.display_image(self.image, self.label_before)
            self.display_image(result, self.label_after)
            print("*" * 40)
            print("Dooooneee")
            print("*" * 40)
        except Exception as e:
            print("AI Error:", e)
    def display_image(self, img, label):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)

        pil_img = pil_img.resize((350, 350))

        ctk_img = ctk.CTkImage(light_image=pil_img, size=(350, 350))

        label.configure(image=ctk_img)
        label.image = ctk_img


#if __name__ == "__main__":
#    app = App()
#    app.mainloop()