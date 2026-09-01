# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 13:04:14 2026

@author: GİZEM
"""

from ultralytics import YOLO

model = YOLO(r"C:\Users\Public\Kedi Detection\runs\train-2\weights\best.pt")
test=r"C:\Users\GİZEM\Downloads\kedi_test.jpg"

results = model.predict(source=test, save=True, show=True)