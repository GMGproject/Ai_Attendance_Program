import socket
import struct
import pickle
import numpy as np
import cv2

from Server.Model.detection import detectSSD, detectMTCNN
from Server.Model.model import predict
from Server.Model.utils import checkFaceSize

from Server.utils import chanegeAttendance, getNowTime
from Server.db import queryExecutor

global resultList
resultList = []

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
    '''
    args discription
    client_socket : client connected socket
    '''
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
    '''
    args discription
    frame : frame from client
    faceSize : Set faceSize to recognize face
     - default = 200
    resultCheckSize : Set how many frames to check result
     - default = 10

    return
    frame : Drawn frame
    '''
    global resultList

    # Face Detection
    faces = detectSSD(frame)
    if len(faces) != 0:
        # Check Face Size to judge face Recognition
        passCheck, passFaces = checkFaceSize(faces, size=faceSize)

        if passCheck:
            # Face Recognition
            predictions = predict(frame, passFaces, model_path="./Server/Model/weights/trained_knn_model.clf")
            for name, (top, right, bottom, left) in predictions:
                resultList.append(name)
                print("- Found {} at ({}, {})".format(name, left, top))

                # Draw information on frame
                frame = cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
                cv2.putText(frame, name, (left, top - 5), cv2.FONT_HERSHEY_DUPLEX, 2,(0,0,255), 2, cv2.LINE_AA)

            print(len(resultList))
            if len(resultList) >= resultCheckSize:
                # Allow to change attendance data False -> True 
                resultName = chanegeAttendance(resultList)
                
                if resultName != "Unknown":
                    # Need getNowTime(), resultName to send sql query
                    sql = ("""UPDATE attend_info SET isAttendance = 1, attendanceTime = '{0}' 
                            WHERE studentID = (SELECT studentID FROM stu_info WHERE studentName = '{1}');""".format(getNowTime(), resultName))
                    queryExecutor(sql)

                    print("{0}님 출석처리 되었습니다".format(resultName))

                resultList.clear()

    return frame

def insertStudent(stuData):
    '''
    args discription
    stuData : student data to insert in DB
    '''

    stuID = stuData[0]
    stuName = stuData[1]

    sql = "INSERT INTO stu_info (studentID, studentName) VALUES ({0}, '{1}');".format(stuID, stuName)
    
    queryExecutor(sql)