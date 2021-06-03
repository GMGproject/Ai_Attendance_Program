# Face Detection
#from mtcnn import MTCNN
import cv2
import numpy as np

# Face Detection DNN Model
model_name='./Server/Model/weights/res10_300x300_ssd_iter_140000.caffemodel'
prototxt_name='./Server/Model/weights/deploy.prototxt.txt'

def detectMTCNN(frame):
    pass
"""
    '''
    args discription
    frame : frame to detect faces
    '''

    detector = MTCNN()
    faces = detector.detect_faces(frame)
    _faces = [] # list for return faces position

    '''
    detect_faces value : box -> array | confidence -> float | keypoints -> dictionary
    box : box positions (start x, start y, end x, end y)
    confidence : predict confidence
    keypoints : facial keypoints (5 points [left eye, right eye, nose, left mouth, right mouth])

    detect[faces]{'box' : [startX, startY, endX, endY], 
                  'confidnece' : confidence, 
                  'keypoints' : {'left eye'    : (x, y)
                                 'right eye'   : (x, y)
                                 'nose'        : (x, y)
                                 'left mouth'  : (x, y)
                                 'right mouth' : (x, y)}}
    '''

    for face in faces:
        _faces.append(face['box'])

    print(_faces)
    cv2.imshow('frame', frame)
"""


def detectSSD(frame):
    '''
    args discription
    frame : frame to detect faces

    return
    faces : detected faces list from frame 
    '''
    try:
        model=cv2.dnn.readNetFromCaffe(prototxt_name,model_name) # read face detection model made by caffe
        blob=cv2.dnn.blobFromImage(cv2.resize(frame,(300,300)),1.0, (300,300),(104.0,177.0,123.0)) # Convert Frame data to Blob data 
        model.setInput(blob) # model setting
        detections=model.forward() #predict 200 boxes for one frame
    except Exception as e:
        print(e)

    faces = [] # faces box to send on face recognition model

    width = frame.shape[1]
    height = frame.shape[0]

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
                endX = int(width)

            if startY < 0:
                startY = 0
            elif endY > height:
                endY = int(height)
            
            faces.append((startY, endX, endY, startX)) # top, right, bottom left

            # Draw infos in Frame==================================================================    
            print("{:.2f}%".format(confidence * 100), startX, startY, endX, endY)
            #======================================================================================

    return faces