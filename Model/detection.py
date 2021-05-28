# Face Detection

from mtcnn import MTCNN
import cv2
import numpy as np

# Face Detection DNN Model
model_name='./Model/weights/res10_300x300_ssd_iter_140000.caffemodel'
prototxt_name='./Model/weights/deploy.prototxt.txt'

def detectMTCNN(frame):
    '''
    args discription
    frame : frame to detect faces
    '''

    detector = MTCNN()
    detect = detector.detect_faces(frame)

    if len(detect) > 0: 
        print(detect[0]['box'])
        print(detect[0]['confidence'])
        print(detect[0]['keypoints'])

    cv2.imshow('gg', frame)

def detectSSD(frame):
    '''
    args discription
    frame : frame to detect faces
    '''
    model=cv2.dnn.readNetFromCaffe(prototxt_name,model_name) # read face detection model made by caffe
    blob=cv2.dnn.blobFromImage(cv2.resize(frame,(300,300)),1.0, (300,300),(104.0,177.0,123.0)) # Convert Frame data to Blob data 
    model.setInput(blob) # model setting
    detections=model.forward() #predict 200 boxes for one frame

    faces = [] # faces box to send on face recognition model

    # action for all of data
    for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2] # get confidence for each predict data
            threshold=0.65 # set threshold for filter out Garbage data

            if confidence > threshold:
                    # calculate face positions for predict data * frame size
                    # because predict data was normalized data so we have to multiply by frame size
                    box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])

                    (startX, startY, endX, endY) = box.astype("int")
                    
                    # check position value if position is out of frame then put it on frame size
                    if startX < 0:
                        startX = 0
                    elif endX > width:
                        endX = width

                    if startY < 0:
                        startY = 0
                    elif endY > height:
                        endY = height
                    

                    faces.append((startX, startY, endX, endY))

                    # Draw infos in Frame==================================================================    
                    print("{:.2f}%".format(confidence * 100), startX, startY, endX, endY)

                    text = "{:.2f}%".format(confidence * 100)

                    y = startY - 10 if startY - 10 > 10 else startY + 10

                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                    #======================================================================================


cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

while True:
    retval, frame = cap.read()
    if not retval:
        break   
    frame = cv2.flip(frame, 1)   
    #detectSSD(frame)
    detectMTCNN(frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
        
cap.release()
cv2.destroyAllWindows()



