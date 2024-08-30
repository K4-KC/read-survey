import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2, PIL, numpy as np
from matplotlib import pyplot as plt

pic_path = 'data/surveys/E/254E0.jpg'
img = cv2.imread(pic_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img.shape, pic_path)

# cv2.imshow('image1', img)
# cv2.waitKey(0)
plt.imshow(img, cmap="gray")
plt.show()

original_pt_list = [[775, 456], [1050, 455], [1166, 454], [1430, 453], [1689, 444], [1938, 419], 
                    [817, 1914], [1034, 1812], [1120, 1794], [1408, 1822], [1676, 1829], [1896, 1957]]
target_pt_list = [[24, 234], [390, 234], [544, 233], [892, 234], [1240, 234], [1587, 234], 
                  [112, 2122], [386, 1996], [496, 1973], [873, 2001], [1234, 1996], [1542, 2121]]


# target_pt_list = [[int(pt[0]*zoom), int(pt[1]*zoom)] for pt in target_pt_list]
# print(target_pt_list)

# original_pt = np.float32([(891, 409), (833, 1931), (2077, 465), (2063, 1921)])
# target_pt = np.float32([(0, 0), (0, 2268), (2000, 0), (2000, 2268)])

# # first part
# original_pt = np.float32([original_pt_list[0], original_pt_list[1], original_pt_list[4], original_pt_list[5]])
# target_pt = np.float32([target_pt_list[0], target_pt_list[1], target_pt_list[4], target_pt_list[5]])
# M = cv2.getPerspectiveTransform(original_pt, target_pt)

# img1 = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
# img1 = img1[:1654, :651]
# plt.imshow(img1, cmap="gray")
# plt.show()

# original_pt = np.float32([original_pt_list[1], original_pt_list[2], original_pt_list[5], original_pt_list[6]])
# target_pt = np.float32([target_pt_list[1], target_pt_list[2], target_pt_list[5], target_pt_list[6]])
# M = cv2.getPerspectiveTransform(original_pt, target_pt)

imgs = []
for i in range(5):
    original_pt = np.float32([original_pt_list[i], original_pt_list[i+1], original_pt_list[i+6], original_pt_list[i+7]])
    target_pt = np.float32([target_pt_list[i], target_pt_list[i+1], target_pt_list[i+6], target_pt_list[i+7]])
    M = cv2.getPerspectiveTransform(original_pt, target_pt)

    imgs.append(cv2.warpPerspective(img, M, (img.shape[1], img.shape[0])))
    imgs[i] = imgs[i][:2268, 0 if i == 0 else target_pt_list[i][0]:target_pt_list[i+1][0]]
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
    bg = cv2.morphologyEx(imgs[i], cv2.MORPH_DILATE, se)
    imgs[i] = cv2.divide(imgs[i], bg, scale=255)
    plt.imshow(imgs[i], cmap="gray")
    plt.show()

img = cv2.hconcat(imgs)
plt.imshow(img, cmap="gray")
plt.show()



# img2 = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
# img2 = img2[:1430, 453:]
# plt.imshow(img2, cmap="gray")
# plt.show()

# original_pt = np.float32([(2077, 465), (2969, 433), (3000, 1927), (2063, 1921)])
# target_pt = np.float32([(0, 0), (1500, 0), (1500, 2268), (0, 2268)])
# M = cv2.getPerspectiveTransform(original_pt, target_pt)

# img2 = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
# img2 = img2[:, :1500]
# print(img2.shape)
# # cv2.imshow('image3', img2)
# # cv2.waitKey(0)
# plt.imshow(img2)
# # plt.show()

# img = cv2.hconcat([img1, img2])
# print(img.shape)
# # cv2.imshow('image4', img)
# # cv2.waitKey(0)
# plt.imshow(img)
# plt.show()

# # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# # print(img)
# se = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
# bg = cv2.morphologyEx(img, cv2.MORPH_DILATE, se)
# out_gray = cv2.divide(img, bg, scale=255)

# print(bg.shape)
# plt.imshow(img)
# plt.show()