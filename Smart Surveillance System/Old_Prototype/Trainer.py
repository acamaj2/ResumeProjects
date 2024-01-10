import cv2
import numpy as np
from PIL import Image
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()

path = "ImageDataset"


def getImageID(path):
    imagePath = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    ids = []
    for imagePaths in imagePath:
        faceImage = Image.open(imagePaths).convert('L')
        faceNP = np.array(faceImage)
        ID = (os.path.split(imagePaths)[-1].split(".")[1])
        ID = int(ID)
        faces.append(faceNP)
        ids.append(ID)
        cv2.imshow("Training", faceNP)
        cv2.waitKey(1)
    return ids, faces


IDs, faces = getImageID(path)
recognizer.train(faces, np.array(IDs))
recognizer.write("Trainer.yml")
cv2.destroyAllWindows()
print("Training Completed...")
