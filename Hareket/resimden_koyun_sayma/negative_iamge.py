import cv2
import matplotlib.pyplot as plt

img = cv2.imread('koyun.jpeg')
h, w, _ = img.shape

greenness_degerleri = []

for y in range(h):
    for x in range(w):
        b, g, r = img[y, x]
        # Eksi değerleri de görebilmek için int'e çeviriyoruz
        fark = int(g) - max(int(r), int(b)) 
        greenness_degerleri.append(fark)

# Histogramı çizdir
plt.hist(greenness_degerleri, bins=100, range=[-50, 100], color='green')
plt.title("Yeşillik Farkı (Greenness) Histogramı")
plt.xlabel("g - max(r, b) Değeri")
plt.ylabel("Piksel Sayısı")
plt.axvline(x=15, color='red', linestyle='--', label='Şu anki Eşik (15)')
plt.legend()
plt.show()