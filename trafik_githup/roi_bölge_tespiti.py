# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 09:27:40 2026

@author: GİZEM
"""

import cv2

def tiklama_olayi(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Koordinat: ({x}, {y})")

cap = cv2.VideoCapture("videoplayback.mp4")
ret, frame = cap.read()

if ret:
    
    frame = cv2.resize(frame, (1200, 720)) 
    
    cv2.imshow("Koordinat Bulucu - Tiklayin", frame)
    cv2.setMouseCallback("Koordinat Bulucu - Tiklayin", tiklama_olayi)

    print("Görüntü açıldı. Noktaları belirlemek için ekrana tıklayın.")
    print("Çıkmak için 'q' tuşuna basın.")
    
    while True:
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()
else:
    print("Video açılamadı, dosya yolunu kontrol edin.")

cap.release()