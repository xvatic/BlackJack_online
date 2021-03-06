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
        self.game_states = {}
        self.decks = {}

        self.STATE = settings.LOGGIN

        self.signal = New_message_event_handle()
        self.signal.new_message_serv.connect(self.new_message_serv)

    def append_message_to_server_log(message):
        self.ui.textEdit_server_log.append(f'{message_converted} {address}')
        final_message = self.serialize(final_message)

    def send_game_state(self, room):
        message = {settings.MODE_KEY: settings.GAME, settings.MESSAGE_KEY: self.game_states[room]}
        self.send_to_room_participants(message, room)

    def update_players_cash(self, room):
        for key in self.game_states[room]:
            if key != settings.DECK_POS_KEY and key != settings.DEALER_KEY:
                if self.game_states[room][key][0] == settings.WIN:
                    self.database.inc_players_cash(self.game_states[room][key][1], key)
                elif self.game_states[room][key][0] == settings.LOSS:
                    self.database.dec_players_cash(self.game_states[room][key][1], key)

    def send_game_result(self, room):
        message = {settings.MODE_KEY: settings.MODE_GAME_RESULT,
                   settings.MESSAGE_KEY: self.game_states[room]}
        self.send_to_room_participants(message, room)

    def send_players_cash(self, room):
        for client_value, address_value in self.clients.items():
            if address_value == self.rooms[room][settings.ADMIN_KEY] or address_value in self.rooms[room][settings.PLAYERS_KEY]:
                login = self.client_info[address_value]
                message = {settings.MODE_KEY: settings.MODE_DONATE,
                           settings.CASH_KEY: self.database.get_cash(login)}
                client_value.send(self.serialize(message))

    def get_player_room(self, client_id):
        for key in self.rooms:
            if self.rooms[key][settings.ADMIN_KEY] == client_id or client_id in self.rooms[key][settings.PLAYERS_KEY]:
                return key

    def send_text_message(self, message, client_id):
        for key in self.rooms:
            if self.rooms[key][settings.ADMIN_KEY] == client_id or client_id in self.rooms[key][settings.PLAYERS_KEY]:
                for client_value, address_value in self.clients.items():
                    if address_value == self.rooms[key][settings.ADMIN_KEY] or address_value in self.rooms[key][settings.PLAYERS_KEY]:
                        client_value.send(self.serialize(message))

    def refresh_room_info(self, client_id):
        if client_id not in self.rooms.keys():
            for key in self.rooms:
                if self.rooms[key][settings.ADMIN_KEY] == client_id or client_id in self.rooms[key][settings.PLAYERS_KEY]:
                    players = []
                    for id in self.rooms[key][settings.PLAYERS_KEY]:
                        players.append(self.client_info[id])
                    message = {settings.MODE_KEY: settings.MODE_PLAYERS, settings.ADMIN_KEY:
                               self.client_info[self.rooms[key][settings.ADMIN_KEY]], settings.PLAYERS_KEY: players}
                    for client_value, address_value in self.clients.items():
                        if address_value == self.rooms[key][settings.ADMIN_KEY] or address_value in self.rooms[key][settings.PLAYERS_KEY]:
                            client_value.send(self.serialize(message))
        elif client_id in self.rooms.keys():
            players = []
            for id in self.rooms[client_id][settings.PLAYERS_KEY]:
                players.append(self.client_info[id])
            message = {settings.MODE_KEY: settings.MODE_PLAYERS, settings.ADMIN_KEY:
                       self.client_info[self.rooms[client_id][settings.ADMIN_KEY]], settings.PLAYERS_KEY: players}
            for client_value, address_value in self.clients.items():
                if address_value == self.rooms[client_id][settings.ADMIN_KEY] or address_value in self.rooms[client_id][settings.PLAYERS_KEY]:
                    client_value.send(self.serialize(message))

    def refresh_rooms(self):
        if len(self.rooms) != 0:
            message = {settings.MODE_KEY: settings.MODE_ROOMS, settings.ROOMS_KEY: []}
            for key in self.rooms:
                if len(self.rooms[key][settings.PLAYERS_KEY]) < 3:
                    message[settings.ROOMS_KEY].append(key)
            for client_value, address_value in self.clients.items():
                client_value.send(self.serialize(message))
        else:
            message = {settings.MODE_KEY: settings.MODE_ROOMS, settings.ROOMS_KEY: []}
            for client_value, address_value in self.clients.items():
                client_value.send(self.serialize(message))

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

                self.refresh_rooms()
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

                self.refresh_rooms()

                return True
            else:
                message = {settings.MODE_KEY: settings.MODE_REGISTER,
                           settings.RESULT_KEY: settings.FAIL}
                connection.send(self.serialize(message))
                return True
        if mode == settings.MODE_DISCONNECT:
            self.clients.pop(connection)

        if mode == settings.MODE_DONATE:
            if self.database.check_promocode(data[settings.CODE_KEY], login) == True:
                cash = self.database.get_cash(login)
                message = {settings.MODE_KEY: settings.MODE_DONATE, settings.CASH_KEY: cash}
                connection.send(self.serialize(message))
                return True

        if mode == settings.MODE_CREATE_GAME:
            client_id, client_ip = str(address[1]), address[0]
            if data[settings.LOGIN_KEY] not in self.rooms.keys():
                self.rooms[data[settings.LOGIN_KEY]] = {
                    settings.PASSWORD_KEY: data[settings.PASSWORD_KEY], settings.ADMIN_KEY: client_id, settings.PLAYERS_KEY: []}
                message = {settings.MODE_KEY: settings.MODE_CREATE_GAME,
                           settings.RESULT_KEY: settings.SUCCESS}
                time.sleep(0.2)
                connection.send(self.serialize(message))
                self.refresh_rooms()
                self.refresh_room_info(client_id)
            else:
                message = {settings.MODE_KEY: settings.MODE_CREATE_GAME,
                           settings.RESULT_KEY: settings.FAIL}
                connection.send(self.serialize(message))
            return True

        if mode == settings.MODE_JOIN_GAME:
            client_id, client_ip = str(address[1]), address[0]
            if data[settings.LOGIN_KEY] in self.rooms.keys():
                if self.rooms[data[settings.LOGIN_KEY]][settings.PASSWORD_KEY] == data[settings.PASSWORD_KEY]:
                    self.rooms[data[settings.LOGIN_KEY]][settings.PLAYERS_KEY].append(client_id)
                    message = {settings.MODE_KEY: settings.MODE_JOIN_GAME,
                               settings.RESULT_KEY: settings.SUCCESS}

                    connection.send(self.serialize(message))
                    self.refresh_rooms()
                    time.sleep(1)
                    self.refresh_room_info(client_id)

            else:
                message = {settings.MODE_KEY: settings.MODE_JOIN_GAME,
                           settings.RESULT_KEY: settings.FAIL}
                connection.send(self.serialize(message))
            return True

        if mode == settings.MODE_LEAVE_GAME:
            client_id, client_ip = str(address[1]), address[0]
            room = self.get_player_room(client_id)
            if self.rooms[room][settings.ADMIN_KEY] == client_id:
                message = {settings.MODE_KEY: settings.MODE_CLOSE_GAME}
                self.send_to_room_participants(message, room)
                self.send_players_cash(room)
                self.rooms.pop(room)
                self.refresh_rooms()
            elif client_id in self.rooms[room][settings.PLAYERS_KEY]:
                self.rooms[room][settings.PLAYERS_KEY].remove(client_id)
                login = self.client_info[client_id]
                message = {settings.MODE_KEY: settings.MODE_DONATE,
                           settings.CASH_KEY: self.database.get_cash(login)}
                connection.send(self.serialize(message))
                self.refresh_rooms()
                time.sleep(1)
                self.refresh_room_info(room)

            return True

        if mode == settings.MODE_START:
            client_id, client_ip = str(address[1]), address[0]
            room = self.get_player_room(client_id)
            self.decks[room] = self.game.generate_deck(room)
            admin = self.client_info[self.rooms[room][settings.ADMIN_KEY]]
            player1 = self.client_info[self.rooms[room][settings.PLAYERS_KEY][0]]
            player2 = self.client_info[self.rooms[room][settings.PLAYERS_KEY][1]]
            player3 = self.client_info[self.rooms[room][settings.PLAYERS_KEY][2]]
            places = [admin, player1, player2, player3]
            hand = []
            self.game_states[room] = {admin: ['', 0, 0], player1: ['', 0, 0], player2: [
                '', 0, 0], player3: ['', 0, 0], settings.DEALER_KEY: 0, settings.DECK_POS_KEY: 8}

            self.game_states[room] = self.game.deal_starting_cards(
                self.decks[room], self.game_states[room], places)

            message = {settings.MODE_KEY: settings.MODE_START,
                       settings.MESSAGE_KEY: self.game_states[room]}
            self.send_to_room_participants(message, room)
            return True

        if mode == settings.MODE_BET:
            client_id, client_ip = str(address[1]), address[0]
            room = self.get_player_room(client_id)
            self.game_states[room] = self.game.set_bet(data, self.game_states[room])
            self.send_game_state(room)
            return True

        if mode == settings.GAME:
            client_id, client_ip = str(address[1]), address[0]
            room = self.get_player_room(client_id)
            self.game_states[room] = self.game.process_move(
                data, self.game_states[room], self.decks[room])
            if self.game_states[room][settings.DEALER_KEY] > 0:
                self.update_players_cash(room)
                self.send_game_result(room)
                self.game_states.pop(room)
            else:
                self.send_game_state(room)

        if mode == settings.MODE_COMMON:
            client_id, client_ip = str(address[1]), address[0]
            self.send_text_message(data, client_id)
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

        if self.process_request(processed_data, connection, address) == True:
            return

    def send_to_client(self, message, reciever, connection):
        for client_value, address_value in self.clients.items():
            if connection != client_value:
                if address_value == reciever:
                    client_value.send(message)
                elif reciever == settings.MARKER_ALL:
                    client_value.send(message)

    def send_to_room_participants(self, message, room):
        for client_value, address_value in self.clients.items():
            if self.rooms[room][settings.ADMIN_KEY] == address_value or address_value in self.rooms[room][settings.PLAYERS_KEY]:
                client_value.send(self.serialize(message))

    def set_tcp_socket(self, socket):
        self.TCPSocket_app = socket

    def set_database_connection(self, database):
        self.database = database

    def set_game_logic(self, game):
        self.game = game

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
    from game import Game
    from database_interaction import Users
    HOST = socket.gethostbyname('localhost')
    PORT = 12345

    app = QtWidgets.QApplication(sys.argv)
    application = Window()
    application.show()

    info = Users()
    info.check_database_existing()
    game = Game()
    application.set_database_connection(info)
    application.set_game_logic(game)

    TCPSocket = TCPTools(application.signal.new_message_serv)
    TCPSocket.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPSocket.socket.bind((HOST, PORT))
    TCPSocket.socket.listen(10)
    TCPSocket.set_server_flag()
    application.set_tcp_socket(TCPSocket)
    application.start()

    sys.exit(app.exec_())
