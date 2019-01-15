# -*- coding: utf-8 -*-  
import numpy as np
import cv2
import matplotlib.pyplot as plt

# 图6-1中的矩阵
img = np.array([
    [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
    [[255, 255, 0], [255, 0, 255], [0, 255, 255]],
    [[255, 255, 255], [128, 128, 128], [0, 0, 0]],
], dtype=np.uint8)

# 用matplotlib存储 红绿蓝（RGB）表示
plt.imsave('img_pyplot.jpg', img)
# 用OpenCV存储  蓝绿红（BGR）表示
cv2.imwrite('img_cv2.jpg', img)