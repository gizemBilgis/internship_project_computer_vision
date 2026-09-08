import cv2
from ultralytics import YOLO
import winsound

THRESHOLD = 0.3

model = YOLO('yolo11n-pose.pt')

cap = cv2.VideoCapture(0)

cv2.namedWindow("Hirsizlik Tespiti Uygulama", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Hirsizlik Tespiti Uygulama", 1280, 720)

kisi_gecmis_taraf = {}
kisi_ilk_taraf = {}
hirsiz_id_seti = set()
alarm_caliyor = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    results = model.track(frame, persist=True, verbose=False)
    
    frame = results[0].plot()
    
    cv2.line(frame, (360, 0), (360, h), (0, 255, 0), 2)
    cv2.putText(frame, "SATICI", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, "MUSTERI", (380, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    
    satici_var = False
    anlik_hirsiz_satici_tarafinda = False
    anlik_basit_ihlal = False
    
    if results[0].boxes is not None and results[0].boxes.id is not None:
        ham_id_verisi = results[0].boxes.id.cpu()
        track_ids = ham_id_verisi.int().tolist()
        
        ham_eklem_koordinatlari = results[0].keypoints.xy.cpu()
        keypoints = ham_eklem_koordinatlari.numpy()
        
        ham_guven_skorlari = results[0].keypoints.conf.cpu()
        confs = ham_guven_skorlari.numpy()
        
        
        
        for i, track_id in enumerate(track_ids):
            eklem_noktası = keypoints[i]
            conf = confs[i]
            
            gecerli_x_kordinatlari = [
                k[0] for j, k in enumerate(eklem_noktası) 
                if conf[j] > THRESHOLD and k[0] > 0
            ]
            
            if not gecerli_x_kordinatlari:
                continue
                
            agirlik_merkezi_x = sum(gecerli_x_kordinatlari) / len(gecerli_x_kordinatlari)
          
            if agirlik_merkezi_x < 360:
                aktif_taraf="SATICI"
            else:
                aktif_taraf="ALICI"

            if track_id not in kisi_ilk_taraf:
                kisi_ilk_taraf[track_id] = aktif_taraf
                
            if track_id in kisi_gecmis_taraf:
                onceki_taraf = kisi_gecmis_taraf[track_id]
                if onceki_taraf == "ALICI" and aktif_taraf == "SATICI":
                    ilk_ciktigi_yer = kisi_ilk_taraf[track_id]
                    if ilk_ciktigi_yer == "ALICI":
                        hirsiz_id_seti.add(track_id)
                        
                    elif ilk_ciktigi_yer == "SATICI":
                        pass
            
            kisi_gecmis_taraf[track_id] = aktif_taraf
            
            if aktif_taraf == "SATICI" and track_id not in hirsiz_id_seti:
                satici_var = True
                
            if track_id in hirsiz_id_seti and aktif_taraf == "SATICI":
                anlik_hirsiz_satici_tarafinda = True
                
            sag_bilek_x = eklem_noktası[10][0]
            sag_bilek_y = eklem_noktası[10][1]
            sag_bilek_conf = conf[10]
            
            if aktif_taraf == "ALICI" and sag_bilek_conf > THRESHOLD and sag_bilek_x > 0:
                cv2.circle(frame, (int(sag_bilek_x), int(sag_bilek_y)), 10, (255, 0, 0), -1)
                
                if sag_bilek_x < 360:
                    if kisi_ilk_taraf.get(track_id) == "ALICI":
                        anlik_basit_ihlal = True

    guncel_alarm_durumu = False
    
    if anlik_hirsiz_satici_tarafinda:
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (360, h), (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        cv2.putText(frame, "HIRSIZ SATICI BOLGESINDE!!!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        guncel_alarm_durumu = True
        
    elif not satici_var and anlik_basit_ihlal:
        cv2.putText(frame, "Dikkat: Hirsizlik Tespit Edildi!!!", (360 + 10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        guncel_alarm_durumu = True
        
    if guncel_alarm_durumu and not alarm_caliyor:
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
        alarm_caliyor = True
    elif not guncel_alarm_durumu and alarm_caliyor:
        winsound.PlaySound(None, winsound.SND_PURGE)
        alarm_caliyor = False

    cv2.imshow("Hirsizlik Tespiti Uygulama", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if alarm_caliyor:
    winsound.PlaySound(None, winsound.SND_PURGE)