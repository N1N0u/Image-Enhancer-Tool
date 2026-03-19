import cv2
from processing import enhacer

img = cv2.imread("testImages/1.jpg")

if img is None:
    print("Error loading image")
    exit()

# processing
gray = enhacer.to_gray(img)

bright = enhacer.adjust_brightness(img)
contrast = enhacer.adjust_contrast(img)

blur = enhacer.gaussian_blur(img)
median = enhacer.median_blur(img)

eq = enhacer.equalize(gray)
edges = enhacer.canny(gray)

# display
cv2.imshow("Original", img)
cv2.imshow("Gray", gray)
cv2.imshow("Edges", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()