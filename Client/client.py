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

    def connectWithServer(self, host, port):
        '''
        args discription
        client_socket : client socket to connect with server
        host          : server host number 
        port          : server port number
        '''
        try:
            self.client_socket.connect((host, port))
            print("Connected with {0}:{1}".format(host, port))

            videoCapture(self.client_socket)

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

    def returnClientSocket(self):
        return self.client_socket


def videoCapture(client_socket):
    '''
    args discription
    client_socket : socket for send data to server
    '''
    msg = "frame"
    vid = cv2.VideoCapture(0)

    while (vid.isOpened()):
        _, frame = vid.read()
        frame = cv2.flip(frame, 1)
        framelist = [msg, frame]
        retval = sendData(client_socket, framelist)

        if retval == False:
            break

        cv2.imshow("안면인식 출결 프로그램", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    vid.release()
    cv2.destroyAllWindows()

def insertStudent(client_socket, imgPath, stuID, stuName):
    '''
    args discription
    client_socket : socket for send data to server
    imgPath       : Image path to read and convert to np.ndarray
    stuID         : studentID
    stuName       : studentName
    '''

    msg = "insert" 
    image = cv2.imread(imgPath, cv2.IMREAD_ANYCOLOR)
    dataList = [msg, image, stuID, stuName]
    
    sendData(client_socket, dataList)

def sendData(client_socket, data):
    '''
    args discription
    client_socket : socket for send data to server
    data          : any data for send to server

    return
    True  : complete to recv data
    False : fail to recv data
    '''

    try:
        a = pickle.dumps(data)
        message = struct.pack("Q", len(a)) + a
        sendResult = client_socket.sendall(message)
        if sendResult == None:
            pass
        else:
            raise Exception('Send Error')

        dataList = recvData(client_socket)
        queue.put(dataList)

        return True

    except Exception as e:
        print(e)
        return False

def recvData(client_socket):
    '''
    args discription
    client_socket : client connected socket

    return
    dataList      : dataList from client 
    '''
    data = b""
    payload_size = struct.calcsize("Q")

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

        dataList = data[:msg_size]
        dataList = pickle.loads(dataList) 

        return dataList

    except Exception as e:
        print("error : " + str(e))
    except struct.error as se:
        print(se)
        print("server Disconnected")