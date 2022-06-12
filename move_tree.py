class MovesTree:

    def __init__(self):
        self.root = None
        self.chosen_move = None

    def set_root_move(self, input_root):
        self.root = input_root

    def get_root(self):
        return self.root

    def add_move(self, move):
        if self.chosen_move is None:
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
        else:
            self.chosen_move

class Move:

    def __init__(self, input_list_of_squares, input_figure, input_board=None):
        self.data = input_list_of_squares
        self.children = []
        self.board_state = input_board  # This attrib is here only for simulating trees further (AI, jump_moves)
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

    def add_parent(self, parent):
        if (self.parent is not None and
           self.parent != parent):
            return
        self.parent = parent
        parent.add_child(self)

    def force_birth(self, position):
        offspring = Move([self.data[-1], position], self.figure, self.board_state)
        self.children.append(offspring)
        offspring.set_parent(self)
        return offspring

    def get_data(self):
        return self.data

    def get_children(self):
        return self.children


# ------------------------------------------------

def get_moves(tree: MovesTree):
    def rec_get_moves(move: Move, list_of_moves, list_copy=[]):
        '''
        Recursively called to get all possible moves from root to leaf.
        Takes on input:
        move ...            a Move object
        list_of_moves ...   a list to be filled with all possible root-leaf moves
        list_copy ...       a copy of current Move's list, it is given to a child after current Move's list updates
        '''
        # if it is a first Move, begin list_copy with it, add self data afterwards
        list_copy.append(move.get_data()[1])

        # if it is a leaf Move, complete current list of squares
        if len(move.get_children()) == 0:
            list_of_moves.append(list_copy)
            return

        # otherwise recursively call itself doing this:
        # 1) copy list_of_moves, which was given to list_copy argument
        # 2) send copy of list_of_moves to all children
        # 3) children recursively update their copies
        for child in move.children:
            list_for_child = list_copy.copy()
            rec_get_moves(child, list_of_moves, list_for_child)

    # short output for empty trees
    if tree.get_root() is None:
        return []

    # creating main list of moves
    list_of_moves = []

    # filling the list
    rec_get_moves(tree.root, list_of_moves)
    for move in list_of_moves:
        move.insert(0, tree.root.data[0])

    # outputing the list
    return list_of_moves