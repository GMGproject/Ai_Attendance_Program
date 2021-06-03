import argparse
import threading
import cv2

from server import createServerSocket, returnInternalHost
from server import recvData

from detection import detectSSD, detectMTCNN
from recognition import getFaceEncoding
from model import predict, train
from utils import checkFaceSize, chanegeAttendance
import cv2
#from server import packData, sendData

print("Training KNN classifier...")
classifier = train("./Model/train", model_save_path="./Model/weights/trained_knn_model.clf", n_neighbors=2)
print("Training complete!")

def main(args):
    faceSize = 200
    resultCheckSize = 10
    resultList = []

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

        while client_socket:
            frame = recvData(client_socket)
            frame = cv2.flip(frame, 1)
            width = frame.shape[0]
            height = frame.shape[1]

            faces = detectSSD(width, height, frame)
            passCheck, passFaces = checkFaceSize(faces, size=faceSize)
            if passCheck:
                predictions = predict(frame, passFaces, model_path="./Model/weights/trained_knn_model.clf")
                for name, (top, right, bottom, left) in predictions:
                    resultList.append(name)
                    print("- Found {} at ({}, {})".format(name, left, top))
                    frame = cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
                    cv2.putText(frame, name, (left, top - 5), cv2.FONT_HERSHEY_DUPLEX, 2,(0,0,255), 2, cv2.LINE_AA)

                print("OK")

                if len(resultList) == resultCheckSize:
                    chanegeAttendance(resultList)
                    resultList.clear()

            
            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)
            if key == 27:
                break

            cv2.imshow('server VIDEO', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        
    
if __name__ == "__main__":
    # get internal host
    internalHost = returnInternalHost()

    # create parser instance
    parser = argparse.ArgumentParser(description='Server Args ip, port')

    # Setup input values
    parser.add_argument('--host', type=str, default=internalHost)
    parser.add_argument('--port', type=int, default=9999)

    args = parser.parse_args()
    main(args)