import cv2
import numpy as np

# 1. Load your original BGR image
img = cv2.imread("fashion_logo1.jpg")

# 2. Split the image into its separate Blue, Green, and Red channels
b_channel, g_channel, r_channel = cv2.split(img)

# 3. Create a grayscale conversion (for contrast/luminance reference if needed)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 4. Create an Alpha channel (fully opaque) for your RGBA merge
alpha_channel = np.ones(r_channel.shape, dtype=r_channel.dtype) * 255

# 5. Merge channels back into a 4-channel RGBA image focused on Red
# Standard order for OpenCV's RGBA format is (Red, Green, Blue, Alpha)
rgba_red_only = cv2.merge([r_channel, g_channel, b_channel, alpha_channel])

# ALTERNATIVE: If you want a visual image that looks entirely red
# Replace Blue and Green channels with zeros
zeros = np.zeros_like(r_channel)
visual_red_img = cv2.merge([zeros, zeros, r_channel])

# Save the outputs
cv2.imwrite("extracted_red_channel.png", rgba_red_only)
cv2.imwrite("visual_red.jpg", visual_red_img)
