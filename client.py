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
        self.signal.message_processing.connect(self.message_processing)
        self.MODE_CLIENTS = '03'
        self.MODE_CONNECT = '01'
        self.MODE_DISCONNECT = '02'
        self.MODE_COMMON = '00'
        self.MODE_HISTORY = '04'

        self.MARKER_ALL = '10'
        self.message_list = []
        self.clients = {}
        self.reciever_address = self.MARKER_ALL
        self.sound = pyglet.media.load('files/sms_uvedomlenie_na_iphone.wav', streaming=False)

    def search(self):
        ClIENT_HOST = socket.gethostbyname(socket.gethostname())
        ClIENT_PORT = 12345
        UDPSocket = UDPTools(ClIENT_HOST, ClIENT_PORT)
        UDPSocket.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        UDPSocket.start_UDP_thread_recieve()
        UDPSocket.start_UDP_thread_send()
        time.sleep(2)
        host, port = UDPSocket.flush()
        needed_host = str(host)
        needed_port = int(port)
        UDPSocket.stopped_connection()
        self.TCPSocket.set_host_and_port(needed_host, needed_port)
        self.TCPSocket.set_login(application.ui.textEdit_setName.toPlainText())
        self.TCPSocket.connect()
        self.history()


if __name__ == "__main__":
    import sys
    import socket
    import threading
    import time

    from Network import TCPTools, UDPTools

    app = QtWidgets.QApplication(sys.argv)
    application = Window()
    application.show()
    TCPSocket = TCPTools(application.signal.message_processing)
    application.set_tcp_socket(TCPSocket)

    application.ui.pushbutton_Connect.clicked.connect(application.search)
    application.ui.pushButton_sendMessage.clicked.connect(application.convert)
    application.ui.pushButton_switch.clicked.connect(application.switch_to_private)
    application.ui.pushButton_toall.clicked.connect(application.return_to_all)
    application.ui.pushbutton_Disconnect.clicked.connect(application.leave)

    sys.exit(app.exec_())
