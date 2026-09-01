# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 08:24:58 2026

@author: GİZEM
"""

import cv2
import numpy as np 
from collections import defaultdict,deque
from ultralytics import YOLO


model=YOLO(r"C:\Users\Public\trafikte_sayım\runs\train\weights\best.pt")
cap=cv2.VideoCapture("videoplayback.mp4")

# roi bölge alanı
left_side_points=[(430,340),(579,350),(503,715),(4,570)]
right_side_point=[(638,347),(784,352),(1197,637),(657,704)]
left_line_points=[(313,416),(562,421)]
right_line_points=[(631,424),(888,430)]


left_count=0
right_count=0

tıklama_x,tıklama_y=-1,-1
zoomed_id=None


def mouse_click(event,x,y,flags,param):
    global tıklama_x,tıklama_y,zoomed_id
    if event==cv2.EVENT_LBUTTONDOWN:
        tıklama_x=x
        tıklama_y= y
    elif event==cv2.EVENT_RBUTTONDOWN:
        zoomed_id=None
        tıklama_x=-1
        tıklama_y=-1


def draw_roi(frame,points):
    overlay=frame.copy()
    cv2.fillPoly(overlay, [np.array(points,np.int32)],(150,0,0))
    #fillPoly ile yapılan çokgen çizimini karıştırmak için kullanılır.
    return cv2.addWeighted(overlay, 0.20, frame, beta=0.80, gamma=0)


def draw_line(frame,pts):
    cv2.line(frame,pts[0],pts[1],(0,0,255),10)
    return frame

sol_karsılık_id=set()
sag_karsılık_id=set()

def is_point_crossing_line(point,line_p1,line_p2,threshold=10):
    cx,cy=point
    x1,y1=line_p1
    x2,y2=line_p2
    
    A=y2-y1
    B=x1-x2
    C=(x2*y1)-(x1*y2)
    distance=abs(A*cx+B*cy+C)/((A*A+B*B)**0.5)
    on_segment=(min(x1,x2)-threshold <=cx<=max(x1,x2)+threshold and min(y1,y2)-threshold <= cy <= max(y1,y2)+threshold)
    return distance<=threshold and on_segment


center_history=defaultdict(lambda:deque(maxlen=5))

def get_smooth_center(track_id,new_center):
    center_history[track_id].append(new_center)
    centers=list(center_history[track_id])
    xs=[]
    
    for c in centers:
        x=c[0]
        xs.append(x)
        
    ys=[]
    
    for c in centers:
        y=c[1]
        ys.append(y)
        
    total_x=sum(xs)
    total_y=sum(ys)
    
    count=len(centers)
    
    avg_x=total_x/count
    avg_y=total_y/count
    
    smooth_x=int(avg_x)
    smooth_y=int(avg_y)
    smooth_center=(smooth_x,smooth_y)
    
    return smooth_center
    
def draw_bbox(frame,result,left_points,right_point,left_line,right_line,left_count,right_count):
    global sol_karsılık_id, sag_karsılık_id, tıklama_x,tıklama_y,zoomed_id
    zoom_kordinant=None
    current_id=[] 
    
    for r in result:
        for box in r.boxes:
            if box.id is None:
                continue
            
            track_id=int(box.id)
            current_id.append(track_id)
            x1,y1,x2,y2=map(int,box.xyxy[0])
            
            w = x2 - x1
            h = y2 - y1
            if w > 400 or h > 400:
                continue
            
            raw_center=((x1+x2)//2,(y1+y2)//2)
            center =get_smooth_center(track_id,raw_center)
            
            
            if len(center_history[track_id]) < 5:
                continue
            
            if tıklama_x != -1 and tıklama_y !=-1:
               if x1 <= tıklama_x <= x2 and y1 <= tıklama_y <= y2:
                    zoomed_id = track_id   
                    tıklama_x, tıklama_y = -1, -1
                    
            if zoomed_id == track_id:
                zoom_kordinant = (x1, y1, x2, y2)
            
            sol_alan=cv2.pointPolygonTest(np.array(left_points,np.int32),center,False)>=0
            sag_alan=cv2.pointPolygonTest(np.array(right_point,np.int32), center,False )>=0
            daire_renk=(0,255,255)
            
            if sol_alan:
                if track_id not in sol_karsılık_id:
                    if is_point_crossing_line(center,left_line[0],left_line[1]):
                        left_count+=1
                        sol_karsılık_id.add(track_id)
                        daire_renk=(255,0,255)

            elif sag_alan:
                if track_id not in sag_karsılık_id:
                    if is_point_crossing_line(center,right_line[0],right_line[1]):
                        right_count+=1 
                        sag_karsılık_id.add(track_id)
                        daire_renk=(255,0,255)
                        
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.circle(frame,raw_center,4,daire_renk,-1)
            #cv2.putText(frame,f"ID:{track_id}",(x1,y1-10),
                     #   cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
    if zoomed_id is not None and zoomed_id not in current_id:
        zoomed_id = None
        
    return frame,left_count,right_count,zoom_kordinant
 
cv2.namedWindow("counter")
cv2.setMouseCallback("counter", mouse_click)           
            
while  True:
    ret,frame=cap.read()
    if not ret:
        break
    frame=cv2.resize(frame,(1200,720))
     #tracking
    result=model.track(
        frame,
        persist=True,
        stream=True,
        conf=0.45,
        iou=0.5, # üst üste olan kutuları engeller 
        tracker="bytetrack.yaml"
        )
    #roi+lines ekranda gösterme
    frame=draw_roi(frame,left_side_points)
    frame=draw_roi(frame,right_side_point)
    frame=draw_line(frame,left_line_points)
    frame=draw_line(frame,right_line_points)
    
   
    frame,left_count,right_count,zoom_kordinant=draw_bbox( frame,result,left_side_points,right_side_point,left_line_points,right_line_points,left_count,right_count)
    
    cv2.putText(frame, f"LEFT :{left_count}",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,255,255),3)
    cv2.putText(frame, f"RIGHT :{right_count}",(900,50),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,255,255),3)
    
    if zoom_kordinant is not None:
        zx1, zy1, zx2, zy2 = zoom_kordinant
        
        # Kutunun tam dibinden kesmemek için etrafında 80 piksel pay (padding) bırakıyoruz
        pad = 80
        zy1 = max(0, zy1 - pad)
        zy2 = min(frame.shape[0], zy2 + pad)
        zx1 = max(0, zx1 - pad)
        zx2 = min(frame.shape[1], zx2 + pad)
        
        # Görüntüyü o aracın etrafından kes
        zoomed_frame = frame[zy1:zy2, zx1:zx2]
        # Kesilen küçük görüntüyü ekran boyutuna (1200x720) genişlet (Zoom Etkisi)
        zoomed_frame = cv2.resize(zoomed_frame, (1200, 720))
        
        cv2.imshow("counter", zoomed_frame)
    else:
        # Herhangi bir araca tıklanmadıysa normal ekranı göster
        cv2.imshow("counter", frame)
    
    if cv2.waitKey(1)& 0xFF==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()