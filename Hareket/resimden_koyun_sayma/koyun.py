import cv2
import numpy as np

image = cv2.imread("koyun.jpeg")

if image is not None:
    h, w = image.shape[:2]
    sonuc = image.copy()
    
    # NumPy ile maske oluşturma
    maske = np.zeros((h, w), dtype=np.uint8)
    gorsel_maske = np.zeros((h, w), dtype=np.uint8)
    
    # 1. ADIM: YENİ MASKELEME (B < 40 Kuralı)
    for y in range(h):
        for x in range(w):
            b = int(image[y, x, 0]) # Sadece Blue (Mavi) kanalını almamız yetiyor
            
            # Sadece B < 40 kuralını uyguluyoruz
            if b < 40:
                maske[y, x] = 1
                gorsel_maske[y, x] = 255

    cv2.imshow("B < 40 Maskesi", gorsel_maske)

    # 2. ADIM: BİZİM DFS VE GEOMETRİ FİLTRELERİMİZ
    koyun_sayisi = 0
    yonler = [(dy, dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if (dy, dx) != (0, 0)]

    for y in range(h):
        for x in range(w):
            if maske[y, x] == 1:
                stack = [(y, x)]
                maske[y, x] = 0
                
                min_y, max_y, min_x, max_x = y, y, x, x
                alan = 0
                
                while stack:
                    cy, cx = stack.pop()
                    alan += 1
                    
                    min_y, max_y = min(min_y, cy), max(max_y, cy)
                    min_x, max_x = min(min_x, cx), max(max_x, cx)
                    
                    for dy, dx in yonler:
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and maske[ny, nx] == 1:
                            maske[ny, nx] = 0 
                            stack.append((ny, nx))
                            
                # 3. ADIM: BİZİM HASSAS FİLTRELERİMİZ
                # Gölgeler büyük çıkacağı için aralığı eski koddaki gibi 110-200'e çekelim
                if 110 <= alan <= 200:
                    box_w, box_h = (max_x - min_x) + 1, (max_y - min_y) + 1
                    
                    aspect_ratio = max(box_w, box_h) / min(box_w, box_h)
                    doluluk = alan / (box_w * box_h)
                    center_y, center_x = min_y + (box_h / 2), min_x + (box_w / 2)
                    
                    # BİZİM KURAL: Oran düzgün mü ve içi dolu mu?
                    if aspect_ratio < 2.5 and doluluk > 0.45 and center_y < h - 30 and center_x < w - 30:
                        koyun_sayisi += 1
                        cv2.rectangle(sonuc, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2) 

    print(f"Ekranda Tespit Edilen Koyun Sayısı: {koyun_sayisi}")
    cv2.imshow("Final Sonucu", sonuc)
    cv2.waitKey(0)
    cv2.destroyAllWindows()