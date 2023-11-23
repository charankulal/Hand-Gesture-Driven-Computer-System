import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

cap=cv2.VideoCapture(0)
pTime=0
cTime=0
detector = htm.HandDetector()
while True:
    success, img= cap.read()
    img = detector.findHands(img=img)
    lmList=detector.findPosition(img)
    # if len(lmList)!=0:
    #     # print(lmList[4])
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    
    img=cv2.flip(img,1)
    cv2.putText(img,str(int(fps)),(10,47),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)