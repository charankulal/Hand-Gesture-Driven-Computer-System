# Mouse actions
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui

wCam, hCam = 640, 480
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
frameR=100
smoothening=3.5
plocX,plocY=0,0
clocX,clocY=0,0


detector=htm.HandDetector(maxHands=1)
wScreen,hScreen=pyautogui.size()
pyautogui.FAILSAFE=False

while True:
    success,img=cap.read()
    img = cv2.flip(img, 1)
    img,which_hand=detector.findHands(img)
    lmList,bbox=detector.findPosition(img)
    
    if len(lmList)!=0:
        [x1,y1]=lmList[8][1:]
        [x2,y2]=lmList[12][1:]
        fingers=detector.fingersUp()
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
        
        # For hovering
        if fingers[1]==1 and fingers[2]==0:
            
            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScreen))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScreen))
            
            clocX=plocX+(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening
            
            pyautogui.moveTo(clocX,clocY)
            plocX,plocY=clocX,clocY
        
        # Left click functionality
        
        if fingers[1]==1 and fingers[2]==1:
            length,img,lineInfo=detector.findDistance(8,12,img)
            # print(length)
            if length<40:
                pyautogui.click()
        
        # Design for right click
        if fingers[1]==1 and fingers[2]==0:
            if fingers[4]==1:
                pyautogui.rightClick()
                
        
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (48, 70),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)