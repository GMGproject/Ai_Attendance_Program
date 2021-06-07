import socket, argparse
import sys

from Client.ui import WindowClass

from PyQt5.QtWidgets import *

def main(args):
    app = QApplication(sys.argv)
    mainWindow = WindowClass()
    mainWindow.show()
    app.exec_()            

if __name__ == "__main__":
    # create parser instance
    parser = argparse.ArgumentParser(description='Client Args ip, port, camIndex')

    # Setup input values
    parser.add_argument('--host', type=str, default="localhost")
    parser.add_argument('--port', type=int, default=9999)
    parser.add_argument('--cam',  type=int, default=0)

    args = parser.parse_args()
    main(args)
