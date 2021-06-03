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

def recvData(client_socket):
        data = b""
        payload_size = struct.calcsize("Q")

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
        except struct.error as se:
                print(se)
                print("server Disconnected")
                
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)

        return frame
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        