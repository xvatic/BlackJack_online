from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject
import pickle
import pyglet
import settings
from client_gui import Ui_Form
from time import localtime, strftime


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.signal = New_message_event_handle()
        self.signal.process_message.connect(self.process_message)

        self.NEEDED_HOST = socket.gethostbyname(socket.gethostname())
        self.NEEDED_PORT = 12345
        self.cash = 0
        self.login_player = ''

        self.message_list = []
        self.clients = {}
        self.reciever_address = settings.MARKER_ALL

        self.LOGGIN = '1'
        self.MAIN = '2'
        self.GAME = '3'
        self.STATE = settings.LOGGIN

    def create_room(self):
        message = {settings.MODE_KEY: settings.MODE_CREATE_GAME, settings.LOGIN_KEY:
                   application.ui.lineEdit_gamename.text(), settings.PASSWORD_KEY: self.ui.lineEdit_gamepassword.text()}
        self.send_to_server(message)

    def refresh_main_ui(self):
        self.ui.label_money.setText(f"{self.cash}")

    def activate(self):
        code = self.ui.lineEdit_code.text()
        message = {settings.MODE_KEY: settings.MODE_DONATE,
                   settings.CODE_KEY: code, settings.LOGIN_KEY: self.login_player}
        self.send_to_server(message)

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
        self.login_player = self.ui.lineEdit_login.text()
        self.TCPSocket.set_login_and_password(
            application.ui.lineEdit_login.text(), application.ui.lineEdit_2_password.text())
        self.TCPSocket.connect()

    def register(self):
        self.configure_socket()
        self.login_player = self.ui.lineEdit_login.text()
        self.TCPSocket.set_login_and_password(
            application.ui.lineEdit_login.text(), application.ui.lineEdit_2_password.text())
        self.TCPSocket.register()

    def process_request(self, data):
        try:
            mode = data[settings.MODE_KEY]
        except KeyError:
            return False

        if mode == settings.MODE_CONNECT:
            if data[settings.RESULT_KEY] == settings.SUCCESS:
                self.cash = data[settings.CASH_KEY]
                self.set_form(True, False, False)
                self.confugure_entry_form()
                return True

        if mode == settings.MODE_REGISTER:
            if data[settings.RESULT_KEY] == settings.SUCCESS:
                self.cash = data[settings.CASH_KEY]
                self.set_form(True, False, False)
                self.confugure_entry_form()
                return True

        if mode == settings.MODE_DISCONNECT:
            return True

        if mode == settings.MODE_DONATE:
            self.cash = data[settings.CASH_KEY]
            self.refresh_main_ui()

        if mode == settings.MODE_CREATE_GAME:
            if data[settings.RESULT_KEY] == settings.SUCCESS:
                self.set_form(False, False, True)

    def process_message(self):
        processed_data = {}
        data = self.TCPSocket.flush()
        try:
            processed_data = self.deserialize(data)
        except EOFError:
            pass
        if self.process_request(processed_data) == True:
            return

    def send_to_server(self, message):
        message = self.serialize(message)
        self.TCPSocket.send_to_server(message)

    def set_form(self, enterState, loginState, gameState):
        self.ui.groupBox_Enter.setVisible(enterState)
        self.ui.groupBox_LogIn.setVisible(loginState)
        self.ui.groupBox_Game.setVisible(gameState)

    def confugure_entry_form(self):
        self.ui.label_money.setText(f"{self.cash}")

    def confugure_game_form(self):
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
    application.ui.pushButton_activate.clicked.connect(application.activate)
    application.ui.pushButton_creategame.clicked.connect(application.create_room)

    sys.exit(app.exec_())
