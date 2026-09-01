# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 11:12:10 2026

@author: GİZEM
"""

import cv2
# setMouseCallback videonun üstüne bir dinleyici yerleştirir herhangi bir tıklama operasyonunu dinler. bu metod mousecallback(const string winname, mousecallback on mouse)
# fonksiyonun 5 parametresini de setMouseCallBack tarafından return olarak fırlatılır.
# flag= Fareye tıklarken klavyeden başka bir tuşa (örneğin Ctrl veya Shift) basılıp basılmadığını kontrol etmek için kullanılır.
# param=Eğer bu fonksiyona dışarıdan kendimiz özel bir veri göndermek istersek kullanılır. Genelde boş bırakılır.
def renk_bulma(event, x, y, flags,param):
    if event== cv2.EVENT_FLAG_LBUTTON: # event_flag_lbuttondown da kullanılabilir.
       print("left click")
       b,g,r =frame[y,x]
       print(f"tıklanan yerin kordinanatları :({x},{y}  | mavi={b}, yeşil={g} , kırmızı={r}")
       
cap=cv2.VideoCapture("color.mp4")
cv2.namedWindow("video ekrani")

cv2.setMouseCallback("video ekrani", renk_bulma)

while True:
    ret,frame=cap.read()
    if ret== False:
        print("video sona erdi ")
        break
    cv2.imshow("video ekrani", frame)
    if cv2.waitKey(30)& 0xFF==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()