# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 08:32:59 2026

@author: GİZEM
"""

import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

url = "https://s1.worldcam.live:8082/aleksandrow-lodzki-dmowskiego-konstantynowska/tracks-v1/mono.ts.m3u8?token=489a3c8240949266b8dbfa750d4241e307c056703f0dcf26727c1de2f79ab134"
cap = cv2.VideoCapture(url)
# Canlı yayın gecikmesini (buffering) azaltmak için arabelleği küçült
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3) #  canlı yayınlarda gecikmeyi önlemek için kullanılan bir metod. buffer ksımını iki kare ile sınırlandırdık.
print("yayın başlıyor")

while cap.isOpened():
    ret,frame=cap.read()
    if not ret:
        print("yayına bağlanılmıyor")
        break
    result=model.track(frame,persist=True,classes=[2,3,5,7],tracker="bytetrack.yaml")
    # persist frameler arasında takip edilmek için id ataması. eğiitlmiş bir yolo kullandığımız için sınıflandırmada 2=araba , 3=motorcycle, 5 =bus, 7= kamyon 
    kutu=result[0].plot(conf=False)
    #result ile tespit edilmiş nesnelerin bir listesini döndürür.
    cv2.imshow("canlı trafic ",kutu)
    
    if cv2.waitKey(1)&0xFF==ord("q"):
        print("kapatıldı")
        break
cap.release()
cv2.destroyAllWindows()