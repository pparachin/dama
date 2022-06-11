class MovesTree():


    def __init__(self):
        self.root = None


    def set_root_move(self, move):
        self.root = move


    def get_root(self):
        return self.root

    def add_move(self, move):
        temp_move = self.root
        can_continue = True
        while can_continue:
            for child in temp_move.children:
                if child.children:
                    can_continue = True
                    temp_move = child
                    continue
            can_continue = False
        temp_move.children.append(move)


class Move():


    def __init__(self, input_list_of_squares, input_figure, input_board=None):
        self.data = input_list_of_squares
        self.children = []
        self.board_state = input_board # This attrib is here only for simulating trees further (AI, jump_moves)
        self.figure = input_figure
        self.parent = None

    def add_step(self, position):
        self.data.append(position)
 
    def set_figure(self, input_figure):
        self.figure = input_figure

    def get_figure(self):
        return self.figure

    def set_parent(self, input_parent):
        self.parent = input_parent
    
    def force_birth(self, position):
        offspring = Move(self._data[-1], position)
        self.children.append(offspring)
        offspring.set_parent(self)
        return offspring
    
    def get_children(self):
        return self.children