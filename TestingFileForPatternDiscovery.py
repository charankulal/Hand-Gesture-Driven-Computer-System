import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math


wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
frameR = 100
smoothening = 3.5
plocX, plocY = 0, 0
clocX, clocY = 0, 0

detector = htm.HandDetector(maxHands=1)
area = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img, which_hand = detector.findHands(img)
    # lmList, bbox = detector.findPosition(img)
    lmList, boundingBox = detector.findPosition(img, handNo=0, draw=True)

    if which_hand == "Right":
        if len(lmList) != 0:
            [x1, y1] = lmList[8][1:]
            [x2, y2] = lmList[12][1:]
            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR),
                          (wCam-frameR, hCam-frameR), (255, 0, 255), 2)
# For opened finger in right
            if fingers[1] == 1:
                cv2.putText(img, "Finger 1 UP : Right", (50, 100),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            if fingers[2] == 1:
                cv2.putText(img, "Finger 2 UP : Right", (50, 130),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            if fingers[3] == 1:
                cv2.putText(img, "Finger 3 UP : Right", (50, 160),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            if fingers[4] == 1:
                cv2.putText(img, "Finger 4 UP : Right", (50, 190),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            if fingers[0] == 1:
                cv2.putText(img, "Finger 0 UP : Right", (50, 220),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

 #  For closed finger in right
            if fingers[1] == 0:
                cv2.putText(img, "Finger 1 DOWN : Right", (50, 250),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            if fingers[2] == 0:
                cv2.putText(img, "Finger 2 DOWN : Right", (50, 280),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            if fingers[3] == 0:
                cv2.putText(img, "Finger 3 DOWN : Right", (50, 310),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            if fingers[4] == 0:
                cv2.putText(img, "Finger 4 DOWN : Right", (50, 340),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            if fingers[0] == 0:
                cv2.putText(img, "Finger 0 DOWN : Right", (50, 370),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    if which_hand == "Left":
        if len(lmList) != 0:
            [x1, y1] = lmList[8][1:]
            [x2, y2] = lmList[12][1:]
            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR),
                          (wCam-frameR, hCam-frameR), (255, 0, 255), 2)
# For opened finger in Left
            if fingers[1] == 1:
                cv2.putText(img, "Finger 1 UP : Left", (50, 100),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            if fingers[2] == 1:
                cv2.putText(img, "Finger 2 UP : Left", (50, 130),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            if fingers[3] == 1:
                cv2.putText(img, "Finger 3 UP : Left", (50, 160),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            if fingers[4] == 1:
                cv2.putText(img, "Finger 4 UP : Left", (50, 190),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            if fingers[0] == 1:
                cv2.putText(img, "Finger 0 UP : Left", (50, 220),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

 #  For closed finger in Left
            if fingers[1] == 0:
                cv2.putText(img, "Finger 1 DOWN : Left", (50, 250),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            if fingers[2] == 0:
                cv2.putText(img, "Finger 2 DOWN : Left", (50, 280),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            if fingers[3] == 0:
                cv2.putText(img, "Finger 3 DOWN : Left", (50, 310),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            if fingers[4] == 0:
                cv2.putText(img, "Finger 4 DOWN : Left", (50, 340),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

            if fingers[0] == 0:
                cv2.putText(img, "Finger 0 DOWN : Left", (50, 370),
                            cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (48, 70),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
