import cv2

cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

model_y="face_detection_yunet_2023mar_int8.onnx"

detector = cv2.FaceDetectorYN.create(
    model=model_y,
    config="",
    input_size=(frame_width, frame_height),
    score_threshold=0.8,  # mininmum güven skoru. bir nesneyi tespit için yüzde 80 olmalıdır.
    nms_threshold=0.3, # aynı yüze ait birden fazla kutu çizmemesi için bir flitre."Eğer ekrandaki iki çerçeve %30'dan daha fazla birbiriyle örtüşüyorsa (üst üste biniyorsa), düşük skorlu olanı sil, sadece en iyisini bırak."
    top_k=1000 
)

while True:
    ret, frame = cap.read()
    if not ret:
        break
   
    _, faces = detector.detect(frame)
    
    if faces is not None:
        for face in faces:
            x, y, w, h = face[0:4].astype(int)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)           
           
    cv2.imshow(" Yuz Tespiti", frame) 
    #yüzün beş noktasını küçük daireler ile belirtme
    if faces is not None:
        for face in faces:
          # 2. Beş Noktayı Değişkenlere Atama
            sag_goz = (int(face[4]), int(face[5]))
            sol_goz = (int(face[6]), int(face[7]))
            burun_ucu = (int(face[8]), int(face[9]))
            sag_agiz = (int(face[10]), int(face[11]))
            sol_agiz = (int(face[12]), int(face[13]))
            
            
            # metoddaki -1 parametresi aslında cv2.FILLED alamına gelir.
            cv2.circle(frame, sag_goz, 2, (0, 0, 255), -1)
            cv2.circle(frame, sol_goz, 2, (0, 0, 255), -1)
            cv2.circle(frame, burun_ucu, 2, (0, 0, 255), -1)
            cv2.circle(frame, sag_agiz, 2, (0, 0, 255), -1)
            cv2.circle(frame, sol_agiz, 2, (0, 0, 255), -1)
            cv2.imshow(" Yuz ", frame) 
    if cv2.waitKey(1) & 0xFF == ord("q"): 
        break 
 
       
cap.release()
cv2.destroyAllWindows()
