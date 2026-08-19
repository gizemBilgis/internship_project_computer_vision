# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:41:17 2026

@author: GİZEM
"""

import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
eye_cascade=cv2.CascadeClassifier('haarcascade_eye.xml')

cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    if ret == False:
        break
    
    gri_image=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    
    # yüz tespiti
    faces=face_cascade.detectMultiScale(gri_image,scaleFactor=1.3,minNeighbors=5)
    
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y) ,(x+w,y+h),(255,0,0),2)
      
        # sadece yüzün olduğu kısmı kırp
        yarım_h=int(h/2)
        k_gri=gri_image[y:y+h,x:x+w]
        k_renkli=frame[y:y+h,x:x+w]
        
        k_gri_ust=k_gri[0:yarım_h, :]  #0 dan yarım_h a kadar
        k_renkli_ust=k_renkli[0:yarım_h, :]
        
        
        k_gri_alt = k_gri[yarım_h:h, :]
        k_renkli_alt = k_renkli[yarım_h:h, :]
        
        
        eyes=eye_cascade.detectMultiScale(k_gri_ust,scaleFactor=1.1,minNeighbors=15)
        for(eye_x,eye_y,eye_w,eye_h) in eyes:
            cv2.rectangle(k_renkli_ust,(eye_x,eye_y),(eye_x+eye_w,eye_y+eye_h), (0,0,255),thickness=2)
            
        
        smiles=smile_cascade.detectMultiScale(k_gri_alt,scaleFactor=1.8,minNeighbors=15)
        for(smile_x,smile_y,smile_w,smile_h) in smiles:
            cv2.rectangle(k_renkli_alt,(smile_x,smile_y),(smile_x+smile_w,smile_y+smile_h), (0,255,0),2)
            
    cv2.imshow("smile", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
            
            