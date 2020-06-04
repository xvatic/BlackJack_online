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

    def dealer(self, pos, deck):
        score = 0
        while score < settings.MAX_DEALER_SCORE:
            score += settings.RANK[deck[pos][1]]
            pos += 1
        return score

    def get_result(self, state, deck):
        state[settings.DEALER_KEY] = self.dealer(state[settings.DECK_POS_KEY], deck)
        for key in state:
            if key != settings.DEALER_KEY and key != settings.DECK_POS_KEY:
                if state[settings.DEALER_KEY] > 21 and self.count_score(state[key][0]) <= settings.MAX_SCORE:
                    state[key][0] = settings.WIN
                    continue
                if self.count_score(state[key][0]) > state[settings.DEALER_KEY] and self.count_score(state[key][0]) <= settings.MAX_SCORE:
                    state[key][0] = settings.WIN
                    continue
                elif self.count_score(state[key][0]) == state[settings.DEALER_KEY] and self.count_score(state[key][0]) <= settings.MAX_SCORE:
                    state[key][0] = settings.DRAW
                    continue
                else:
                    state[key][0] = settings.LOSS
                    continue
        return state

    def check_bet(self, state):
        for key in state:
            if key != settings.DEALER_KEY and key != settings.DECK_POS_KEY:
                if state[key][1] == 0:
                    return False
        return True

    def count_score(self, hand):
        hand = hand.split('~')
        score = 0
        for card in hand:
            score += settings.RANK[card[1]]
        return score

    def get_score(self, state, login):
        hand = state[login][0].split('~')
        score = 0
        for card in hand:
            score += settings.RANK[card[1]]
        if score >= settings.MAX_SCORE:
            return True
        else:
            return False

    def switch_turn(self, state):
        for key in state:
            if key != settings.DEALER_KEY and key != settings.DECK_POS_KEY:
                if state[key][2] == 0 or state[key][2] == 1:
                    state[key][2] = 1
                    return state, True

        return state, False

    def deal_starting_cards(self, deck, state, places):
        i = 0
        for key in state:
            if key != settings.DEALER_KEY and key != settings.DECK_POS_KEY:
                state[key][0] = f"{deck[i]}~{deck[i+1]}"
                i += 2
        return state

    def set_bet(self, message, state):
        player = message[settings.LOGIN_KEY]
        state[player][1] = message[settings.BET_KEY]
        if self.check_bet(state) == True:
            for key in state:
                state[key][2] = 1
                return state
        return state

    def process_move(self, move, state, deck):
        if move[settings.MOVE_KEY] == settings.TAKE:
            pos = state[settings.DECK_POS_KEY]
            state[move[settings.LOGIN_KEY]][0] += f"~{deck[pos]}"
            state[settings.DECK_POS_KEY] += 1
            state[move[settings.LOGIN_KEY]][2] = 1
            if self.get_score(state, move[settings.LOGIN_KEY]) == True:
                state[move[settings.LOGIN_KEY]][2] = 2
                state, marker = self.switch_turn(state)
                if marker == False:
                    state = self.get_result(state, deck)
            return state

        if move[settings.MOVE_KEY] == settings.ENOUGH:
            state[move[settings.LOGIN_KEY]][2] = 2
            state, marker = self.switch_turn(state)
            if marker == False:
                state = self.get_result(state, deck)
            return state

    def generate_deck(self, room):
        deck = settings.CARDS
        random.shuffle(deck)
        return deck
