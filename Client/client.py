import threading
import pickle
import struct
import socket
import cv2

from queue import Queue

global queue
queue = Queue()

class ClientSocket:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "192.168.0.112"
        self.port = 9999

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
            self.start()
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

    def sendData(self):
        while True:
            try:
                data = queue.get()
                a = pickle.dumps(data)
                message = struct.pack("Q", len(a)) + a
                self.client_socket.sendall(message)
            except Exception as e:
                print(e)
                break

    def start(self):
        videoThread = threading.Thread(target=videoCapture)
        videoThread.start()

        sendThread = threading.Thread(target=ClientSocket.sendData, args=())
        sendThread.start()

def videoCapture():
    msg = "frame"
    vid = cv2.VideoCapture(0)

    while (vid.isOpened()):
        _, frame = vid.read()
        frame = cv2.flip(frame, 1)
        framelist = [msg, frame]
        queue.put(framelist)

        cv2.imshow("CLIENT VIDEO",frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

def insertStudent(imgPath, stuName, stuID):
    msg = "insert" 
    image = cv2.imread(imgPath, cv2.IMREAD_ANYCOLOR)
    dataList = [msg, image, stuName, stuID]
    queue.put(dataList)

