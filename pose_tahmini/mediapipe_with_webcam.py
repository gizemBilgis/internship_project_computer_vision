# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 09:05:09 2026

@author: GİZEM
"""

import cv2
import time

import mediapipe as mp 

mpPose=mp.solutions.pose
pose=mpPose.Pose()

mpDraw=mp.solutions.drawing_utils

cap=cv2.VideoCapture(0)


while True:
    success,frame=cap.read()
    if not success:
        break
    
    frame=cv2.flip(frame,1) # 0= x ekranı üzerinde çevirmeyi ifade eder.  1 = y ekseni etrafında döndürmeyi ifade eder.  -1= her iki ekran üzerinde çevirmeyi ifade eder
    img_rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h,w,_=frame.shape
    result=pose.process(img_rgb)
    
    roi_x_start=w//2
    roi_y_start=0
    roi_x_finish=w
    roi_y_finish=h
    cv2.rectangle(frame, (roi_x_start,roi_y_start),(roi_x_finish,roi_y_finish), (255,0,0),2)
    cv2.putText(frame, "ALARM BOLGESI", (roi_x_start + 10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    alarm_durumu=None
    
    if result.pose_landmarks:
        #mpDraw.draw_landmarks(frame,result.pose_landmarks,mpPose.POSE_CONNECTIONS)
        
        for id ,lm in enumerate(result.pose_landmarks.landmark):
            cx,cy =int(lm.x*w), int(lm.y*h)


            if id ==11:
                cv2.circle(frame, (cx,cy), 2, (0,255,0),cv2.FILLED)
                
                
            if (roi_x_start < cx < roi_x_finish) and(roi_y_start < cy < roi_y_finish):
                alarm_durumu=True
                
                
            if alarm_durumu == True:
                cv2.putText(frame, "Hırsızzzz ", (roi_x_start + 30,roi_y_start + 60 ),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255) ,2)
                
        
    cv2.imshow("img", frame)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()