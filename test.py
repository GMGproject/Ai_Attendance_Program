from queue import Queue
import sys
import threading
import socket
import cv2
import pickle
import struct
import numpy as np

from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox #메세지 박스
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *


form_class = uic.loadUiType('D:\\Ai_Attendance_Program06043.2\\Client2\\AttModel2.ui')[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()  
        self.setupUi(self)
        #self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.q = Queue()
        
        # 버튼 이벤트
        self.btu_picture.clicked.connect(self.openFile)
        self.btu_start.clicked.connect(self.Start)
        self.btu_finish.clicked.connect(self.disconnectWithServer)
        self.btu_clear.clicked.connect(self.LogClear)

    # 스레드로 서버 실행
    def Start(self):
        th = threading.Thread(target=self.connectWithServer)
        th.start()   

     # 서버와 연결
    def connectWithServer(self):
        '''
        args discription
        client_socket : client socket to connect with server
        host          : server host number 
        port          : server port number
        '''
        self.startTimer()     
        while True:
            try:
                host = "61.251.5.24" #192.168.99.1 # 192.168.10.35 #61.251.5.24
                port = 9999
                global client_socket
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, port))
                print("Connected with {0}:{1}".format(host, port)) 
                self.addLog(host)  

                self.videoCapture(client_socket)

                break   
            except Exception as e:
                print("please check your host & port number")
                client_socket.close()
                print(e)
            
    # 서버 연결해제     
    def disconnectWithServer(self):
        '''
        args discription
        client_socket : client socket to disconnect with server
        '''
        try:
            self.server_socket.close()
            print("Disconnected with server")
        except Exception as e:
            print("failed to disconnect with server")        
            print(e)

    # 파일 선택
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', "Image files (*.jpg *.png *.gif)")
        imagepath = fname[0]

        self.sendimg(imagepath) 
       

    def sendData(self, client_socket):
        data = self.q.get()
        a = pickle.dumps(data)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)

    # 이미지 보내는 함수
    def sendimg(self,client_socket, imgname):
        msg = "img" 
        filename = imgname #'img_o2.jpg'
        f = open(filename,'rb')
        img = f.read(1024)
        #a = pickle.dumps(l)
        #msg = struct.pack("Q", len(a)) + a 
        imglist = [msg, img]
        print(msg)
        try:
            imgdata = self.q.put(imglist)
            self.sendData(client_socket,imgdata)
        except Exception as e:
            print(e)
        f.close()

    def videoCapture(self, client_socket):
        msg = "frame"
        vid = cv2.VideoCapture(0)
        while (vid.isOpened()):
            _, frame = vid.read()
            frame = cv2.flip(frame, 1)
            framelist = [msg, frame]
            print(msg)
            try:
                framedata = self.q.put(framelist)
                self.sendData(client_socket, framedata)
            except Exception as e:
                print(e)

            #cv2.imshow("CLIENT VIDEO",frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            
    def startTimer(self):
        print("timer")
        self.q.put(["Timer", "Timer2"])
        timer = threading.Timer(2, self.startTimer)
        timer.start()

    #Queue -> 여기에 보낼 데이터를 1렬로 저장
    #Send를 할때 Queue에서 하나씩 빼서 전송


    #로그 리스트 클리어하는 함수
    def LogClear(self):
        self.list_log.clear()

    #로그 리스트 출력하는 함수
    def addLog(self, msg): #로그 출력
        self.list_log.addItem("system: " + msg) # 리스트에 글자 더하기

    #메세지 박스 출력
    def createMsgbox(self, msg): # 메세지 박스 출력
        print(msg)
        msgBox = QMessageBox()
        msgBox.setWindowTitle("System Message")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(msg)
        msgBox.setFixedSize(500, 500)
        msgBox.setStandardButtons(QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Cancel)
        msgBox.exec_()

app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec_()            

