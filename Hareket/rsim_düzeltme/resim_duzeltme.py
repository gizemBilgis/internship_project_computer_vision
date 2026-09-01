# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:46:32 2026

@author: GİZEM
"""
import cv2
import numpy as np

img=cv2.imread("image3.jpeg")
h, w, kanal=img.shape
yeni_image=np.zeros((h,w,3), dtype="uint8")
for y in range(1,h-1):
    for x in range(1,w-1):
        for c in range(3):
            deger=[]
            
            for dy in [-1,0,1]:
                for dx in [-1,0,1]:
                    deger.append(img[y+dy][x+dx][c])
            deger.sort()
            yeni_image[y][x][c]=deger[4]
cv2.imshow("ori", img)
cv2.imshow("yeni", yeni_image)
cv2.waitKey(0)
cv2.destroyAllWindows()