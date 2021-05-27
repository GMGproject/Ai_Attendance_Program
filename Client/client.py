
def connectWithServer(client_socket, host, port):
    '''
    args discription
    client_socket : client socket to connect with server
    host          : server host number 
    port          : server port number
    '''
    try:
        client_socket.connect((host, port))
        print("Connected with {0}:{1}".format(host, port))
    except Exception as e:
        print("please check your host & port number")
        print(e)

def disconnectWithServer(client_socket):
    '''
    args discription
    client_socket : client socket to disconnect with server
    '''
    try:
        client_socket.close()
        print("Disconnected with server")
    except Exception as e:
        print("failed to disconnect with server")        
        print(e)