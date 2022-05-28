class MovesTree():


    def __init__(self):
        self.root = None


    def set_root_move(self, Move):
        self.root = Move


class Move():


    def __init__(self, start, end):
        self.data = [start, end]
        self.parent = None
        self.children = []
        self.figure = None
        self.friends = None
        self.enemies = None


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