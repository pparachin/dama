from validator import Validator
from game import Game
from alias import *


class Figure:

    # Position = aktuální pozice figurky
    # Color = barva figurky
    # Status = zda je figurka stále na desce nebo byla odebrána
    # Label = název figurky

    def __init__(self, position, color, status, label, advantage):
        self._position = position
        self._color = color
        self._status = status
        self._label = label
        self._advantage = advantage
        self._game = Game() # NUTNO PREPSAT NA NONE, JEN PRO DEBUGGING JE TU Game()

    def show(self):
        print(f"{self._position} {self._color} {self._status} {self._label}")

    def position(self):
        return self._position

    def label(self):
        return self._label

    def set_game(self, game):
        self._game = game

    def get_possible_moves(self):
        assert self._game is not None

        player_color = PlayerColor.WHITE if self._color == StoneColor.WHITE else StoneColor.BLACK
        for move in self._game.validator.find_all_valid_moves(self._game.game_field, self._game.get_player_to_turn):
            pass # DOES NOT WORK RN, VALIDATOR HAS TO BE CHANGED TO OPERATE WITH OBJECTS, NOT STRINGS