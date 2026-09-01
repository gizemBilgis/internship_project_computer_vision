# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 15:36:22 2026

@author: GİZEM
"""

import cv2
import glob
import os
import numpy as np

kaynak="Data"
hedef="augmented_data"



def saltPepperNoise(image):
    row,col,ch=image.shape
    s_p=0.5
    amount=0.04
   # amount: Resmin yüzde kaçının gürültüyle kaplanacağını belirler.
    noisy=np.copy(image)
    
    #beyaz gürültü sayısı
    num_salt=np.ceil(amount*image.size*s_p)
    cordinant=[np.random.randint(0,i-1,int(num_salt)) for i in image.shape]
    noisy[tuple(cordinant)] = 255
    
    num_pepper=np.ceil(amount*image.size*(1-s_p))
    cordinant=[np.random.randint(0,i-1,int(num_pepper)) for i in image.shape]
    noisy[tuple(cordinant)] =0
    
    return noisy

if not os.path.exists(hedef):
    os.makedirs(hedef)
    
resim_url=('*.jpg','*.jpeg','*.png')
resim_list=[]
for url in resim_url:
    resim_list.extend(glob.glob(os.path.join(kaynak,url)))

for dosya_yolu in resim_list:
    dosya_adi=os.path.basename(dosya_yolu)
    resim=cv2.imread(dosya_yolu)
    
    if resim is not None:
        blur=cv2.GaussianBlur(resim, ksize=(15,15), sigmaX=0)
        cv2.imwrite(os.path.join(hedef,f"blur_{dosya_adi}"),blur)
        
        noise=saltPepperNoise(resim)
        cv2.imwrite(os.path.join(hedef,f"noise_{dosya_adi}"),noise)
        
        y_flip=cv2.flip(resim,0)# (0: dikey, 1: yatay, -1: hem dikey hem yatay)
        cv2.imwrite(os.path.join(hedef,f"yflip_{dosya_adi}"),y_flip)
        
        # alpha:kontrast çarpanı (1 =değişmez), beta parlaklık eklmesei
        brigness=cv2.convertScaleAbs(resim,alpha=1,beta=50)
        cv2.imwrite(os.path.join(hedef,f"brigness_{dosya_adi}"),brigness)
        
        h,w=resim.shape[:2]
        merkez=(w//2,h//2)
        acilar = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300]
        for aci in acilar:
           dondurme_matrisi=cv2.getRotationMatrix2D(merkez, angle=aci, scale=1) 
           rotated=cv2.warpAffine(resim,dondurme_matrisi, (w,h))
           cv2.imwrite(os.path.join(hedef,f"rotated_{dosya_adi}"),rotated)

        
        
    else:
        print(f"Hata: {dosya_adi} dosyası OpenCV ile okunamadı!")

