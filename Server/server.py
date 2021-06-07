import socket
import struct
import pickle
import cv2

from Server.Model.detection import detectSSD
from Server.Model.model import predict
from Server.Model.utils import checkFaceSize

from Server.utils import chanegeAttendance, getNowTime, getToday, makeFolder
from Server.db import queryIUD, queryS

from threading import Thread

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
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(2 * 1024)  # 4K
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(2 * 1024)

            frame_data = data[:msg_size]
            data = data[msg_size:]
            dataList = pickle.loads(frame_data) 

            checkMsg(client_socket, dataList)

        except Exception as e:
            print("error : " + str(e))
            break
        except struct.error as se:
            print(se)
            print("server Disconnected")

def sendData(client_socket, data):
    '''
    args discription
    client_socket : socket for send data to client
    data          : any data for send to client
    '''
    try:
        a = pickle.dumps(data)
        message = struct.pack("Q", len(a)) + a
        sendResult = client_socket.sendall(message)
        if sendResult == None:
            pass
        else:
            raise Exception('Send Error')
    except Exception as e:
        print(e)
    
def checkMsg(client_socket, data):
    '''
    args discription
    data : recv data from client
    this function will split data and control to convey data to next function
    '''
    msg = data[0]
    image = data[1]

    if msg == "frame":
        sqlResult = faceRecognition(image)
        if sqlResult != None:
            sqlResult = ["attend", sqlResult]
        else:
            sqlResult = ["None", sqlResult]
    elif msg == "insert":
        stuID = data[2]
        stuName = data[3]
        sqlResult = insertStudent(image, stuID, stuName)
        sqlResult = ["insert", sqlResult]
    else:
        print("No data!!!!!!")

    sendData(client_socket, sqlResult)

def faceRecognition(frame, faceSize=200, resultCheckSize=10):
    '''
    args discription
    frame           : frame from client
    faceSize        : Set faceSize to recognize face
     - default = 200
    resultCheckSize : Set how many frames to check result
     - default = 10

    return
    sqlResult       : sql result for echo to client
    '''
    global resultList
    sqlResult = None

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
                            WHERE studentID = (SELECT studentID FROM stu_info WHERE studentName = '{1}')
                            AND attendanceDate = '{2}';""".format(getNowTime(), resultName, getToday()))
                    queryIUD(sql)
                    
                    # For Send Attendance Result to Client
                    sql = ("""SELECT isAttendance, studentID, (SELECT studentName FROM stu_info s WHERE s.studentID = a.studentID) as studentName 
                              FROM attend_info a WHERE attendanceDate = '{0}';""".format(getToday()))
                    sqlResult = queryS(sql)

                resultList.clear()

    return sqlResult

def insertStudent(stuFace, stuID, stuName):
    '''
    args discription
    stuFace   : student Face Data (np.ndarray)
    stuId     : studentID
    stuName   : studentName

    result
    sqlResult : sql result for echo to client 
    '''
    sqlResult = False

    trainPath = "./Server/Model/train/"

    # make folder & Save Image to train next time
    makeFolder(trainPath + stuName)
    cv2.imwrite('./Server/Model/train/{0}/{0}.PNG'.format(stuName), stuFace)

    # insert data in DB
    sql = "INSERT INTO stu_info (studentID, studentName) VALUES ({0}, '{1}');".format(stuID, stuName)
    queryIUD(sql)

    # check inserted data
    sql = ("SELECT studentName FROM stu_info WHERE studentID = {0};".format(stuID))
    sqlResult = queryS(sql)

    for column in sqlResult:
        print(column, type(column))
        if column[0] == stuName:
            sqlResult = True
            break

    return sqlResult
