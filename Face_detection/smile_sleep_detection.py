
import cv2
import pygame

# 1. Ses sistemini başlat ve kendi ses dosyanı yükle
pygame.mixer.init()
alarm_sesi = pygame.mixer.Sound("ses.mp3") 
alarm_caliyor = False

# 2. OpenCV'nin kendi içindeki hazır yüz ve göz bulma dosyalarını (Haar Cascades) çağır
yuz_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
goz_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

cap = cv2.VideoCapture(0)
kapali_sayac = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # İşlemi hızlandırmak için görüntüyü gri tonlamaya çevir
    gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    yuzler = yuz_cascade.detectMultiScale(gri, scaleFactor=1.3, minNeighbors=5)

    yuz_var_goz_yok = False

    for (x, y, w, h) in yuzler:
        # Yüzün etrafına mavi kare çiz
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Sadece yüzün olduğu bölgeyi kesip o bölgede göz arayacağız
        yuz_gri = gri[y:y+h, x:x+w]
        yuz_renkli = frame[y:y+h, x:x+w]
        
        # Gözleri bul
        gozler = goz_cascade.detectMultiScale(yuz_gri, scaleFactor=1.1, minNeighbors=3)
        
        
        if len(gozler) == 0:
            yuz_var_goz_yok = True
        else:
            for (ex, ey, ew, eh) in gozler:
                cv2.rectangle(yuz_renkli, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    # Uyku Kontrol Mantığı
    if yuz_var_goz_yok:
        kapali_sayac += 1
        
        # Yaklaşık 15-20 kare (kamera hızına göre yarım saniye) gözler görünmezse
        if kapali_sayac > 5:
            cv2.putText(frame, "UYARI: UYUYORSUN!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            if not alarm_caliyor:
                alarm_sesi.play(-1) # Sesi döngüye sok
                alarm_caliyor = True
    else:
       
        kapali_sayac = 0
        if alarm_caliyor:
            alarm_sesi.stop()
            alarm_caliyor = False

    cv2.imshow('Uyku Tespiti', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()