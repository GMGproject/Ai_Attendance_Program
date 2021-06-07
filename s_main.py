import argparse
import threading

from Server.server import createServerSocket, returnInternalHost
from Server.server import recvData, checkMsg

from Server.Model.model import train

print("Training KNN classifier...")
classifier = train("./Server/Model/train", model_save_path="./Server/Model/weights/trained_knn_model.clf", n_neighbors=2)
print("Training complete!")

def main(args):

    host = args.host
    port = args.port
    client_socket = None

    # create server & client socket
    server_socket = createServerSocket(host=host, port=port)
    client_socket = None

    while True:
        print("waiting client")
        client_socket, addr = server_socket.accept()
        if client_socket != None:
            print("Connect with {0}:{1}".format(client_socket, addr))
            recvThread = threading.Thread(target=recvData, args=(client_socket,))
            recvThread.start()  
            break
            
    checkMsg()

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