# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 17:17:21 2026

@author: GİZEM
"""

import cv2
import glob
import os 
import numpy as np

kaynak="Data"
hedef="noise_img"

def gaussianNoise (image):
    row,col,ch=image.shape
    mean=0
    var=0.05
    sigma=var**0.5
    # sigma (standart sapma): Gürültünün ne kadar şiddetli olacağını belirler.Değer arttıkça gürültü artar.
    gauss=np.random.normal(mean,sigma,(row,col,ch))
    # np.random.normal: Gauss dağılımına (çan eğrisi) uygun rastgele sayılar üretir.
    # Bu matrisin boyutu resimle aynı olmalıdır (row, col, ch).
    noise=image+gauss
    noise = np.clip(noise, 0, 1)
    return noise

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
        noise=saltPepperNoise(resim) 
        noise_dosya_adi=os.path.join(hedef,f"noise_{dosya_adi}")
        cv2.imwrite(noise_dosya_adi,noise)
        