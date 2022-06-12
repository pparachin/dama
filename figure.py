from move_tree import *

from alias import *


class Figure:

    # Position = aktuální pozice figurky
    # Color = barva figurky
    # Status = zda je figurka stále na desce nebo byla odebrána
    # Label = název figurky

    def __init__(self, position, color, status, label):
        self._position = position
        self._color = color
        self._status = status
        self._label = label
        self.moves_tree = MovesTree()

        initial_move = Move([self._position, self._position], self)
        self.moves_tree.set_root_move(initial_move)
        self.moves_tree.set_chosen_move(initial_move)

    def show(self):
        print(f"{self._position} {self._color} {self._status} {self._label}")

    def get_position(self):
        return self._position

    def get_label(self):
        return self._label

    def set_position(self, position):
        self._position = position

    def set_label(self, newlabel):
        self._label = newlabel