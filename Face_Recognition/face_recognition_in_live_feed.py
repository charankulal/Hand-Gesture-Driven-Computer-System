import face_recognition
import numpy as np
import cv2
from face_encoding import  ref_img_face_encodings, known_face_names

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(ref_img_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            
        
        cv2.rectangle(frame,(left, bottom-35), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name,(left+6,bottom-6),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,255,255),1)

        

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break


