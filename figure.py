from move_tree import MovesTree
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
        self._game = None # NUTNO PREPSAT NA NONE, JEN PRO DEBUGGING JE TU Game()
        self.moves_tree = MovesTree()

    def show(self):
        print(f"{self._position} {self._color} {self._status} {self._label}")

    def position(self):
        return self._position

    def label(self):
        return self._label

    def set_game(self, game):
        self._game = game

    def update_possible_moves(self):
        assert self._game is not None
        self._game.validator.find_all_valid_moves(self._game)