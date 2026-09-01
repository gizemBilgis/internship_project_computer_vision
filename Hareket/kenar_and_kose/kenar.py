# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 10:39:11 2026

@author: GİZEM
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

img1=cv2.imread("london.jpg",0)
plt.figure(), plt.imshow(img1,cmap="gray"), plt.axis("off")

medyan=np.median(img1)
print(medyan)

kenar=cv2.Canny(img1, threshold1=0, threshold2=255)
plt.figure(), plt.imshow(kenar,cmap="gray"), plt.axis("off")

low=int(max(0,(1-0.33)*medyan))
high=int(min(255,(0+0.33)*medyan))
kenar2=cv2.Canny(img1, low, high)
plt.figure(), plt.imshow(kenar2,cmap="gray"), plt.axis("off")

blur=cv2.blur(img1, ksize=(3,3))
kenar3=cv2.Canny(blur, low, high)
plt.figure(), plt.imshow(kenar3,cmap="gray"), plt.axis("off")

h,w =150,200
img2=np.zeros((h,w),dtype=("uint8"))
img2[0:h:15]=255
img2[:,0:w:15]=255
plt.figure()
plt.imshow(img2,cmap="gray")
plt.axis('off') 
plt.show()

corner=cv2.goodFeaturesToTrack(img2, maxCorners=150, qualityLevel=0.01, minDistance=10)
corner=np.int32(corner)
for i in corner:
    x, y = i.ravel()
    cv2.circle(img2, (x, y), 3, (255, 255, 255), -1)  

img_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

plt.imshow(img_rgb)
plt.title('Shi-Tomasi Corner Detection')
plt.axis('off')  
plt.show()