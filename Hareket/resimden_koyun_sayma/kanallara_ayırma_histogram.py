# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 14:04:49 2026

@author: GİZEM
"""

import cv2
import matplotlib.pyplot as plt 

image=cv2.imread("koyun.jpeg")


b = image[:, :, 0] 
g = image[:, :, 1] 
r = image[:, :, 2]

cv2.imshow("b", b)
cv2.imshow("r", r)
cv2.imshow("g", g)

# histagram

hist_b = cv2.calcHist([b], [0], None, [256], [0, 256])
hist_g = cv2.calcHist([g], [0], None, [256], [0, 256])
hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])

plt.figure(1)
plt.plot(hist_b, color='blue', label='Mavi (B) Kanalı')

plt.xlim([0, 256])
plt.legend()



plt.figure(2)
plt.plot(hist_g, color='green', label='Yeşil (G) Kanalı')
plt.xlim([0, 256])
plt.legend()

plt.figure(3)
plt.plot(hist_r, color='red', label='Kırmızı (R) Kanalı')
plt.xlim([0, 256])
plt.legend()


ters_b = 255 - b
ters_g = 255 - g
ters_r = 255 - r     

cv2.imshow("b ne",ters_b)      

plt.show()


cv2.waitKey(0)
cv2.destroyAllWindows()

