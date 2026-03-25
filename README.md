🚀 AI Image Enhancement Tool (Real-ESRGAN + OpenCV)

A modern desktop application for image enhancement and super-resolution, 
combining classical computer vision techniques with GAN-based deep learning upscaling.

Built with a clean UI using CustomTkinter, this tool provides both manual controls and deep learning enhancement in one workflow.

--------------------------------------------------

✨ Features

🎛️ Manual Image Enhancement
- Brightness adjustment (real-time slider)
- Contrast control
- Sharpening filter (custom kernel)
- Noise reduction (OpenCV denoising)

🤖 AI Super-Resolution
- GAN-based super-resolution (Real-ESRGAN, x4 upscaling)
- Runs on CPU (no GPU required)

🖥️ Modern UI
- Built with CustomTkinter
- Responsive layout (controls + preview panels)
- Real-time preview updates

💾 Export Options
- Save manual enhancement
- Save AI-enhanced image (PNG for best quality)
- Save both versions at once

--------------------------------------------------

## 📸 Demo

### 📷 Testing
![Data Collection](screenshots/test.gif)


🧠 Architecture Overview

Image-Enhancer-Tool/

app/
 ├── core/
 │    └── ops.py        # Image processing logic (OpenCV + AI)
 │
 ├── ui/
 │    └── gui.py        # UI (CustomTkinter)
 │
 └── utils/
      └── (model goes here)

main.py               # Entry point
requirements.txt
README.md

This project follows a modular architecture separating UI, processing logic, and model handling to ensure scalability and maintainability.
--------------------------------------------------

⚙️ Installation

1. Clone Repository
git clone https://github.com/N1N0u/Image-Enhancer-Tool.git
cd Image-Enhancer-Tool

2. Install Dependencies
pip install -r requirements.txt

--------------------------------------------------

📥 Model Download (Required)

This project uses a pretrained model from Real-ESRGAN.

The model file is NOT included in this repository due to:
- Licensing considerations
- Best practices for clean repositories

👉 Download it from the official source:
https://github.com/xinntao/Real-ESRGAN/releases

After downloading, place it here:
app/utils/realesr-general-x4v3.pth

--------------------------------------------------

▶️ Usage

Run the application:

python main.py

Workflow:
1. Load an image
2. Adjust brightness/contrast
3. Click "AI Enhance"
4. Save results

--------------------------------------------------

🧪 Technologies Used

- Python
- OpenCV
- PyTorch
- Real-ESRGAN
- CustomTkinter
- NumPy
- Pillow (PIL)

--------------------------------------------------

💻 Development Environment

This project was developed and tested on low-end hardware:

- CPU: Intel Core 2 Quad Q8300 @ 2.5GHz
- RAM: 4GB
- GPU: None (CPU-only, no VRAM)

⚙️ Optimization Approach

- Efficient OpenCV pipelines for real-time processing
- Lightweight AI model (SRVGGNetCompact)
- CPU-compatible PyTorch inference
- Memory-conscious image handling

Despite limitations, the system supports:
- Real-time manual enhancement
- AI-based super-resolution on CPU

Note:
AI enhancement is slower on CPU and may take several seconds per image.

--------------------------------------------------

🚀 Performance Insight

- Manual enhancements: near-instant
- AI enhancement (CPU): ~5–20 seconds depending on image size

Future optimization ideas:
- Model quantization (INT8)
- ONNX optimization
- Background threading (avoid UI freeze)

--------------------------------------------------

🚧 Future Improvements

- Add multithreading (non-blocking UI)
- Batch image processing
- Drag & drop support
- Multiple AI models (x2, x4, anime, etc.)
- Export quality settings
- Convert to standalone .exe

--------------------------------------------------

📌 Key Highlights (For Recruiters)

- Combines classical computer vision + deep learning
- Clean architecture (UI separated from processing)
- Runs on low-spec hardware (CPU-only)
- Real-world usable application
- Demonstrates PyTorch model loading and inference

--------------------------------------------------

📄 License

MIT License

--------------------------------------------------

🙏 Acknowledgements

- Real-ESRGAN by xinntao (used for super-resolution model)
- Open-source contributors in computer vision and deep learning

--------------------------------------------------

👨‍💻 Author

ATEF Aliat

Passionate about AI, Computer Vision, and Software Engineering.
Focused on building real-world tools combining ML + UI.

--------------------------------------------------
