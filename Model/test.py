from detection import detectSSD, detectMTCNN
from recognition import recogKNN
from utils import checkFaceSize
import cv2

cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

while True:
    retval, frame = cap.read()
    if not retval:
        break   
    frame = cv2.flip(frame, 1)   
    '''
    faces = detectSSD(width, height, frame)
    #faces = detectMTCNN(frame)

    passCheck, passFaces = checkFaceSize(faces)

    if passCheck:
        #names = recogKNN(passFaces)
        print("OK")
    '''


    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
        
cap.release()
cv2.destroyAllWindows()