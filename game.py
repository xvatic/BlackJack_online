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
        buf = []
        i = 0
        for key in state:
            if key != settings.DEALER_KEY and key != settings.DECK_POS_KEY:
                buf.append(deck[i])
                buf.append(deck[i+1])
                state[key][settings.HAND_KEY] = buf
                i += 2
        return state

    def generate_deck(self, room):
        deck = settings.CARDS
        random.shuffle(deck)
        return deck
