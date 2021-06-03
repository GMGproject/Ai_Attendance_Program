from detection import detectSSD, detectMTCNN
from recognition import getFaceEncoding
from model import predict, train
from utils import checkFaceSize, chanegeAttendance
import cv2

print("Training KNN classifier...")
classifier = train("./Model/train", model_save_path="./Model/weights/trained_knn_model.clf", n_neighbors=2)
print("Training complete!")

cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

faceSize = 200
resultCheckSize = 10
resultList = []

while True:
    retval, frame = cap.read()
    if not retval:
        break   
    frame = cv2.flip(frame, 1)   
    
    faces = detectSSD(width, height, frame)

    passCheck, passFaces = checkFaceSize(faces, size=faceSize)

    if passCheck:
        predictions = predict(frame, passFaces, model_path="./Model/weights/trained_knn_model.clf")
        for name, (top, right, bottom, left) in predictions:
            resultList.append(name)
            print("- Found {} at ({}, {})".format(name, left, top))
            frame = cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
            cv2.putText(frame, name, (left, top - 5), cv2.FONT_HERSHEY_DUPLEX, 2,(0,0,255), 2, cv2.LINE_AA)

        print("OK")

        if len(resultList) == resultCheckSize:
            chanegeAttendance(resultList)
            resultList.clear()

    
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
        
cap.release()
cv2.destroyAllWindows()