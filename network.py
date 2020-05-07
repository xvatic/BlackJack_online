import socket
import threading
import time
from PyQt5 import QtCore, QtWidgets
from time import localtime, strftime
import pickle


class TCPTools(QtWidgets.QWidget):
    def __init__(self, signal):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.login = ''
        self.server_flag = False
        self.message_signal = signal

        self.MODE_CLIENTS = '03'
        self.MODE_CONNECT = '01'
        self.MODE_DISCONNECT = '02'
        self.MODE_COMMON = '00'
        self.MODE_HISTORY = '04'

        self.MARKER_ALL = '10'

    def fill(self, message):
        self.message = message

    def flush(self):
        return self.message

    def sending(self, mode, reciever, message):
        time = strftime("%H:%M:%S %d-%m-%Y", localtime())
        message = f' AT {time} : {message}'
        final_message = {1: mode, 2: reciever, 3: self.login, 4: message}
        try:
            self.socket.send(pickle.dumps(final_message))
        except OSError:
            pass

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.sending(self.MODE_CONNECT, self.MARKER_ALL, 'connected')
        self.start_TCP_thread_recieve(None, None)

    def set_login(self, value):
        self.login = value

    def set_host_and_port(self, host, port):
        self.host = host
        self.port = port

    def accept(self):
        connection, address = self.socket.accept()

        self.start_TCP_thread_recieve(connection, address)
        return connection, address

    def set_client_connection_info(self, connection, address):
        self.connection = connection
        self.address = address

    def get_client_connection_info(self):
        return self.connection, self.address

    def set_server_flag(self):
        self.server_flag = True

    def recieve(self, connection, address):
        while not self.stopped:
            try:
                while not self.stopped:
                    if self.server_flag:
                        data = connection.recv(1024)
                        self.set_client_connection_info(connection, address)
                    else:
                        data = self.socket.recv(1024)
                    self.fill(data)
                    self.message_signal.emit()
                    time.sleep(2)
            except:
                self.stopped = True

    def start_TCP_thread_recieve(self, connection, address):
        self.stopped = False

        Thread_recieve = threading.Thread(
            target=self.recieve, args=(connection, address), daemon=True)
        Thread_recieve.start()

    def disconnect(self):
        self.sending(self.MODE_DISCONNECT, self.MARKER_ALL, "left")
        self.stopped = True
        self.socket.close()