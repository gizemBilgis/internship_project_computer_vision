# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 08:26:29 2026

@author: GİZEM
"""

import numpy as np
import matplotlib.pyplot as plt

h, w =150 ,200
img1=np.zeros((h,w),dtype=("uint8"))
for y in range(25, h, 50):
    for x in range(25, w, 50):
        img1[y-12:y+13, x-2:x+3] = 255  
        img1[y-2:y+3, x-12:x+13] = 255 
plt.figure()
plt.imshow(img1, cmap="gray")
plt.axis('off') 
plt.show()


img2=np.zeros((h,w),dtype=("uint8"))
img2[0:h:15]=255
img2[:,0:w:15]=255
plt.figure()
plt.imshow(img2,cmap="gray")
plt.axis('off') 
plt.show()

img3=np.zeros((h,w),dtype="uint8")
for r in range(0, h + 20, 20):
    for c in range(0, w + 20, 20):
        
        if (r // 20) % 2 == 1:
            kaydirma = 10
        else:
            kaydirma = 0
        merkez_y = r
        merkez_x = c + kaydirma
        for dy in [-3, -2, -1, 0, 1, 2, 3]:
            for dx in [-3, -2, -1, 0, 1, 2, 3]:
                y = merkez_y + dy
                x = merkez_x + dx
                if y >= 0 and y < h and x >= 0 and x < w:
                    if dx**2 + dy**2 <= 9:
                        img3[y][x] = 255
plt.figure()
plt.imshow(img3,cmap="gray")
plt.axis('off') 
plt.show()