from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject
import pickle
import pyglet
from client_gui import Ui_Form
from time import localtime, strftime


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.signal = New_message_event_handle()
        self.signal.process_message.connect(self.process_message)
        self.MODE_CLIENTS = '03'
        self.MODE_CONNECT = '01'
        self.MODE_DISCONNECT = '02'
        self.MODE_COMMON = '00'

        self.NEEDED_HOST = socket.gethostbyname(socket.gethostname())
        self.NEEDED_PORT = 12345

        self.MARKER_ALL = '10'
        self.message_list = []
        self.clients = {}
        self.reciever_address = self.MARKER_ALL
        self.sound = pyglet.media.load('files/sms_uvedomlenie_na_iphone.wav', streaming=False)

    def configure_socket(self):
        self.TCPSocket.set_host_and_port(NEEDED_HOST, NEEDED_PORT)

    def login(self):
        self.configure_socket()
        self.TCPSocket.set_login_and_password('', application.ui.lineEdit_2_password.toPlainText())
        self.TCPSocket.connect()

    def register(self):
        self.configure_socket()
        self.TCPSocket.set_login_and_password(
            application.ui.lineEdit_login, application.ui.lineEdit_2_password.toPlainText())
        self.TCPSocket.register()

    def manage_gui(self):
        self.ui.groupBox_Enter.setVisible(True)
        self.ui.groupBox_LogIn.setVisible(False)

    def process_message():
        pass

    def set_tcp_socket(self, socket):
        self.TCPSocket = socket


class New_message_event_handle(QObject):
    process_message = pyqtSignal()


if __name__ == "__main__":
    import sys
    import socket
    import threading
    import time

    from network import TCPTools

    app = QtWidgets.QApplication(sys.argv)
    application = Window()
    application.ui.groupBox_Game.setVisible(False)
    application.ui.groupBox_Enter.setVisible(False)
    application.show()
    TCPSocket = TCPTools(application.signal.process_message)
    application.set_tcp_socket(TCPSocket)
    application.ui.pushButton_register.clicked.connect(application.register)
    application.ui.pushButton_connect.clicked.connect(application.login)

    sys.exit(app.exec_())
