# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 13:31:26 2026

@author: GİZEM
"""

import cv2

video=cv2.VideoCapture(0)

def renk_bulma(event, x, y, flags,param):
    if event== cv2.EVENT_FLAG_LBUTTON: # event_flag_lbuttondown da kullanılabilir.
       print("left click")
       b,g,r =frame[y,x]
       print(f"tıklanan yerin kordinanatları :({x},{y}  | mavi={b}, yeşil={g} , kırmızı={r}")
       if b> g : 
          if b>r:
              print("bu nokta mavi alt tonlu")
       
       elif r>g:
         if r >b :
             print("kırmızı alt tonlu ")
       elif g>r:
           if g>b :
               print("yeşil alt tonlu ")
        
       else: print("noktaların kamrşık")         
        
cv2.namedWindow("video ekranı")       
cv2.setMouseCallback("video ekranı", renk_bulma)

while True:
    ret, frame=video.read()
    if ret == False:
        break
    
    cv2.imshow("video ekranı", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()  