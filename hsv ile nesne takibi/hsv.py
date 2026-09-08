# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 10:52:18 2026

@author: GİZEM
"""

import cv2
import numpy as np

def nothing (x):
    pass

def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = hsv[y, x]
        print(f" - H: {pixel[0]}, S: {pixel[1]}, V: {pixel[2]}")

# cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap = cv2.VideoCapture("renkli_toplar.mp4")
cv2.namedWindow("Trackbars")
cv2.namedWindow("frame")
cv2.setMouseCallback("frame", get_hsv_value)

cv2.createTrackbar("LH", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("LS", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("LV", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("UH", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("US", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("UV", "Trackbars", 255, 255, nothing)
is_paused = False

while True:
    # Eğer video duraklatılmamışsa yeni kare oku
    if not is_paused:
        success, frame = cap.read()
        
        if not success or frame is None:
            print("Video bitti.")
            break
        frame = cv2.resize(frame, (800, 600))
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    l_h=cv2.getTrackbarPos("LH", "Trackbars") 
    l_s=cv2.getTrackbarPos("LS", "Trackbars")
    l_v=cv2.getTrackbarPos("LV", "Trackbars")
    u_h=cv2.getTrackbarPos("UH", "Trackbars")
    u_s=cv2.getTrackbarPos("US", "Trackbars")
    u_v=cv2.getTrackbarPos("UV", "Trackbars")
    
    
    lower_blue=np.array([l_h,l_s,l_v])
    upper_blue=np.array([u_h,u_s,u_v])
    mask=cv2.inRange(hsv, lower_blue, upper_blue)
    
    result =cv2.bitwise_and(frame,frame, mask=mask)
    
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("result",result)
    
    key= cv2.waitKey(60)& 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):
        cv2.waitKey(-1)
cap.release()
cv2.destroyAllWindows()