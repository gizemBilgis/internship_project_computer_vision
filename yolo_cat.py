# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 14:31:03 2026

@author: GİZEM
"""

from ultralytics import YOLO

if __name__ == '__main__':
    model=YOLO('yolo11n.pt')
    result = model.train(
    data=r"C:\Users\Public\Kedi Detection\cat\data.yaml", 
    epochs=100, 
    plots=True, 
    imgsz=640, 
    device=0,
    project=r"C:\Users\Public\Kedi Detection\runs"
)

