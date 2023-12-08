# HandTracking module

## Requirements

```text
mediapipe==0.10.8
numpy==1.26.2
opencv-contrib-python==4.8.1.78
opencv-python==4.8.1.78
Pillow==10.1.04
pycaw==20230407

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
    # if len(lmList)!=0:
    #     # print(lmList[4])
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

            # drawings

            # Frame rate

            

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (48, 70),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)

```