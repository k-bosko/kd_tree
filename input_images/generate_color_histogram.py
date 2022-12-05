import cv2
import matplotlib.pyplot as plt
import os

# load image
filename = 'color_wheel_square.png'
img = cv2.imread(f'./input_images/{filename}')

# Get RGB data from image
# cv2.calchist([imageObject], [channelValue], mask, [histSize], [low,high])
blue_color = cv2.calcHist([img], [0], None, [255], [0, 255])
red_color = cv2.calcHist([img], [1], None, [255], [0, 255])
green_color = cv2.calcHist([img], [2], None, [255], [0, 255])

# # Separate Histograms for each color
plt.subplot(3, 1, 1)
plt.title("histogram of Blue")
plt.plot(blue_color, color="b")

plt.subplot(3, 1, 2)
plt.title("histogram of Green")
plt.plot(green_color, color="g")

plt.subplot(3, 1, 3)
plt.title("histogram of Red")
plt.plot(red_color, color="r")

plt.tight_layout()
# plt.show()
filebase, ext = filename.split(".")
if not os.path.exists("./input_images/hist"):
    os.mkdir("./input_images/hist")

plt.savefig(f'./input_images/hist/{filebase}_hist.{ext}')
