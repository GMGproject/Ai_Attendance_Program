# Face Recognition

import face_recognition
import cv2
import numpy as np

def getFaceEncoding(faceDir, name):
    '''
    arg discription
    faceDir : face image dir
    name : person's name in face image

    return
    faceDictData : name + face encoding dictionary data
    '''

    image = face_recognition.load_image_file(faceDir)
    faceEncoding = face_recognition.face_encodings(image)[0]
    faceDictData = {name : faceEncoding}

    return faceDictData

def recogKNN(passedFaces):
    pass
