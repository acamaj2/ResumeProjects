from roboflow import Roboflow
import cv2
from ultralytics import YOLO
import time
from pyfirmata import Arduino, SERVO
import Arduino

# Load Model Details
model = YOLO("C:\\Users\\alexm\\Downloads\\best.pt")
model.to('cuda')
names = model.names

# Open a connection to the webcam
cap = cv2.VideoCapture(0)
Arduino.Start()


# Set inital variables
verify = 0
threshold_high = 0.9
threshold_low = 0.5
confidence = 0
limit = 100
status = 0
Locked = True

# Setting up variables for FPS
prev_frame = 0
new_frame = 0

# Create a display window (720p)
window_name = 'Webcam'
window_width = 1280
window_height = 720
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL) 
cv2.resizeWindow(window_name, 1280, 720)

# Creating inference on each frame
while cap.isOpened():
    ret, frame = cap.read()    #Reading in one frame at a time
    if not ret:
        break

    
    frame = cv2.resize(frame, (window_width, window_height)) # Resize frame to fit display window
    new_frame = time.time()
    print(status)
    if verify >= limit:    # Check to see if face has been verified

        if (status == 0):
            Arduino.Unlock()
            print("ran")

        cv2.putText(frame, f"Welcome {Name_Detection}", (250, 250), cv2.FONT_HERSHEY_TRIPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
        status += 1

        if (status == 150):
            Arduino.Lock()
            verify = 0
            status = 0

    else:
        data = model.predict(frame)   # Perform prediction using YOLOv8 Model
       

        # Fetching necessary results from prediction
        for result in data:                                                 # iterate results
            boxes = result.boxes.cpu().numpy()                              # Get the boxes object with information for frame annotation
                                   
            for box in boxes:                                               # iterate boxes
                key_points  = box.xyxy[0].astype(int)                       # Get corner points as int
                Name_Detection = names[int(box.cls[0])]                     # Save 
                confidence = box.conf 
                
                if (confidence >= threshold_high):
                    cv2.rectangle(frame, key_points[:2], key_points[2:], (0, 255, 0), 2)
                    cv2.putText(frame, f"{Name_Detection}: Verifying({verify}/100)", (key_points[0], key_points[1]),
                                        cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2)
                    verify += 1

                elif (confidence < threshold_high and confidence >= threshold_low):
                    cv2.rectangle(frame, key_points[:2], key_points[2:], (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown Person", (key_points[0], key_points[1]),
                                        cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
                    verify = 0

                else: 
                    verify = 0
            
    fps = 1/(new_frame-prev_frame)
    prev_frame = new_frame
    fps = int(fps)
    cv2.putText(frame, f"FPS:{round(fps,0)}", (7, 70), cv2.FONT_HERSHEY_TRIPLEX, 2, (100, 255, 0), 3, cv2.LINE_AA)

    cv2.imshow('Webcam',frame)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  

cap.release()
cv2.destroyAllWindows()


#SMART SURVEILANCE