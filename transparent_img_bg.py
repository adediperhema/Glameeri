import cv2
import numpy as np

# 1. Load the image
img = cv2.imread("images/fashion_logo1.png.png")

# 2. Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 3. Create a mask targeting the background (off-white color values)
# Adjust the '240' value if needed to clean up more or less edge pixels
_, alpha = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# 4. Split the original image into its BGR channels
b, g, r = cv2.split(img)

# 5. Merge channels back together with the alpha mask as the 4th layer
rgba = [b, g, r, alpha]
dst = cv2.merge(rgba, 4)

# 6. Save the new image as a transparent PNG file
cv2.imwrite("glameeri_logo_transparent.png", dst)
print("Transparent logo saved successfully!")
