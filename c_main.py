import socket, argparse
from Client.client import connectWithServer, disconnectWithServer

def main(args):
    host = args.host
    port = args.port
    cam = args.cam

    # create client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connectWithServer(client_socket=client_socket,
                        host=host, 
                        port=port)
                        
    while True:
        print("helloworld")
        break
        
    disconnectWithServer(client_socket)
    

if __name__ == "__main__":
    # create parser instance
    parser = argparse.ArgumentParser(description='Client Args ip, port, camIndex')

    # Setup input values
    parser.add_argument('--host', type=str, default="localhost")
    parser.add_argument('--port', type=int, default=9999)
    parser.add_argument('--cam',  type=int, default=0)

    args = parser.parse_args()
    main(args)
