import cv2
import numpy as np
image = cv2.imread("koyun.jpeg")

if image is not None:
    h = len(image)
    w = len(image[0])
    sonuc = image.copy()
    maske = np.zeros((h, w), dtype=np.uint8) 
    gorsel_maske = np.zeros((h, w), dtype=np.uint8)
   
    for i in range(h):
        for j in range(w):
            p_b = int(image[i][j][0])
            p_g = int(image[i][j][1])
            p_r = int(image[i][j][2])
            
            if p_g > 120 and p_r > 100 and p_b > 100:
                maske[i][j] = 1
                gorsel_maske[i,j] = 255
            elif p_g < 52 and p_r < 33 and p_b < 33:
                greenness = p_g - max(p_r, p_b)
                if greenness < 5:
                    maske[i][j] = 1
                    gorsel_maske[i,j] = 255
koyun_sayisi = 0
yonler = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

for y in range(h):
    for x in range(w):
        if maske[y][x] == 1:
            piksel_sayisi = 0
            min_y, max_y = y, y
            min_x, max_x = x, x
            
            stack = [(y, x)]
            maske[y][x] = 0 
            
            while len(stack) > 0:
                cy, cx = stack.pop()
                piksel_sayisi += 1
                
                min_y, max_y = min(min_y, cy), max(max_y, cy)
                min_x, max_x = min(min_x, cx), max(max_x, cx)
                
                for dy, dx in yonler:
                    ny, nx = cy + dy, cx + dx
                    
                    if 0 <= ny < h and 0 <= nx < w and maske[ny][nx] == 1:
                        maske[ny][nx] = 0 
                        stack.append((ny, nx))
                        
            if 12 < piksel_sayisi < 150: 
                
                box_w = (max_x - min_x) + 1
                box_h = (max_y - min_y) + 1
                kutu_alani = box_w * box_h
                
                aspect_ratio = max(box_w, box_h) / min(box_w, box_h)
                doluluk_orani = piksel_sayisi / kutu_alani
                
                center_y = min_y + (box_h / 2)
                center_x = min_x + (box_w / 2)
                
                if aspect_ratio < 2.5 and doluluk_orani > 0.45:
                    if center_y < h - 30 and center_x < w - 30:
                        
                        koyun_sayisi += 1
                        cv2.rectangle(sonuc, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2) 
cv2.imshow("Algoritmanin Gordugu Maske", gorsel_maske)      
print(f"Koyun Sayısı: {koyun_sayisi}")
cv2.imshow("Final Sonucu", sonuc)
cv2.waitKey(0)
cv2.destroyAllWindows()