import cv2
import numpy as np
from PIL import Image, ImageTk
import os
import time
import tkinter as tk
import threading

name_list = ['',"Alex Camaj"]
def GetName():
    return name_list

def AddName(string):
    name_list.append(str(string))
    print(name_list)


def GetDimensions():
    Frame_Width = 1280
    Frame_Height = 720
    return Frame_Width,Frame_Height
def OpenCVtoGUI(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img = ImageTk.PhotoImage(image=img)
    video_label.config(image=img)
    video_label.image = img
    pass
def DataCollection():

    width, height = GetDimensions()
    camera = cv2.VideoCapture(1)

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    obj_cascade = cv2.CascadeClassifier('cascade.xml')

    id = len(GetName())-1

    count = 0
    limit = 1000

    while True:

        ret, frame = camera.read()

        grayscale_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if count != limit-1:
            width, height = GetDimensions()
            a = width / 18
            b = height / 4
            cv2.putText(frame, str("Collecting Data..."), (int(a), int(b)), cv2.FONT_ITALIC, 3, (0, 0, 255), 3)

        Detection_Obj = obj_cascade.detectMultiScale(grayscale_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in Detection_Obj:
            count += 1

            cv2.imwrite("ImageDataset/User." + str(id) + "." + str(count) + ".jpg", grayscale_img[y:y + h, x:x + w])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        OpenCVtoGUI(frame)

        k = cv2.waitKey(1)

        if count >= limit:
            break

    width, height = GetDimensions()
    x = width/18
    y = height/4
    cv2.putText(frame, str("Dataset Collection Done!"), (int(x), int(y)), cv2.FONT_ITALIC, 3, (0, 255, 0), 3)
    OpenCVtoGUI(frame)
    camera.release()
    cv2.destroyAllWindows()
    print("Dataset Collection Done!")
    pass

def Trainer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load the face dataset and labels from the 'ImageDataset' directory
    path = "ImageDataset"
    imagePath = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    ids = []
    video_path = 'Training Model.mp4'
    cap = cv2.VideoCapture(video_path)

    for imagePaths in imagePath:
        faceImage = Image.open(imagePaths).convert('L')
        faceNP = np.array(faceImage)
        ID = (os.path.split(imagePaths)[-1].split(".")[1])
        ID = int(ID)
        faces.append(faceNP)
        ids.append(ID)
        ret, frame = cap.read()
        if not ret:
            break
        OpenCVtoGUI(frame)
        cv2.waitKey(1)

    video_path = 'Complete.mp4'
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    OpenCVtoGUI(frame)

    recognizer.train(faces, np.array(ids))
    trained_model_filename = "Trainer.yml"
    recognizer.write(trained_model_filename)
    print("Training Completed...")

def SurveillanceSystem():
    width, height = GetDimensions()
    camera = cv2.VideoCapture(1)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    PrevTime = 0

    obj_cascade = cv2.CascadeClassifier('cascade.xml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("Trainer.yml")


    while True:
        ret, frame = camera.read()
        grayscale_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        Detection_Obj = obj_cascade.detectMultiScale(grayscale_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in Detection_Obj:
            serial, conf = recognizer.predict(grayscale_img[y:y + h, x:x + w])
            if conf < 63:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y - 40), (x + w, y), (0, 255, 0), -1)
                cv2.putText(frame, name_list[serial], (x, y - 10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (50, 50, 250), 2)
                cv2.putText(frame, str("Status: Safe"), (200, 200), cv2.FONT_ITALIC, 3, (0, 255, 0), 3)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y - 40), (x + w, y), (0, 0, 255), -1)
                cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (50, 50, 250), 2)
                cv2.putText(frame, str("WARNING INTRUDER DETECTED"), (100, 350), cv2.FONT_ITALIC, 3, (0, 0, 255), 1)
                cv2.putText(frame, str("Status: Unsafe"), (200, 200), cv2.FONT_ITALIC, 3, (0, 0, 255), 3)

        OpenCVtoGUI(frame)

        CurrTime = time.time()
        fps = 1 / (CurrTime - PrevTime)
        PrevTime = CurrTime

        cv2.putText(frame, "FPS: " + str(int(fps)), (70, 50), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 3, (0, 255, 0), 1)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    print("Surveillance Done!")
    pass

def start_data_collection():
    t = threading.Thread(target=DataCollection)
    t.start()

def start_training():
    t = threading.Thread(target=Trainer)
    t.start()
def start_surveillance():
    t = threading.Thread(target=SurveillanceSystem)
    t.start()

def on_button_click():
    user_input = entry.get()
    AddName(user_input)
    print("User input:", user_input)

def quit_application():
    root.quit()

root = tk.Tk()
root.title("Face Recognition GUI")

root.configure(background='lightblue')

app_title = tk.Label(root, text="Customizable Surveillance System", font=("Helvetica", 20, "bold"))
app_title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(side='left', padx=10, pady=10)
# Create a label to describe the input box (optional)
label = tk.Label(root, text="Enter Your Name:")
label.pack(pady=10)

# Create the Entry widget for text input
entry = tk.Entry(root, width=30)
entry.pack()

# Create a button to print the input when clicked
Name_button = tk.Button(root, text="Submit", command=on_button_click)
Name_button.pack(side = 'top', pady=10)

# Create a label to display the camera feed
video_label = tk.Label(root)
video_label.pack(pady=10)

# Create a button to start the surveillance system
Data_button = tk.Button(frame, text="Start Data Collection", command=start_data_collection)
Data_button.pack(side = 'top', pady=10)

Trainer_button = tk.Button(frame, text="Start Training Model", command=start_training)
Trainer_button.pack(side = 'top', pa3dy=10)

surveillance_button = tk.Button(frame, text="Start Surveillance System", command=start_surveillance)
surveillance_button.pack(side = 'top', pady=10)

quit_button = tk.Button(root, text="Quit", command=quit_application)
quit_button.pack(side = 'bottom', pady=10)

root.mainloop()

