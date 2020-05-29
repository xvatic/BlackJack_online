from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
import pickle
import sqlite3
import settings
from server_gui import Ui_Form


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.clients = {}
        self.history_list = []
        self.client_info = {}
        self.rooms = {}

        self.STATE = settings.LOGGIN

        self.signal = New_message_event_handle()
        self.signal.new_message_serv.connect(self.new_message_serv)

    def append_message_to_server_log(message):
        self.ui.textEdit_server_log.append(f'{message_converted} {address}')
        final_message = self.serialize(final_message)

    def string_to_dictionary(self, message):
        content = message.split('~')
        mode, client_id, reciever, login, message = content[0], content[1], content[2], content[3], content[4]
        history_element = {1: mode, 2: client_id, 3: reciever, 4: login, 5: message}
        return history_element

    def common_message(self, mode, client_id, reciever, login, message):
        final_message = {1: mode, 2: client_id, 3: reciever, 4: login, 5: message}
        return final_message

    def serialize(self, message_dictionary):
        message_byte_form = pickle.dumps(message_dictionary)
        return message_byte_form

    def deserialize(self, message_byte_form):
        message_dictionary = pickle.loads(message_byte_form)
        return message_dictionary

    def process_game_state(self, state):
        return

    def process_request(self, data, connection, address):
        try:
            mode = data[settings.MODE_KEY]
        except KeyError:
            return False

        login = data[settings.LOGIN_KEY]
        if mode == settings.MODE_CONNECT:
            password = data[settings.PASSWORD_KEY]
            client_id, client_ip = str(address[1]), address[0]

            self.client_info[client_id] = login
            if self.database.verify_client(password, login) == True:
                cash = self.database.get_cash(login)

                message = {settings.MODE_KEY: settings.MODE_CONNECT,
                           settings.RESULT_KEY: settings.SUCCESS, settings.CASH_KEY: cash}
                connection.send(self.serialize(message))
                return True
            else:
                message = {settings.MODE_KEY: settings.MODE_CONNECT,
                           settings.RESULT_KEY: settings.FAIL}
                connection.send(self.serialize(message))
                return True

        if mode == settings.MODE_REGISTER:
            password = data[settings.PASSWORD_KEY]
            client_id, client_ip = str(address[1]), address[0]
            self.client_info[client_id] = login
            if self.database.register_client(password, login) == True:
                cash = self.database.get_cash(login)
                message = {settings.MODE_KEY: settings.MODE_REGISTER,
                           settings.RESULT_KEY: settings.SUCCESS, settings.CASH_KEY: cash}
                connection.send(self.serialize(message))
                return True
            else:
                message = {settings.MODE_KEY: settings.MODE_REGISTER,
                           settings.RESULT_KEY: settings.FAIL}
                connection.send(self.serialize(message))
                return True
        if mode == settings.MODE_DISCONNECT:
            pass

        if mode == settings.MODE_DONATE:
            if self.database.check_promocode(data[settings.CODE_KEY], login) == True:
                cash = self.database.get_cash(login)
                message = {settings.MODE_KEY: settings.MODE_DONATE, settings.CASH_KEY: cash}
                connection.send(self.serialize(message))
                return True
        return False

    def new_message_serv(self):
        mode = ''
        login = ''
        client_id = ''
        connection = ''
        message_content = ''
        reciever = ''
        processed_data = {}
        data = self.TCPSocket_app.flush()
        try:
            processed_data = self.deserialize(data)
        except EOFError:
            pass
        connection, address = self.TCPSocket_app.get_client_connection_info()
        try:
            mode = processed_data[settings.MODE_KEY]
        except KeyError:
            pass

        if mode == settings.MODE_GAME:
            self.process_game_state(processed_data)

        if self.process_request(processed_data, connection, address) == True:
            return

        if reciever == settings.MARKER_ALL:
            self.store(mode, client_id, reciever, login, message_converted)

        if mode == settings.MODE_COMMON:
            final_message = self.common_message(mode, client_id, reciever, login, message_converted)

    def send_to_client(self, message, reciever, connection):
        for client_value, address_value in self.clients.items():
            if connection != client_value:
                if address_value == reciever:
                    client_value.send(message)
                elif reciever == settings.MARKER_ALL:
                    client_value.send(message)

    def set_tcp_socket(self, socket):
        self.TCPSocket_app = socket

    def set_database_connection(self, database):
        self.database = database

    def thread_option(self):
        while True:
            connection, address = self.TCPSocket_app.accept()
            self.clients[connection] = str(address[1])

    def start(self):
        thread = threading.Thread(target=self.thread_option, daemon=True)
        thread.start()


class New_message_event_handle(QObject):
    new_message_serv = pyqtSignal()


if __name__ == "__main__":

    import sys
    import socket
    import threading
    import time

    from network import TCPTools
    from database_interaction import Users
    HOST = socket.gethostbyname(socket.gethostname())
    PORT = 12345

    app = QtWidgets.QApplication(sys.argv)
    application = Window()
    application.show()

    info = Users()
    info.check_database_existing()
    application.set_database_connection(info)

    TCPSocket = TCPTools(application.signal.new_message_serv)
    TCPSocket.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPSocket.socket.bind((HOST, PORT))
    TCPSocket.socket.listen(10)
    TCPSocket.set_server_flag()
    application.set_tcp_socket(TCPSocket)
    application.start()

    sys.exit(app.exec_())
