import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2, PIL, numpy as np
from matplotlib import pyplot as plt

pic_path = 'data/surveys/E/blank0.jpg'
img = cv2.imread(pic_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print(img.shape, pic_path)

plt.imshow(img)
plt.show()

original_pt = np.float32([(906, 467), (2077, 514), (2057, 1915)])
target_pt = np.float32([(0, 0), (2077, 514), (2057, 1915)])
M = cv2.getPerspectiveTransform(original_pt, target_pt)

img = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))

plt.imshow(img)
plt.show()