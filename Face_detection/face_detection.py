import cv2
import matplotlib.pyplot as plt

#sınıflandırma
face_cascade= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

"""#  içe aktarma
img_1= cv2.imread("e.jpg",0)
plt.figure(),plt.imshow(img_1,cmap="gray"),plt.axis("off")


face_rectangle=face_cascade.detectMultiScale(img_1)

for(x,y,w,h ) in face_rectangle:
    cv2.rectangle(img_1,(x,y),(x+w,y+h), (255,255,255),10)
plt.figure(),plt.imshow(img_1,cmap="gray"),plt.axis("off")
"""
"""  
#  çoklu resimde bulma
img_2=cv2.imread("e2.jpg",0)
plt.figure(),plt.imshow(img_2,cmap="gray"),plt.axis("off")
 #scaleFactor: Görüntü boyutunun her görüntü ölçeğinde ne kadar küçültüleceğini belirtir.
face_rect=face_cascade.detectMultiScale(img_2,minNeighbors=7,scaleFactor=1.1) #minneig= Bir yüzün etrafında kümelenmesi gereken minimum komşu dikdörtgen sayısıdır.

for(x,y,w,h ) in face_rect:
    cv2.rectangle(img_2,(x,y),(x+w,y+h), (255,255,255),10)
plt.figure(),plt.imshow(img_2,cmap="gray"),plt.axis("off")
"""
cap=cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()
    if ret:
        face_rect=face_cascade.detectMultiScale(frame, minNeighbors=7)
        for(x,y,w,h) in face_rect:
            cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),10)
        cv2.imshow("face detect",frame) 
    if cv2.waitKey(1) & 0xFF==ord("q"): break 
    
    
cap.release()
cv2.destroyAllWindows()
        
        
