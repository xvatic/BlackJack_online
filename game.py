import time
from PyQt5 import QtCore, QtWidgets
from time import localtime, strftime
import pickle
import settings
import random


class Game(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.login = ''
        self.password = ''
        self.server_flag = False

    def dealer(self):
        pass

    def deal_starting_cards(self, deck, state):
        i = 0
        for key, parameters in state.items():
            parameters[settings.HAND_KEY].append(deck[i])
            parameters[settings.HAND_KEY].append(deck[i+1])
            continue
            i += 2
        return state

    def generate_deck(self, room):
        deck = settings.CARDS
        random.shuffle(deck)
        return deck
