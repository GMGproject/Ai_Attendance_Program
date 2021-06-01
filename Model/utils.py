'''
def drawRectangle():
    text = "{:.2f}%".format(confidence * 100)
    y = startY - 10 if startY - 10 > 10 else startY + 10 # set y position to write percentage of confidence value on left top of boxes
    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
    cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
'''

def checkFaceSize(faces, size=100):
    '''
    args discription
    faces : detected faces list from frame
    size : to set standard of face size
     - default = 100

    return
    passCheck : variables to determine the next process
    passFaces : faces that satisfied our own standard
    '''

    passedFaces = []
    passCheck = False

    if len(faces) == 0:
        pass
    else:    
        for face in faces:
            if (face[2] - face[0]) > size:
                passedFaces.append(face)
                passCheck = True

    return passCheck, passedFaces