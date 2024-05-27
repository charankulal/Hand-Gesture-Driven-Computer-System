import sys
import cv2
import time
import numpy as np
import threading
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyautogui
import screen_brightness_control as sbc
import pygetwindow as gw
import face_recognition
from face_encoding import ref_img_face_encodings, known_face_names

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
wScreen, hScreen = pyautogui.size()
pyautogui.FAILSAFE = False

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volumeRange = volume.GetVolumeRange()
minimumVolume = volumeRange[0]
maximumVolume = volumeRange[1]
area = 0

def is_powerpoint_in_focus():
    windows = gw.getAllWindows()
    for window in windows:
        if "PowerPoint" in window.title:
            if window.isActive:
                return True
    return False

def is_powerpoint_in_presentation_mode():
    windows = gw.getAllWindows()
    for window in windows:
        if "PowerPoint Slide Show" in window.title:
            return True
    return False

def process_face(frame):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(ref_img_face_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        cv2.rectangle(frame, (left, bottom-35), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name,(left+6,bottom-6),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,255,255),1)
    return frame

def process_hand(frame):
    global plocX, plocY
    img, which_hand = detector.findHands(frame)
    lmList, boundingBox = detector.findPosition(frame, handNo=0, draw=True)
    return img, which_hand, lmList, boundingBox

def adjust_audio_volume(length):
    vol = np.interp(length, [10, 150], [0, 100])
    smoothness = 5
    vol = smoothness * round(vol / smoothness)
    volume.SetMasterVolumeLevelScalar(vol / 100, None)

def adjust_brightness(length):
    brightness = np.interp(length, [10, 150], [0, 100])
    smoothness = 5
    brightness = smoothness * round(brightness / smoothness)
    sbc.set_brightness(brightness)

def main():
    global pTime
    while True:
        success, frame = cap.read()
        if not success:
            continue
        frame = cv2.flip(frame, 1)

        # Process face recognition in a separate thread
        face_thread = threading.Thread(target=process_face, args=(frame,))
        face_thread.start()

        # Process hand tracking
        img, which_hand, lmList, boundingBox = process_hand(frame)

        if which_hand == "Right" and lmList:
            [x1, y1] = lmList[8][1:]
            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255, 0, 255), 2)

            if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0:
                x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScreen))
                y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScreen))
                clocX = plocX+(x3-plocX)/smoothening
                clocY = plocY+(y3-plocY)/smoothening
                pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY

            if fingers[0] == 1 and all(f == 0 for f in fingers[1:]):
                pyautogui.hotkey('win', 'a')

            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                pyautogui.click()

            if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0:
                if fingers[4] == 1:
                    pyautogui.rightClick()

            area = (boundingBox[2]-boundingBox[0]) * (boundingBox[3]-boundingBox[1]) // 100
            if not fingers[2] and 100 < area < 1000:
                length, _, _ = detector.findDistance(4, 8, img=img)
                adjust_audio_volume(length)

        if which_hand == "Left" and lmList:
            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255, 0, 255), 2)
            if is_powerpoint_in_presentation_mode():
                if all(f == 1 for f in fingers[0:4]):
                    pyautogui.press('backspace')
                elif all(f == 1 for f in fingers[0:3]):
                    pyautogui.press('enter')
            else:
                if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1:
                    [x1, y1] = lmList[8][1:]
                    x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScreen))
                    y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScreen))
                    clocX = plocX+(x3-plocX)/smoothening
                    clocY = plocY+(y3-plocY)/smoothening
                    pyautogui.moveTo(clocX, clocY)
                    plocX, plocY = clocX, clocY
                if all(f == 1 for f in fingers[0:4]):
                    pyautogui.click()
                if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0:
                    if fingers[4] == 1:
                        pyautogui.rightClick()
                area = (boundingBox[2]-boundingBox[0]) * (boundingBox[3]-boundingBox[1]) // 100
                if not fingers[2] and 100 < area < 900:
                    length, _, _ = detector.findDistance(4, 8, img=img)
                    adjust_brightness(length)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS:{int(fps)}', (48, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
