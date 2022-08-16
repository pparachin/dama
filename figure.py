from move_tree import *


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

    def get_status(self):
        return self._status

    def get_color(self):
        return self._color

    def get_label(self):
        return self._label

    def print_move_tree(self):
        print(get_moves(self.moves_tree))

    def set_position(self, position):
        self._position = position

    def set_label(self, newlabel):
        self._label = newlabel

    def get_move_by_data(self, input_move):
        return self.moves_tree.get_move_by_data(input_move)

    def set_as_chosen_move_in_tree(self, input_move):
        self.moves_tree.set_chosen_move(input_move)

    def add_to_move_tree(self, input_move):
        self.moves_tree.add_move(input_move)

    def __repr__(self):
        return self._label

    # spravne pythonovsky takhle:
    '''
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        self._position = value
    '''