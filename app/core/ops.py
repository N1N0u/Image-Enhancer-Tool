import cv2
import numpy as np
import torch
from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact
from basicsr.archs.rrdbnet_arch import RRDBNet
import os


class ImageEnhancer:

    def __init__(self, image):
        self.image = image

    #Auto Adjust brightness from user interface
    def adjust_brightness(self, image, value):
        return cv2.convertScaleAbs(image, alpha=1, beta=value)

    # Auto Adjust Contrast from user interface
    def adjust_contrast(self, image, alpha):
        return cv2.convertScaleAbs(image, alpha=alpha, beta=0)

    # Auto Sharpen image using predefined Kernel
    def sharpen(self, image):
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)

    # Autoremove noise using my baby cv
    def denoise(self, image):
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    # Using AI-Enhacement using realSR
    def ai_enhance(self):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model_path = 'app/utils/realesr-general-x4v3.pth'


        from realesrgan.archs.srvgg_arch import SRVGGNetCompact

        model = SRVGGNetCompact(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_conv=32,
            upscale=4,
            act_type='prelu'
        )


        loadnet = torch.load(model_path, map_location=device)

        if 'params' in loadnet:
            model.load_state_dict(loadnet['params'])
        else:
            model.load_state_dict(loadnet)

        model.eval().to(device)

        img = self.image
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(np.transpose(img, (2, 0, 1))).unsqueeze(0).to(device)

        # inference
        with torch.no_grad():
            output = model(img_tensor)


        output = output.squeeze().cpu().numpy()
        output = np.transpose(output, (1, 2, 0))
        output = (output * 255.0).clip(0, 255).astype(np.uint8)
        output = cv2.cvtColor(output, cv2.COLOR_RGB2BGR)

        return output

    # Auto Interact with user
    def enhance(self, brightness=20, contrast=1.4):
        img = self.adjust_brightness(self.image, brightness)
        img = self.adjust_contrast(img, contrast)
        img = self.sharpen(img)
        return img