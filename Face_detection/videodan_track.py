# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 09:58:07 2026

@author: GİZEM
"""

import cv2
import datetime

def main():
    cap=cv2.VideoCapture(0)
    #video sıkıştırma formatlarını belirlemek için kullanılır.
    #XviD, tam anlamıyla bir video dosya formatı değil, büyük boyutlu video dosyalarını kaliteden çok ödün vermeden küçültmeye (sıkıştırmaya) ve açmaya yara
    fourcc=cv2.VideoWriter_fourcc(*'XVID')
    out=None
    recording=False
    record_timer = 0
    record_Buffer=50 # hareket bittikten sonra fazladan kaydedilecek kare sayısı 
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    while cap.isOpened():
        diff=cv2.absdiff(frame1, frame2)
        gray=cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
        blur=cv2.GaussianBlur(gray, ksize=(5,5), sigmaX=0)
        thresh=cv2.threshold(blur, thresh=25, maxval=255, cv2.THRESH_BINARY)
        dilated=cv2.dilate(thresh,None,iterations=3)
        # beyaz alanı genişletme
        contours=cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        