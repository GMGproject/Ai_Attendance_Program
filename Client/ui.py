from Client.client import insertStudent
from Client.client import ClientSocket
from queue import Queue

import socket

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType('./Client/ui/AttModel.ui')[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        clientsocket = ClientSocket()
        super().__init__()  
        self.setupUi(self)

        
        # 버튼 이벤트
        self.btu_start.clicked.connect(lambda:clientsocket.connectWithServer())
        self.btu_finish.clicked.connect(lambda:clientsocket.disconnectWithServer())
        self.btu_picture.clicked.connect(self.openFile)
        self.btu_clear.clicked.connect(self.LogClear)

    # 파일 선택
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', "Image files (*.jpg *.png *.gif)")
        imagepath = fname[0]
        insertStudent(imagepath, "Daejeong", 201610560) 

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