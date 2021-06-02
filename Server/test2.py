import argparse
import pickle
import cv2
import struct
import numpy
import threading

from server import createServerSocket

def main(args):
    host = args.host
    port = args.port
    client_socket = None

    # create server socket
    server_socket = createServerSocket(host=host, port=port)

    while True:
        print("waiting client")
        client_socket, addr = server_socket.accept()
        if client_socket != None:
            print("Connect with {0}:{1}".format(client_socket, addr))

            thread_stratServer = threading.Thread(target=recvvdieo(client_socket))
            thread_stratServer.start() 


def recvvdieo(client_socket):
    #data = b"" # 데이터 크기를 먼저 보내 서버에게 데이터 받게 대기하도록
    vid = cv2.VideoCapture(0)
    index = 0
    try:
        while (vid.isOpened()):
            img, frame = vid.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            cv2.imshow('server VIDEO', frame)
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
            index += 1
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        client_socket.close()
    except:
        client_socket.close()

def recvimg(client_socket):
    length = recvall(client_socket,16) #길이 16의 데이터를 먼저 수신하는 것은 여기에 이미지의 길이를 먼저 받아서 이미지를 받을 때 편리하려고 하는 것이다.
    stringData = recvall(client_socket, int(length))
    data = numpy.fromstring(stringData, dtype='uint8')
    decimg=cv2.imdecode(data,1)
    cv2.imshow('SERVER',decimg)

def recvall(client_socket, count):
    buf = b''
    while count:
        newbuf = client_socket.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

if __name__ == "__main__":
    # create parser instance
    parser = argparse.ArgumentParser(description='Server Args ip, port')

    # Setup input values# "192.168.10.35"
    parser.add_argument('--host', type=str, default="192.168.99.1")
    parser.add_argument('--port', type=int, default=9999)

    args = parser.parse_args()
    main(args)