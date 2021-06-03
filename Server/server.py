import socket
import struct
import pickle
import numpy as np
import cv2

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

def sendData(client_socket, data):
    try:
        #packedData = packData(data)
        a = pickle.dumps(data)
        message = struct.pack("Q", len(a)) + a
        client_socket.sendall(message)
    except Exception as e:
        print(e)

def recvData(client_socket, recvSize=1024):
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * recvSize)
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size] 
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4 * recvSize)
        except struct.error as se:
                print(se)
                print("server Disconnected")
                break
                
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.imshow('server VIDEO', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        #convertData(data)
        
def convertData(data):
    try:
        if data == None:
            pass
        else:
            if data[0] == "frame":
                # convert data type string to np.ndarray
                data = data[1]               
                print(type(data))
            elif data[0] == "string":
                # split image data & name data
                data = data[1]               
                print(type(data))
    except Exception as e:
        print(e)
        pass

def packData(data):
    """
    만약 데이터 타입이 Array면 Image@ + 데이터
    만약 데이터 타입이 String이면 String@ + 데이터
    해서 sendData로 전송
    """
    packedData = []

    if type(data) == str:
        packedData.append("string")
    elif type(data) == np.ndarray:
        packedData.append("frame")

    packedData.append(data)
    return packedData
