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
        self.SUCCESS = '12'
        self.FAIL = '13'

        self.RESULT_KEY = 'result'
        self.MODE_KEY = 'mode'
        self.RECIEVER_KEY = 'reciever'
        self.PASSWORD_KEY = 'password'
        self.LOGIN_KEY = 'login'
        self.MESSAGE_KEY = 'message'
        self.ROOMS_KEY = 'rooms'
        self.CASH_KEY = 'cash'

        self.NEEDED_HOST = socket.gethostbyname(socket.gethostname())
        self.NEEDED_PORT = 12345
        self.cash = 0

        self.MARKER_ALL = '10'
        self.MARKER_ROOM = '11'
        self.message_list = []
        self.clients = {}
        self.reciever_address = self.MARKER_ALL

    def serialize(self, message_dictionary):
        message_byte_form = pickle.dumps(message_dictionary)
        return message_byte_form

    def deserialize(self, message_byte_form):
        message_dictionary = pickle.loads(message_byte_form)
        return message_dictionary

    def configure_socket(self):
        self.TCPSocket.set_host_and_port(self.NEEDED_HOST, self.NEEDED_PORT)

    def login(self):
        self.configure_socket()
        self.TCPSocket.set_login_and_password(
            application.ui.lineEdit_login.text(), application.ui.lineEdit_2_password.text())
        self.TCPSocket.connect()

    def register(self):
        self.configure_socket()
        self.TCPSocket.set_login_and_password(
            application.ui.lineEdit_login.text(), application.ui.lineEdit_2_password.text())
        self.TCPSocket.register()

    def process_request(self, data):
        try:
            mode = data[self.MODE_KEY]
        except KeyError:
            return False
        print(data)
        if mode == self.MODE_CONNECT:
            if data[self.RESULT_KEY] == self.SUCCESS:
                self.cash = data[self.CASH_KEY]
                self.manage_gui()
                return True

        if mode == self.MODE_REGISTER:
            if data[self.RESULT_KEY] == self.SUCCESS:
                self.cash = data[self.CASH_KEY]
                self.manage_gui()
                return True

        if mode == self.MODE_DISCONNECT:
            return True

    def process_message(self):
        processed_data = {}
        data = self.TCPSocket.flush()
        try:
            processed_data = self.deserialize(data)
        except EOFError:
            pass
        if self.process_request(processed_data) == True:
            return

    def manage_gui(self):
        self.ui.groupBox_Enter.setVisible(True)
        self.ui.groupBox_LogIn.setVisible(False)

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
