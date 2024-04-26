from PIL import Image, ImageDraw
import face_recognition

charan = face_recognition.load_image_file("DP.jpg")
charan_face_encodings = face_recognition.face_encodings(charan)

known_face_encodings = [
    charan
]

known_face_names = [
    "Charan"
]


image = face_recognition.load_image_file("sample.jpg")
face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image, face_locations)


pil_image = Image.fromarray(image)
draw = ImageDraw.Draw(pil_image)

for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces(
        charan_face_encodings, face_encoding)
    name = "Unknown"

    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
    text_width, text_height = 50,10
    draw.rectangle(((left, bottom-text_height-10), (right, bottom)),
                   fill=(0, 0, 255), outline=(0, 0, 255))

    draw.text((left+6, bottom-text_height-5), name, fill=(255, 255, 255, 255))
    
del draw
pil_image.show()
