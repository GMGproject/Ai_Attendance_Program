import threading
import pickle
import struct
import socket
import cv2

from queue import Queue

global queue
queue = Queue()

class ClientSocket:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        #self.host = "192.168.0.112"
        #self.host = "192.168.10.35"
        self.host = "192.168.10.127"
        self.port = 9999

        self.connectWithServer()

    def connectWithServer(self):
        '''
        args discription
        client_socket : client socket to connect with server
        host          : server host number 
        port          : server port number
        '''
        try:
            self.client_socket.connect((self.host, self.port))
            print("Connected with {0}:{1}".format(self.host, self.port))
        except Exception as e:
            print("please check your host & port number")
            print(e)

    def disconnectWithServer(self):
        '''
        args discription
        client_socket : client socket to disconnect with server
        '''
        try:
            self.client_socket.close()
            print("Disconnected with server")
        except Exception as e:
            print("failed to disconnect with server")        
            print(e)

    def sendData(self, data):
        try:
            a = pickle.dumps(data)
            message = struct.pack("Q", len(a)) + a
            sendResult = self.client_socket.sendall(message)
            if sendResult == None:
                print("send Data")
            else:
                raise Exception('Send Error')
        except Exception as e:
            print(e)


def videoCapture(client_socket):
    msg = "frame"
    vid = cv2.VideoCapture(0)

    while (vid.isOpened()):
        _, frame = vid.read()
        frame = cv2.flip(frame, 1)
        framelist = [msg, frame]
        
        client_socket.sendData(framelist)

        cv2.imshow("CLIENT VIDEO",frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

def insertStudent(client_socket, imgPath, stuName, stuID):
    msg = "insert" 
    image = cv2.imread(imgPath, cv2.IMREAD_ANYCOLOR)
    dataList = [msg, image, stuName, stuID]
    
    client_socket.sendData(dataList)

def startClient():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket = ClientSocket(client_socket)

    vidThread = threading.Thread(target=videoCapture, args=(client_socket,))
    vidThread.start()

def endClient():
    pass