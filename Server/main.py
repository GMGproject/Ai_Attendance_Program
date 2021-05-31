import argparse

from server import createServerSocket, returnInternalHost

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

        while client_socket:
            print("Hello World")
            #break
        
    
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