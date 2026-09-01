# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 14:11:11 2026

@author: GİZEM
"""

import cv2
image=cv2.imread('horses.jpg',0)
cv2.imshow("ori", image)
ret,thres=cv2.threshold(image,150,255,cv2.THRESH_BINARY)
cv2.imshow("bnary_image",thres)
cv2.waitKey(0)
cv2.imwrite('image_thresh', thres)
cv2.destroyAllWindows()

