import cv2

def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def to_bgr(gray):
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def adjust_brightness(img, beta=50):
    return cv2.convertScaleAbs(img, alpha=1, beta=beta)

def adjust_contrast(img, alpha=2):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=0)

def gaussian_blur(img, k=3):
    return cv2.GaussianBlur(img, (k, k), 0)

def median_blur(img, k=5):
    return cv2.medianBlur(img, k)

def equalize(gray):
    return cv2.equalizeHist(gray)

def canny(gray, t1=100, t2=200):
    return cv2.Canny(gray, t1, t2)