import os
from PIL import Image
import numpy as np
import cv2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
img_dir = os.path.join(BASE_DIR, "images")

face_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_alt2.xml")

current_id = 0
label_ids = {}
y_labels = []
x_train = []


for root, dirs, files in os.walk(img_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ", "-").lower()
            # print(path, label)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1

            id_ = label_ids[label]
            pil_image = Image.open(path).convert(
                "L"
            )  # this converts Image into grayscale
            image_array = np.array(
                pil_image, "uint8"
            )  # use uint8 because 8 bit makes 255 0-255 positive numbers
            print(id_)

            faces = face_cascade.detectMultiScale(
                image_array, scaleFactor=1.5, minNeighbors=5
            )

            for (x, y, w, h) in faces:
                roi = image_array[y : y + h, x : x + w]
                x_train.append(roi)
                y_labels.append(id_)
print(label_ids)
