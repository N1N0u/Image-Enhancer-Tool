import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage

from processing import enhancer


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Enhancer Pro")
        self.image = None

        self.label = QLabel("No Image")

        btn_load = QPushButton("Load Image")
        btn_gray = QPushButton("Grayscale")
        btn_edge = QPushButton("Edges")

        btn_load.clicked.connect(self.load_image)
        btn_gray.clicked.connect(self.apply_gray)
        btn_edge.clicked.connect(self.apply_edges)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(btn_load)
        layout.addWidget(btn_gray)
        layout.addWidget(btn_edge)

        self.setLayout(layout)

    def load_image(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg)")
        if file:
            self.image = cv2.imread(file)
            self.display_image(self.image)

    def apply_gray(self):
        if self.image is not None:
            gray = enhancer.to_gray(self.image)
            self.display_image(gray)

    def apply_edges(self):
        if self.image is not None:
            gray = enhancer.to_gray(self.image)
            edges = enhancer.canny(gray)
            self.display_image(edges)

    def display_image(self, img):
        if len(img.shape) == 2:
            qformat = QImage.Format_Grayscale8
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            qformat = QImage.Format_RGB888

        h, w = img.shape[:2]
        bytes_per_line = 3 * w if len(img.shape) == 3 else w

        qimg = QImage(img.data, w, h, bytes_per_line, qformat)
        self.label.setPixmap(QPixmap.fromImage(qimg))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())