import cv2

camera = cv2.VideoCapture(0)
obj_cascade = cv2.CascadeClassifier('pretrained_cascade_model.xml')
id = input("Enter Your ID:")
id = int(id)
count = 0

while True:
    ret, frame = camera.read()

    grayscale_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    Detection_Obj = obj_cascade.detectMultiScale(grayscale_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in Detection_Obj:
        count += 1
        cv2.imwrite("ImageDataset/User." + str(id) + "." + str(count) + ".jpg", grayscale_img[y:y + h, x:x + w])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)

    if count > 1000:
        break

camera.release()
cv2.destroyAllWindows()
print("Dataset Collection Done!")
