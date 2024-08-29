import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2, PIL, numpy as np
from matplotlib import pyplot as plt

pic_path = 'data/surveys/E/blank0.jpg'
img = cv2.imread(pic_path)
img = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)

print(img.shape, pic_path)

# cv2.imshow('image1', img)
# cv2.waitKey(0)
plt.imshow(img)
# plt.show()

original_pt = np.float32([(891, 409), (833, 1931), (2077, 465), (2063, 1921)])
target_pt = np.float32([(0, 0), (0, 2268), (2000, 0), (2000, 2268)])
M = cv2.getPerspectiveTransform(original_pt, target_pt)

img1 = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
img1 = img1[:, :2000]
print(img1.shape)
# cv2.imshow('image2', img1)
# cv2.waitKey(0)
plt.imshow(img1)
# plt.show()

original_pt = np.float32([(2077, 465), (2969, 433), (3000, 1927), (2063, 1921)])
target_pt = np.float32([(0, 0), (1500, 0), (1500, 2268), (0, 2268)])
M = cv2.getPerspectiveTransform(original_pt, target_pt)

img2 = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
img2 = img2[:, :1500]
print(img2.shape)
# cv2.imshow('image3', img2)
# cv2.waitKey(0)
plt.imshow(img2)
# plt.show()

img = cv2.hconcat([img1, img2])
print(img.shape)
# cv2.imshow('image4', img)
# cv2.waitKey(0)
plt.imshow(img)
plt.show()

# img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# print(img)
se = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
bg = cv2.morphologyEx(img, cv2.MORPH_DILATE, se)
out_gray = cv2.divide(img, bg, scale=255)

print(out_gray)
print(out_gray.shape)
plt.imshow(out_gray)
plt.show()