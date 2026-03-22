import cv2
import numpy as np
from realesrgan import RealESRGANer
from PIL import Image
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet

class ImageEnhancer:

    def __init__(self, image):
        self.image = image

    def adjust_brightness(self, image, value):
        return cv2.convertScaleAbs(image, alpha=1, beta=value)

    def adjust_contrast(self, image, alpha):
        return cv2.convertScaleAbs(image, alpha=alpha, beta=0)

    def sharpen(self, image):
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)


    def denoise(self, image):
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    def ai_enhance(self):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # 🔥 مهم جدًا: تعريف model architecture
        model = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=23,
            num_grow_ch=32,
            scale=4
        )

        upsampler = RealESRGANer(
            scale=4,
            model_path='app/utils/realesr-general-x4v3.pth',
            model=model,
            device=device
        )

        img = self.image

        output, _ = upsampler.enhance(img)

        return

    def enhance(self, brightness=20, contrast=1.4):
        img = self.adjust_brightness(self.image, brightness)
        img = self.adjust_contrast(img, contrast)
        img = self.sharpen(img)
        return img