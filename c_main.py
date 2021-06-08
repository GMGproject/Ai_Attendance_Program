import sys

from Client.ui import WindowClass

from PyQt5.QtWidgets import *

def main():
    app = QApplication(sys.argv)
    mainWindow = WindowClass()
    mainWindow.show()
    app.exec_()            

if __name__ == "__main__":
    main()
