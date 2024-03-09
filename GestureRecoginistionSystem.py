# Mouse actions
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui
import screen_brightness_control as sbc

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
frameR = 100
smoothening = 3.5
plocX, plocY = 0, 0
clocX, clocY = 0, 0


# maxHands parameter specifies that the detector should track a maximum of 1 hand in the video feed.

detector = htm.HandDetector(maxHands=1)

# `wScreen, hScreen = pyautogui.size()` retrieves the screen resolution width and height using the `pyautogui.size()` function 
# and assigns them to the variables `wScreen` and `hScreen` respectively. This information is useful for mapping 
# the hand movements on the camera feed to the corresponding positions on the screen.

# declarations related to mouse control functionalities
wScreen, hScreen = pyautogui.size()
pyautogui.FAILSAFE = False

# This block of code is related to controlling the system's audio volume using the `pycaw` library.

# declarations related to volume control functionality
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volumeRange = volume.GetVolumeRange()
minimumVolume = volumeRange[0]
maximumVolume = volumeRange[1]
area = 0

# Infinite loop to accept input live from the cam feed using opencv

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img, which_hand = detector.findHands(img)
    # lmList, bbox = detector.findPosition(img)
    lmList, boundingBox = detector.findPosition(img, handNo=0, draw=True)

    if which_hand=="Right":
        if len(lmList) != 0:
            [x1, y1] = lmList[8][1:]
            [x2, y2] = lmList[12][1:]
            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR),
                        (wCam-frameR, hCam-frameR), (255, 0, 255), 2)

            # For hovering or pointer movement
            if fingers[1] == 1 and fingers[2] == 0 and fingers[0]==0:

                x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScreen))
                y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScreen))

                clocX = plocX+(x3-plocX)/smoothening
                clocY = plocY+(y3-plocY)/smoothening

                pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY

            # Left click functionality

            if fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = detector.findDistance(8, 12, img)
                # print(length)
                if length < 40:
                    pyautogui.click()

            # Right click functionality
            if fingers[1] == 1 and fingers[2] == 0:
                if fingers[4] == 1:
                    pyautogui.rightClick()
                    
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
