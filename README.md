# HandTracking module

## Table of Contents

- [HandTracking module](#handtracking-module)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Execution of the code](#execution-of-the-code)
  - [Simple code](#simple-code)
  - [Code for volume control](#code-for-volume-control)
  - [Sample code for Mouse control](#sample-code-for-mouse-control)

## Requirements

```text
absl-py==2.0.0
asttokens==2.4.1
attrs==23.1.0
cffi==1.16.0
colorama==0.4.6
comm==0.2.0
comtypes==1.2.0
contourpy==1.2.0
cycler==0.12.1
debugpy==1.8.0
decorator==5.1.1
executing==2.0.1
flatbuffers==23.5.26
fonttools==4.45.0
ipykernel==6.27.0
ipython==8.17.2
jedi==0.19.1
jupyter_client==8.6.0
jupyter_core==5.5.0
kiwisolver==1.4.5
matplotlib==3.8.2
matplotlib-inline==0.1.6
mediapipe==0.10.8
MouseInfo==0.1.3
nest-asyncio==1.5.8
numpy==1.26.2
opencv-contrib-python==4.8.1.78
opencv-python==4.8.1.78
packaging==23.2
parso==0.8.3
Pillow==10.1.0
platformdirs==4.0.0
prompt-toolkit==3.0.41
protobuf==3.20.3
psutil==5.9.6
pure-eval==0.2.2
PyAutoGUI==0.9.54
pycaw==20230407
pycparser==2.21
PyGetWindow==0.0.9
Pygments==2.17.2
PyMsgBox==1.0.9
pyparsing==3.1.1
pyperclip==1.8.2
PyRect==0.2.0
PyScreeze==0.1.30
python-dateutil==2.8.2
pytweening==1.0.7
pywin32==306
pyzmq==25.1.1
six==1.16.0
sounddevice==0.4.6
stack-data==0.6.3
tornado==6.3.3
traitlets==5.13.0
wcwidth==0.2.12

```

## Execution of the code

Copy the requirements into `requirements.txt` and execute the following command in terminal

```bash
pip install -r requirements.txt
```

## Simple code

```python

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
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    
    img=cv2.flip(img,1)
    cv2.putText(img,str(int(fps)),(10,47),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
```

## Code for volume control

```python
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480
# boundingBox=[]
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0


detector = htm.HandDetector(maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volumeRange = volume.GetVolumeRange()
minimumVolume = volumeRange[0]
maximumVolume = volumeRange[1]
area = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flipping is needed to create mirroring
    # Find the hands
    detector.findHands(img)
    lmList, boundingBox = detector.findPosition(img, handNo=0, draw=True)
    if len(lmList) != 0:
        # Filter based on size
        area = (boundingBox[2]-boundingBox[0]) * \
            (boundingBox[3]-boundingBox[1])//100
        # print(area)
        if 100 < area < 900:

            # Find the distance btwn index and thumb
            length, img, lineInfo = detector.findDistance(4, 8, img=img)

            # Converting length to volume
            vol = np.interp(length, [10, 150], [0, 100])

            # Reduce resolution to make smoother.
            smoothness = 5
            vol = smoothness*round(vol/smoothness)

            # Check fingers which are up
            fingers=detector.fingersUp()         

            # if pinky is down then set volume
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(vol/100, None)           

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (48, 70),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

```

## Sample code for Mouse control

```python

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
smoothening=7
plocX,plocY=0,0
clocX,clocY=0,0


detector=htm.HandDetector(maxHands=1)
wScreen,hScreen=pyautogui.size()
pyautogui.FAILSAFE=False

while True:
    success,img=cap.read()
    img = cv2.flip(img, 1)
    img=detector.findHands(img)
    lmList,bbox=detector.findPosition(img)
    
    if len(lmList)!=0:
        [x1,y1]=lmList[8][1:]
        [x2,y2]=lmList[12][1:]
        fingers=detector.fingersUp()
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)
        if fingers[1]==1 and fingers[2]==0:
            
            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScreen))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScreen))
            
            clocX=plocX+(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening
            
            pyautogui.moveTo(clocX,clocY)
            plocX,plocY=clocX,clocY
        
        if fingers[1]==1 and fingers[2]==1:
            length,img,lineInfo=detector.findDistance(8,12,img)
            print(length)
            if length<40:
                pyautogui.click()
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (48, 70),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
    

```
