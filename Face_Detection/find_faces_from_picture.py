from PIL import Image, ImageDraw
import face_recognition

image = face_recognition.load_image_file("sample.jpg")
face_locations = face_recognition.face_locations(image)

print("I found {} faces in this photo".format(len(face_locations)))

pil_image = Image.fromarray(image)
draw = ImageDraw.Draw(pil_image)

for face_location in face_locations:
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top:{}, Left: {}, Bottom:{}, Right: {}".format(
        top, left, bottom, right))

    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

pil_image.show()
