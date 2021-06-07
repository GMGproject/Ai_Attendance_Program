from Client.client import ClientSocket
from Client.client import insertStudent, queue
from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_class = uic.loadUiType('./Client/ui/AttModel.ui')[0]

"""
서버 IP = text_host
서버 Port = text_port
학생 이름 = text_studentName
학생 학번 = text_studentID

사용자 추가 버튼 = btu_insert
사진 찾기 버튼 = btu_picture
Clear 버튼 = btu_clear
연결 버튼 = btu_start
해제 버튼 = btu_finish

사진 영역 = label_image
폴더 경로 = label_folderName
"""

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()  
        self.cs = ClientSocket()
        self.setupUi(self)

        self.client_socket = None
        self.host = None
        self.port = None
        self.filePath = None
        self.stuName = None
        self.stuID = None

        # Button Events
        self.btu_start.clicked.connect(self.connectServer)
        self.btu_finish.clicked.connect(self.disconnectServer)
        self.btu_picture.clicked.connect(self.openFileThread)
        self.btu_insert.clicked.connect(self.insertStudent)
        self.btu_clear.clicked.connect(self.logClear)

        checkThread = Thread(target=self.checkMsg)
        checkThread.start()

        
    def createMsgbox(self, msg):
        """
        arg discription
        msg : message to put on MessageBox
        """
        QMessageBox.about(self, "System Message", msg)

    def connectServer(self):
        self.host = self.text_host.toPlainText()
        self.port = int(self.text_port.toPlainText())
        
        self.cs.connectWithServer(self.host, self.port)
        self.isServerConnected = True
        self.client_socket = self.cs.returnClientSocket()     
        

    def disconnectServer(self):
        self.cs.disconnectWithServer()
        self.isServerConnected = False

    def openFileThread(self):
        insertThread = Thread(target=self.openFile)
        insertThread.start()

    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', "Image files (*.jpg *.png *.gif)")
        self.filePath = fname[0]

        self.label_image.setPixmap(QPixmap(self.filePath))
        self.label_folderName.setText(self.filePath)

    def insertStudent(self):
        self.stuName = self.text_studentName.toPlainText()
        self.stuID = self.text_studentID.toPlainText()

        # Check Empty data
        if self.stuName == None or self.stuName == "":
            self.createMsgbox("학생 이름을 입력하세요")
        elif self.stuID == None or self.stuID == "":
            self.createMsgbox("학생 학번을 입력하세요")
        elif self.filePath == None:
            self.createMsgbox("등록할 사진을 선택하세요")
        else:          
            insertStudent(self.cs.returnClientSocket(), self.filePath, int(self.stuID), self.stuName)

            # Reset Label & textEdits
            self.label_folderName.setText("")
            self.label_image.setText("")
            self.stuName = None
            self.stuID = None
            self.text_studentName.clear()
            self.text_studentID.clear()

    # Clear Log
    def logClear(self):
        self.list_log.clear()

    # Add Log in List
    def addLog(self, dataList):
        self.logClear()
        for column in dataList:
            isAttendance = column[0]
            studentName = column[2]
            if isAttendance == 1:
                isAttendance = "출석"
            else:
                isAttendance = "결석"
            
            msg = "{0}님은 현재 {1} 상태입니다.".format(studentName, isAttendance)
            self.list_log.addItem(msg) # 리스트에 글자 더하기

    def checkMsg(self):
        '''
        args discription
        data : recv data from server
        this function will split data and control to convey data to next function
        '''
        while True:
            dataList = queue.get()

            if dataList[0] == "attend":
                # list
                self.addLog(dataList[1])
            elif dataList[0] == "insert":
                # boolean
                if dataList[1] == True:
                    print("정보 등록 성공")
                else:
                    print("정보 등록 실패")
            elif dataList[0] == "None":
                pass