import face_recognition

ref_img = face_recognition.load_image_file("DP.jpg")
ref_img_face_encodings = face_recognition.face_encodings(ref_img, model="large")

known_face_encodings = [
    ref_img_face_encodings
]

known_face_names = [
    "Admin"
]