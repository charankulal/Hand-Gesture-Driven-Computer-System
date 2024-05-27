import copy
import cv2.data
import cv2
import imutils
import numpy as np
import sys
import time
import face_recognition
from feedback import notification,msg_toast
from face_encoding import ref_img_face_encodings, known_face_names
from config import set_auth, get_auth_frame, get_root



def face_completely_visible(image):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face = faceCascade.detectMultiScale(
        cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
        scaleFactor=1.2,
        minSize=(40, 40)
    )
    for (x, y, w, h) in face:
        last_height = x + h
        last_width = y + w

        if last_height not in range(0, 480) or last_width not in range(0, 640):
            return False

    return True


def detect_blur(image, size=60):
    (h, w) = image.shape
    (cX, cY) = (int(w / 2.0), int(h / 2.0))

    fft = np.fft.fft2(image)
    fftShift = np.fft.fftshift(fft)

    fftShift[cY - size:cY + size, cX - size:cX + size] = 0
    fftShift = np.fft.ifftshift(fftShift)
    recon = np.fft.ifft2(fftShift)

    magnitude = 20 * np.log(np.abs(recon))
    mean = np.mean(magnitude)

    return mean, mean <= 10


def capture_face():
    # vs = VideoStream(src=0).start()
    # time.sleep(2.0)
    notification("Authorization", "Detecting and Recording Admin's Face")
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow("Detecting Face...", frame)
        # cv2.waitKey(2)
        face = copy.deepcopy(frame)
        frame = imutils.resize(frame, width=500)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        (mean, blurry) = detect_blur(gray, size=60)

        if not blurry:
            cv2.imwrite("Buffer.jpg",face)
            ref_img = face_recognition.load_image_file("Buffer.jpg")
            ref_img_encodings = face_recognition.face_encodings(ref_img, model="large")
            if face_completely_visible(face) and len(ref_img_encodings) == 1:
                cv2.imwrite("DP.jpg", face)
                # msg_toast(get_root,"Authorized User Created")
                time.sleep(2.0)
                break

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            # msg_toast("No authority profile created")
            break
    cap.release()
    cv2.destroyAllWindows()


def check_auth():
    print("Auth process")
    while True:
        set_auth(0)
        f = get_auth_frame()
        if f is None:
            print("No frame received")
            time.sleep(2)
        else:

            # print("Frame Processing")
            face_locations = face_recognition.face_locations(f)
            face_encodings = face_recognition.face_encodings(f, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(ref_img_face_encodings, face_encoding)
                # name = "Unknown"
                # print(matches)
                if True in matches:
                    # first_match_index = matches.index(True)
                    # name = known_face_names[first_match_index]
                    set_auth(1)
                    # print("A")
                    time.sleep(1)
                    break

            time.sleep(0.5)
