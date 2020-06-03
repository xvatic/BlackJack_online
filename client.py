from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
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
        self.p = self.palette()
        self.p.setColor(self.backgroundRole(), QtCore.Qt.gray)
        self.setPalette(self.p)

        self.NEEDED_HOST = socket.gethostbyname('localhost')
        self.NEEDED_PORT = 12345
        self.cash = 0
        self.login_player = ''
        self.current_room = ''

        self.game_state = {}
        self.message_list = []
        self.clients = {}
        self.rooms = []
        self.places = []
        self.reciever_address = settings.MARKER_ALL

        self.LOGGIN = '1'
        self.MAIN = '2'
        self.GAME = '3'
        self.state = settings.LOGGIN

    def gui_set_cards(self, x, y, card):
        label_Player_card = QtWidgets.QLabel(application.ui.groupBox_Game)
        label_Player_card.setGeometry(QtCore.QRect(x, y, 30, 50))
        label_Player_card.setPixmap(QtGui.QPixmap(f"{settings.PIC_PATH}{card}.png"))
        label_Player_card.setScaledContents(True)
        label_Player_card.setObjectName('label_Player_card')
        label_Player_card.show()

    def show_game_result(self):
        self.clear_form()
        result = QMessageBox()
        result.setWindowTitle('result')
        result.setText(f"YOU {self.game_state[self.login_player]}")
        x = result.exec_()

    def clear_form(self):
        self.p.setColor(self.backgroundRole(), QtCore.Qt.gray)
        self.setPalette(self.p)
        for label in self.ui.groupBox_Game.findChildren(QtWidgets.QLabel, "label_Player_card"):
            label.deleteLater()

    def draw_hand(self):
        for label in self.ui.groupBox_Game.findChildren(QtWidgets.QLabel, "label_Player_card"):
            label.deleteLater()
        x = 20
        hand = self.game_state[self.places[0]][0].split('~')
        for card in hand:
            self.gui_set_cards(x, 400, card)
            x += 15
        x = 300
        hand = self.game_state[self.places[1]][0].split('~')
        for card in hand:
            self.gui_set_cards(x, 220, card)
            x += 15
        x = 570
        hand = self.game_state[self.places[2]][0].split('~')
        for card in hand:
            self.gui_set_cards(x, 360, card)
            x += 15
        x = 280
        hand = self.game_state[self.login_player][0].split('~')
        for card in hand:
            self.gui_set_cards(x, 350, card)
            x += 15

    def take_card(self):
        message = {settings.MODE_KEY: settings.GAME,
                   settings.LOGIN_KEY: self.login_player, settings.MOVE_KEY: settings.TAKE}
        self.send_to_server(message)

    def pass_and_turn(self):
        message = {settings.MODE_KEY: settings.GAME,
                   settings.LOGIN_KEY: self.login_player, settings.MOVE_KEY: settings.ENOUGH}
        self.send_to_server(message)

    def refresh_game_state(self):
        self.draw_hand()
        if self.game_state[self.login_player][2] == 1:
            self.ui.pushButton_take.setVisible(True)
            self.ui.pushButton_enough.setVisible(True)
        else:
            self.ui.pushButton_take.setVisible(False)
            self.ui.pushButton_enough.setVisible(False)

    def make_bet(self):
        bet = int(application.ui.lineEdit_bet.text())
        if bet < self.cash and self.game_state != {}:
            message = {settings.MODE_KEY: settings.MODE_BET,
                       settings.LOGIN_KEY: self.login_player, settings.BET_KEY: bet}
            self.send_to_server(message)

    def start_game(self):
        try:
            if len(self.places) == 3:
                message = {settings.MODE_KEY: settings.MODE_START,
                           settings.LOGIN_KEY: self.login_player}
                self.send_to_server(message)
        except:
            pass

    def send_text_message(self):
        message = {settings.MODE_KEY: settings.MODE_COMMON, settings.LOGIN_KEY: self.login_player,
                   settings.MESSAGE_KEY: self.ui.lineEdit_message.text()}
        self.send_to_server(message)

    def join_room(self):
        message = {settings.MODE_KEY: settings.MODE_JOIN_GAME, settings.LOGIN_KEY:
                   str(application.ui.comboBox_rooms.currentText()), settings.PASSWORD_KEY: self.ui.lineEdit_gamepassword.text()}
        self.send_to_server(message)

    def create_room(self):
        message = {settings.MODE_KEY: settings.MODE_CREATE_GAME, settings.LOGIN_KEY:
                   application.ui.lineEdit_gamename.text(), settings.PASSWORD_KEY: self.ui.lineEdit_gamepassword.text()}
        self.send_to_server(message)

    def refresh_main_ui(self):
        self.ui.label_money.setText(f"{self.cash}")
        self.ui.comboBox_rooms.clear()
        self.ui.comboBox_rooms.addItems(self.rooms)

    def refresh_game_ui(self):
        try:
            self.ui.label_player1.setText(self.places[0])
            self.ui.label_player2.setText(self.places[1])
            self.ui.label_player3.setText(self.places[2])
        except:
            pass

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

    def process_request(self, message):
        try:
            mode = message[settings.MODE_KEY]
        except KeyError:
            return False

        if mode == settings.MODE_CONNECT:
            if message[settings.RESULT_KEY] == settings.SUCCESS:
                self.state = settings.MAIN
                self.cash = message[settings.CASH_KEY]
                self.set_form(True, False, False)
                self.confugure_entry_form()
                return True
            else:
                self.TCPSocket.disconnect(self.login_player)

        if mode == settings.MODE_REGISTER:
            if message[settings.RESULT_KEY] == settings.SUCCESS:
                self.state = settings.MAIN
                self.cash = message[settings.CASH_KEY]
                self.set_form(True, False, False)
                self.confugure_entry_form()
                return True
            else:
                self.TCPSocket.disconnect(self.login_player)

        if mode == settings.MODE_DISCONNECT:
            return True

        if mode == settings.MODE_DONATE:
            self.cash = message[settings.CASH_KEY]
            self.refresh_main_ui()
            return True

        if mode == settings.MODE_CREATE_GAME or mode == settings.MODE_JOIN_GAME:
            self.state = settings.GAME
            self.ui.pushButton_take.setVisible(False)
            self.ui.pushButton_enough.setVisible(False)

            if message[settings.RESULT_KEY] == settings.SUCCESS:
                self.set_form(False, False, True)
            if mode == settings.MODE_JOIN_GAME:
                self.ui.pushButton_start.setVisible(False)
            return True

        if mode == settings.MODE_ROOMS:
            self.rooms = message[settings.ROOMS_KEY]
            if self.state == settings.MAIN:
                self.refresh_main_ui()
            return True

        if mode == settings.MODE_COMMON:
            if self.state == settings.GAME and message[settings.LOGIN_KEY] != self.login_player:
                self.append_message(message)
            return True

        if mode == settings.MODE_PLAYERS:
            if self.state == settings.GAME:
                self.confugure_game_form(message)
                self.refresh_game_ui()
            return True

        if mode == settings.MODE_START:
            print(message)
            self.p.setColor(self.backgroundRole(), QtCore.Qt.black)
            self.setPalette(self.p)
            self.game_state = message[settings.MESSAGE_KEY]
            self.draw_hand()
            return True

        if mode == settings.GAME:
            self.game_state = message[settings.MESSAGE_KEY]
            self.refresh_game_state()

        if mode == settings.MODE_GAME_RESULT:
            self.game_state = message[settings.MESSAGE_KEY]
            self.p.setColor(self.backgroundRole(), QtCore.Qt.gray)
            self.setPalette(self.p)
            self.show_game_result()

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

    def append_message(self, message):
        try:
            if message[settings.LOGIN_KEY] == self.places[0]:
                self.ui.label_message1.setText(message[settings.MESSAGE_KEY])
            if message[settings.LOGIN_KEY] == self.places[1]:
                self.ui.label_message2.setText(message[settings.MESSAGE_KEY])
            if message[settings.LOGIN_KEY] == self.places[2]:
                self.ui.label_message3.setText(message[settings.MESSAGE_KEY])
        except:
            pass

    def set_form(self, enterState, loginState, gameState):
        self.ui.groupBox_Enter.setVisible(enterState)
        self.ui.groupBox_LogIn.setVisible(loginState)
        self.ui.groupBox_Game.setVisible(gameState)

    def confugure_entry_form(self):
        self.ui.label_money.setText(f"{self.cash}")

    def confugure_game_form(self, info):
        self.places.clear()
        if info[settings.ADMIN_KEY] == self.login_player:
            self.places = info[settings.PLAYERS_KEY]
            self.refresh_game_ui()
        elif self.login_player in info[settings.PLAYERS_KEY]:
            info[settings.PLAYERS_KEY].remove(self.login_player)
            self.places.append(info[settings.ADMIN_KEY])
            self.places += info[settings.PLAYERS_KEY]
            self.refresh_game_ui()
        return True

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
    application.ui.pushButton_choosegame.clicked.connect(application.join_room)
    application.ui.pushButton_send.clicked.connect(application.send_text_message)
    application.ui.pushButton_start.clicked.connect(application.start_game)
    application.ui.pushButton.clicked.connect(application.make_bet)
    application.ui.pushButton_take.clicked.connect(application.take_card)
    application.ui.pushButton_enough.clicked.connect(application.pass_and_turn)

    sys.exit(app.exec_())
