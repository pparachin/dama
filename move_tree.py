from multiprocessing.reduction import duplicate


class MovesTree:

    def __init__(self):
        self.root = None
        self.chosen_move = None

    def set_root_move(self, input_root):
        self.root = input_root

    def get_root(self):
        return self.root

    def add_move(self, move):
        if self.chosen_move is not None:
            self.chosen_move.add_child(move)
        else:
            self.root.add_child(move)
        
    def set_chosen_move(self, input_move):
        self.chosen_move = input_move

    def get_move_by_data(self, input_data):
        if self.root.data == input_data:
            return self.root
        else:
            for child in self.root.children:
                if child.data == input_data:
                    return child
                else:
                    return child.get_move_by_data(input_data)

class Move:

    def __init__(self, input_list_of_squares, input_figure, input_board=None):
        self.data = input_list_of_squares
        self.children = []
        self.board_state = input_board  # This attrib is here only for simulating trees further (AI, jump_moves)
        self.figure = input_figure
        self.parent = None

    def look_for_chosen_move(self, pattern):
        for child in self.children:
            if child is pattern:
                return child
            else:
                return child.look_for_choosen_move(pattern)
        return None

    def get_move_by_data(self, input_data):
        if self.data == input_data:
            return self
        else:
            for child in self.children:
                if child.data == input_data:
                    return child
                else:
                    return child.get_move_by_data(input_data)

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

    def get_all_submoves(self):
        output = []
        if self not in output:
            output.append(self)
        for child in self.children:
            for submove in child.get_all_submoves():
                output.append(submove)
        return output

    def add_child(self, move):
        # looking for longest branch of moves
        its_children_have_no_children = False
        for child in self.children:
            if child.get_children() != []:
                its_children_have_no_children = False
                break
        if self.children == [] or its_children_have_no_children:

            # if textual interpretation of move is same as potential parent's or siblings'
            # then this function will refuse to add it
            is_not_duplicate = True
            if self.data == move.get_data():
                is_not_duplicate = False
            for child in self.children:
                if child.get_data() == move.get_data():
                    is_not_duplicate = False

            # every move in moves_tree has to start on the same tile as parents ended on
            if self.data[-1] == move.get_data()[0] and is_not_duplicate:
                self.children.append(move)
                move.set_parent(self)

        else:
            for child in self.children:
                child.add_child(move)

    def force_birth(self, position):
        offspring = Move([self.data[-1], position], self.figure, self.board_state)
        self.children.append(offspring)
        offspring.set_parent(self)
        return offspring

    def set_siblings(self, list_of_siblings, input_figure):
        if self.parent is None:
            return None
        else:
            for sibling in list_of_siblings:
                duplicate = False
                temp_move_object = Move(sibling, input_figure)
                for child in self.parent.children:
                    if child.get_data() == sibling:
                        duplicate = True
                if not duplicate:
                    self.parent.children.append(temp_move_object)

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