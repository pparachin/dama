class MovesTree():


    def __init__(self):
        self.root = None


    def set_root_move(self, Move):
        self.root = Move


    def get_root(self):
        return self.root


class Move():


    def __init__(self, start, end, input_figure, input_board=None):
        self.data = [start, end]
        self.children = []
        self.board_state = input_board
        self.figure = input_figure
        self.parent = None
        self.friends = None
        self.enemies = None
        self.update_friends_and_foes()

    def add_step(self, position):
        self.data.append(position)

 
    def set_figure(self, input_figure):
        self.figure = input_figure


    def set_parent(self, input_parent):
        self.parent = input_parent

    
    def force_birth(self, position):
        offspring = Move(self._data[-1], position)
        self.children.append(offspring)
        offspring.set_parent(self)
        return offspring


    def update_friends_and_foes(self):
        if self.figure in ['w', 'ww']:
            self.friends = ['w', 'ww']
            self.enemies = ['b', 'bb']
        elif self.figure in ['b', 'bb']:
            self.friends = ['b', 'bb']
            self.enemies = ['w', 'ww']

    
    def get_children(self):
        return self.children