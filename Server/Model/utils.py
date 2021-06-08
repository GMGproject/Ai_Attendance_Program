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

