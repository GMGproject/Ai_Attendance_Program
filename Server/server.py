import socket
import struct
import pickle
import numpy as np
import cv2

from Server.Model.detection import detectSSD, detectMTCNN
from Server.Model.model import predict
from Server.Model.utils import checkFaceSize, chanegeAttendance

def returnInternalHost():
    '''
    return : return my computer's internal host
    '''
    return socket.gethostbyname(socket.gethostname())

def createServerSocket(host, port):
    '''
    args discription
    host : server host number 
    port : server port number

    return
    server_socket : server socket to use
    '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("IP Address(Internal) : ",socket.gethostbyname(socket.gethostname()))

    return server_socket

def recvData(client_socket):
    data=b""
    payload_size=struct.calcsize("Q")

    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)  # 4K
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size] 
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)

            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)

            frame = faceRecognition(frame)

            cv2.imshow('server VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break

        except struct.error as se:
            print(se)
            print("server Disconnected")

def faceRecognition(frame, faceSize=200, resultCheckSize=10):
    resultList = []

    faces = detectSSD(frame)
    passCheck, passFaces = checkFaceSize(faces, size=faceSize)

    if passCheck:
        predictions = predict(frame, passFaces, model_path="./Server/Model/weights/trained_knn_model.clf")
        for name, (top, right, bottom, left) in predictions:
            resultList.append(name)
            print("- Found {} at ({}, {})".format(name, left, top))
            frame = cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
            cv2.putText(frame, name, (left, top - 5), cv2.FONT_HERSHEY_DUPLEX, 2,(0,0,255), 2, cv2.LINE_AA)

        if len(resultList) == resultCheckSize:
            chanegeAttendance(resultList)
            resultList.clear()

    return frame

    

        