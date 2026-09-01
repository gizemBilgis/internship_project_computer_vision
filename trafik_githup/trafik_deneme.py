# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 09:45:10 2026

@author: GİZEM
"""

from ultralytics import YOLO

model = YOLO(r"C:\Users\Public\trafikte_sayım\runs\train\weights\best.pt")
test=r"C:/Users/GİZEM/Downloads/traffic-3849621_1280.jpg"

results = model.predict(source=test, save=True, show=True)