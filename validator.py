# general modules
import copy

# our modules
from alias import *
from move_tree import *
from stone import Stone
from lady import Lady


class Validator():

    def __init__(self):
        ...

    @staticmethod
    def get_sq_string_from_2D_board(row, col):
        output = None
        number_list = ['8', '7', '6', '5', '4', '3', '2', '1']
        if (0 <= row <= 7) and (0 <= col <= 7):
            letter = chr((97 + col))
            number = number_list[row]
            output = letter + number

        return output

    @staticmethod
    def get_rowcol_from_sq_string(sq_string):
        output = None
        number_list = [7, 6, 5, 4, 3, 2, 1, 0]
        column = int(ord(sq_string[0])) - 97
        row_index = int(sq_string[1]) - 1
        row = number_list[row_index]
        output = (row, column)

        return output

    @staticmethod
    def old_generate_game_field(game_file_path):
        """
        This function opens .csv file and outputs corresponding "game field dictionary".
        !!! Note: This function does NOT validate if the text inside file is correct. !!!
        """
        playing_field = {}
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for letter in letters:
            for number in range(1, 9):
                tag = str(letter) + str(number)
                playing_field[tag] = None

        # putting figures in
        try:
            with open(game_file_path) as game_file:
                game_file_contents = game_file.read().splitlines()
                for line in game_file_contents:
                    playing_field[line[0:2]] = line[3:]
                game_file.close()
                output = []
        except FileNotFoundError:
            output = None

        return playing_field

    def game_field_to2D(self, field):
        board = []
        for dimension in range(8):
            board.append(["-", "-", "-", "-", "-", "-", "-", "-", ])

        for sq in range(len(field)):
            row = self.get_rowcol_from_sq_string(list(field.keys())[sq])[0]
            col = self.get_rowcol_from_sq_string(list(field.keys())[sq])[1]
            if list(field.values())[sq] is not None:
                board[row][col] = list(field.values())[sq]

        return board


    def translate_GUI_board_to_Validator_board(self, gui_board):
        output = self.generate_empty_field()
        for row in range(len(gui_board)):
            for column in range(len(gui_board[row])):
                sq = self.get_sq_string_from_2D_board(row, column)
                if gui_board[row][column] == "-":
                    output[sq] = None
                else:
                    output[sq] = gui_board[row][column]
        return output

    @staticmethod
    def validate_base_setup(game_file_path):
        """
        returns 0 if input file path leads to .csv file containing correct setup for Czech dama
        returns 1 for incorrect game setup
        returns 2 for errors connected with reading the file, e.g.: incorrect path
        """
        assert isinstance(game_file_path, str)

        base_setups = [["a1,w",
                        "a3,w",
                        "a7,b",
                        "b2,w",
                        "b6,b",
                        "b8,b",
                        "c1,w",
                        "c3,w",
                        "c7,b",
                        "d2,w",
                        "d6,b",
                        "d8,b",
                        "e1,w",
                        "e3,w",
                        "e7,b",
                        "f2,w",
                        "f6,b",
                        "f8,b",
                        "g1,w",
                        "g3,w",
                        "g7,b",
                        "h2,w",
                        "h6,b",
                        "h8,b"],
                       ["a1,b",
                        "a3,b",
                        "a7,w",
                        "b2,b",
                        "b6,w",
                        "b8,w",
                        "c1,b",
                        "c3,b",
                        "c7,w",
                        "d2,b",
                        "d6,w",
                        "d8,w",
                        "e1,b",
                        "e3,b",
                        "e7,w",
                        "f2,b",
                        "f6,w",
                        "f8,w",
                        "g1,b",
                        "g3,b",
                        "g7,w",
                        "h2,b",
                        "h6,w",
                        "h8,w"]]

        output = None
        try:
            with open(game_file_path) as game_file:
                game_file_contents = game_file.read().splitlines()

                setup_v1 = None
                setup_v2 = None

                for valid_line in base_setups[0]:
                    if valid_line not in game_file_contents:
                        setup_v1 = False
                        break
                    setup_v1 = True

                for valid_line in base_setups[1]:
                    if valid_line not in game_file_contents:
                        setup_v2 = False
                        break
                    setup_v2 = True

                if setup_v1:
                    for line in game_file_contents:
                        if line not in base_setups[0]:
                            output = 1
                            break
                    output = 0

                # This section was commented out due to setup_v2 NOT being 
                # allowed by http://damweb.cz/pravidla/cdfull.html rules.
                #
                # elif setup_v2:
                #     for line in game_file_contents:
                #         if line not in base_setups[1]:
                #             output = 1
                #             break
                #     output = 0

                else:
                    output = 1

                game_file.close()

        except FileNotFoundError:
            output = 2

        return output

    @staticmethod
    def get_move_direction(move):
        """
        Takes simple move on input (that means a list of squares, only consideres first and last).
        Returns string representing direction (ne/nw/se/sw) according to correct board position where:
        a1 is bottom left corner
        a8 is top left corner
        h8 is top right corner
        h1 is bottom right corner
        """
        output, up, right = None, None, None

        if ord(move[0][0]) < ord(move[1][0]):
            right = True
        else:
            right = False

        if int(move[0][1]) < int(move[1][1]):
            up = True
        else:
            up = False

        if up and right:
            output = 'ne'
        elif up and not right:
            output = 'nw'
        elif not up and right:
            output = 'se'
        elif not up and not right:
            output = 'sw'

        return output

    def span(self, move, direction=None):
        """
        Takes simple move on input (that means a list of squares, only consideres first and last).
        Returns list of squares from start of the move (not including start square itself) to the end of the board.
        It is possible to input single square as a one-item list and direction as a string (nw/ne/sw/se).
        """
        output = []
        border_letter = move[0][0]
        border_number = move[0][1]

        if direction:
            match_input = direction
        else:
            match_input = self.get_move_direction(move)

        match match_input:
            case 'ne':
                while ord(border_letter) <= ord('h') and int(border_number) <= 8:
                    border_letter = chr(ord(border_letter) + 1)
                    border_number = str(int(border_number) + 1)
                output = self.find_inbetween_coords(move[0], (border_letter + border_number))
                return output
            case 'nw':
                while ord(border_letter) >= ord('a') and int(border_number) <= 8:
                    border_letter = chr(ord(border_letter) - 1)
                    border_number = str(int(border_number) + 1)
                output = self.find_inbetween_coords(move[0], (border_letter + border_number))
                return output
            case 'se':
                while ord(border_letter) <= ord('h') and int(border_number) >= 1:
                    border_letter = chr(ord(border_letter) + 1)
                    border_number = str(int(border_number) - 1)
                output = self.find_inbetween_coords(move[0], (border_letter + border_number))
                return output
            case 'sw':
                while ord(border_letter) >= ord('a') and int(border_number) >= 1:
                    border_letter = chr(ord(border_letter) - 1)
                    border_number = str(int(border_number) - 1)
                output = self.find_inbetween_coords(move[0], (border_letter + border_number))
                return output

    @staticmethod
    def generate_empty_field():
        output = None
        playing_field = {}
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for letter in letters:
            for number in range(1, 9):
                tag = str(letter) + str(number)
                playing_field[tag] = None
        output = playing_field
        return output

    @staticmethod
    def generate_list_of_square_names():
        output = []
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for letter in letters:
            for number in range(1, 9):
                tag = str(letter) + str(number)
                output.append(tag)
        return output

    @staticmethod
    def find_inbetween_coords(start, end):
        """
        Returns list of inbetween coordinates.
        Since this is a private method, no safety measures were included,
        works only for correct input == only coords on the same diagonal.
        """
        output = []
        possible_letters = []
        possible_numbers = []

        temp = ord(end[0]) - 1
        while ord(start[0]) < temp:
            possible_letters.append(chr(temp))
            temp = temp - 1

        temp = ord(end[0]) + 1
        while ord(start[0]) > temp:
            possible_letters.append(chr(temp))
            temp = temp + 1

        temp = int(end[1]) - 1
        while int(start[1]) < temp:
            possible_numbers.append(temp)
            temp = temp - 1

        temp = int(end[1]) + 1
        while int(start[1]) > temp:
            possible_numbers.append(temp)
            temp = temp + 1

        for i in range(len(possible_letters)):
            output.append(str(possible_letters[i]) + str(possible_numbers[i]))

        return output

    def get_bounded_line(self, start, end):
        output = [start, self.find_inbetween_coords(start, end), end]
        return output

    @staticmethod
    def get_circle(position, game_field, diameter=1):
        """
        Returns list of positions that are diameter away from the input position in each diagonal direction.
        """
        output = []
        for letter in [chr(ord(position[0]) - diameter), chr(ord(position[0]) + diameter)]:
            if (letter + str((int(position[1]) - diameter))) in game_field:
                output.append((letter + str((int(position[1]) - diameter))))
            if (letter + str((int(position[1]) + diameter))) in game_field:
                output.append((letter + str((int(position[1]) + diameter))))
        return output

    def find_all_valid_moves(self, game):
        """
        Generates all possible moves for each figure but returns only valid moves.
        Output depends on which player is to turn.
        Function expects validated and correctly typed game file.
        Output values:
        list of moves   - success
        empty list      - stalemate
        None            - game file error or other error
        """
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        all_square_names = self.generate_list_of_square_names()

        # GENERATING ALL MOVES
        moves = []  # contains lists [from, inbetween1, inbetween2, ... , to]

        # which figures to evaluate
        if game.get == PlayerColor.BLACK:
            figures_for_evaluation = ["b", "bb"]
        else:
            figures_for_evaluation = ["w", "ww"]

        # getting all moves for current player, even impossible ones
        for square in all_square_names:

            rowcol = self.get_rowcol_from_sq_string(square)
            r = rowcol[0]
            c = rowcol[1]

            for figure in figures_for_evaluation:
                if not isinstance(game.game_field[r][c], str):

                    # different figure abilities
                    if len(figure) == 1:
                        hop_range = 2
                    else:
                        hop_range = 8

                    for i in range(1, hop_range):
                        # finding neighbouring coordinates
                        # (cL = column on the left from figure,
                        # lD = line down from figure etc.)
                        cL, cR, lD, lU = None, None, None, None
                        if (ord(square[0]) - 97 - i) >= 0:
                            cL = letters[letters.index(square[0]) - i]
                        if (ord(square[0]) - 97 + i) <= (len(letters) - 1):
                            cR = letters[letters.index(square[0]) + i]
                        if (int(square[1]) - i) >= 1:
                            lD = int(square[1]) - i
                            lD = str(lD)
                        if (int(square[1]) + i) <= 8:
                            lU = int(square[1]) + i
                            lU = str(lU)

                        # appending moves considering game direction (which player started up)
                        if game.get_player_to_turn == PlayerColor.BLACK or (len(figure) > 1):
                            if cL and lD:  # and playing_field[(cL + lD)] not in figures_for_evaluation:
                                moves.append([square, (cL + lD)])
                            if cR and lD:  # and playing_field[(cR + lD)] not in figures_for_evaluation:
                                moves.append([square, (cR + lD)])

                        if game.get_player_to_turn == PlayerColor.WHITE or (len(figure) > 1):
                            if cL and lU:  # and playing_field[(cL + lU)] not in figures_for_evaluation:
                                moves.append([square, (cL + lU)])
                            if cR and lU:  # and playing_field[(cR + lU)] not in figures_for_evaluation:
                                moves.append([square, (cR + lU)])

        # removing simple moves that would jump over or step on teammate
        moves_to_delete = []

        for move in moves:

            rowcol0 = self.get_rowcol_from_sq_string(move[0])
            r0 = rowcol0[0]
            c0 = rowcol0[1]

            if (game.get_player_to_turn == PlayerColor.BLACK and game.game_field[r0][c0].get_label() in ['b', 'bb']) \
                    or (game.get_player_to_turn == PlayerColor.WHITE and game.game_field[r0][c0].get_label() in ['w', 'ww']):
                temp_line = self.span(move)
                temp_direction = self.get_move_direction(move)
                temp_occupied_sq_list = []

                for square in temp_line:

                    tmpln_rowcol = self.get_rowcol_from_sq_string(square)
                    r_sq = tmpln_rowcol[0]
                    c_sq = tmpln_rowcol[1]

                    if not isinstance(game.game_field[r_sq][c_sq], str):
                        if (game.get_player_to_turn == PlayerColor.BLACK and game.game_field[r_sq][c_sq].get_label() in ['b', 'bb']) or (
                                game.get_player_to_turn == PlayerColor.WHITE and game.game_field[r_sq][c_sq].get_label() in ['w', 'ww']):
                            temp_occupied_sq_list.append(square)

                for temp_occupied_sq in temp_occupied_sq_list:
                    temp_squares_to_delete_for_this_move = [temp_occupied_sq]
                    for sq in self.span([temp_occupied_sq], temp_direction):
                        temp_squares_to_delete_for_this_move.append(sq)

                    temp_squares_to_delete_for_this_move.append(temp_occupied_sq)

                    for sq_to_delete in temp_squares_to_delete_for_this_move:
                        moves_to_delete.append([move[0], sq_to_delete])

        for move in moves_to_delete:
            try:
                moves.remove(move)
            except ValueError:
                pass  # ignoring exceptions caused by trying to delete an item that is not in the lis

        # # checking for jump moves
        # jumping_moves = []
        # for move in moves:

        #     rowcol0 = self.get_rowcol_from_sq_string(move[0])
        #     r0 = rowcol0[0]
        #     c0 = rowcol0[1]

        #     rowcol1 = self.get_rowcol_from_sq_string(move[1])
        #     r1 = rowcol1[0]
        #     c1 = rowcol1[1]

        #     if ((game.get_player_to_turn == PlayerColor.WHITE and game.game_field[r1][c1].get_label() in ['b', 'bb'])
        #             or (game.get_player_to_turn == PlayerColor.BLACK and game.game_field[r1][c1].get_label() in ['w', 'ww'])):

        #         jump_move = [move[0], ""]

        #         # if there is enemy figure in vicinity
        #         if not isinstance(game.game_field[r0][c0], str):
        #             if (game.get_player_to_turn == PlayerColor.BLACK and game.game_field[r0][c0].get_label() in ['b', 'bb']) or (
        #                     game.get_player_to_turn == PlayerColor.WHITE and game.game_field[r0][c0].get_label() in ['w', 'ww']):

        #                 if (ord(move[0][0]) > ord(move[1][0])) and (chr(ord(move[1][0]) - 1) in letters):
        #                     jump_move[1] = jump_move[1] + str(chr(ord(move[1][0]) - 1))
        #                 elif (ord(move[0][0]) < ord(move[1][0])) and (chr(ord(move[1][0]) + 1) in letters):
        #                     jump_move[1] = jump_move[1] + str(chr(ord(move[1][0]) + 1))

        #                 if (int(move[0][1]) > int(move[1][1])) and ((int(move[1][1]) - 1) <= 8) and (
        #                         (int(move[1][1]) - 1) >= 1) and (game.get_player_to_turn == PlayerColor.BLACK or game.game_field[r0][c0].get_label() in ['bb', 'ww']):
        #                     jump_move[1] = jump_move[1] + str(int(move[1][1]) + 1)
        #                 elif (int(move[0][1]) < int(move[1][1])) and ((int(move[1][1]) + 1) <= 8) and (
        #                         (int(move[1][1]) + 1) >= 1) and (game.get_player_to_turn == PlayerColor.WHITE or game.game_field[r0][c0].get_label() in ['bb', 'ww']):
        #                     jump_move[1] = jump_move[1] + str(int(move[1][1]) + 1)

        #                 if len(jump_move[1]) == 2:
        #                     jumping_moves.append(jump_move)

        # # eliminating simple moves if any jumping moves are available
        # if jumping_moves:
        #     moves = jumping_moves

        #     # eliminating stone moves if any queen/king moves are available
        #     queen_moves = []
        #     for move in moves:

        #         rowcol0 = self.get_rowcol_from_sq_string(move[0])
        #         r0 = rowcol0[0]
        #         c0 = rowcol0[1]

        #         if game.game_field[r0][c0].get_label() in ['bb', 'ww']:
        #             queen_moves.append(move)
        #     if queen_moves:
        #         moves = queen_moves

        #     # if there are any jumping moves, they need to be simulated further for compulsory chained jumps
        #     # moves = self.jump_move_simulation(moves, playing_field)
        #     moves = jumping_moves

        # creating move objects
        obj_moves = []
        for move in moves:
            rowcol = self.get_rowcol_from_sq_string(move[0])
            r = rowcol[0]
            c = rowcol[1]
            temp_move = Move(move, game.game_field[r0][c0])
            obj_moves.append(temp_move)

        # adding move objects to move trees of figures
        for obj_move in obj_moves:
            obj_figure = obj_move.get_figure
            obj_figure.moves_tree.add_move(obj_move)
            
'''
    def jump_move_simulation(self, moves, game_field):
        """
        Takes moves list on input, presumes all of them are jumping moves.
        Simulates all possible outcomes of these moves a tests for any compulsory jump moves.
        Returns list of moves and chained moves, if any.
        Any chained moves would replace their predecessors - no need to check that after this function ended.
        """
        simulated_move_trees = []

        # 1) transfering lists of strings into Move objects 
        for move in moves:

            # copying playing field so we avoid editing actual game and are just simulating what could happen
            simulated_game_field = copy.deepcopy(game_field)

            # for better navigation chained jumps will be stored in trees
            simulated_moves_tree = MovesTree()
            root_move = Move(move[0], move[1], simulated_game_field(move[0]), simulated_game_field)
            simulated_moves_tree.set_root_move(root_move)
            simulated_move_trees.append(simulated_moves_tree)

        # 2) calculating all possible chained jump variations
        for move_tree in simulated_move_trees:
            self._simulation_subprocess(move_tree.get_root(), simulated_game_field)

        # 3) transfering Move objects into lists of string

    def _simulation_subprocess(self, move, simulated_game_field):
        squares_of_interest = []

        if move.figure in ['w', 'b']:
            close_vicinity = self.get_circle(simulated_game_field, diameter=1)
            further_vicinity = self.get_circle(simulated_game_field, diameter=2)
            for closer_sq in close_vicinity:
                for further_sq in further_vicinity:
                    if (self.get_move_direction([move[0], closer_sq]) == self.get_move_direction(
                            [move[0], further_sq]) and
                            simulated_game_field[closer_sq] in move.enemies and
                            simulated_game_field[further_sq] is None):
                        move.force_birth(further_sq)

        # considering all cases for kings and queens
        elif root_move.figure in ['ww', 'bb']:
            close_vicinity = []
            temp_circle = self.get_circle(simulated_game_field, diameter=1)
            previous_sq = None
            for direction in temp_circle:
                previous_sq = direction
                for item in self.span([root_move.data[0], direction]):
                    if (simulated_game_field[previous_sq] in root_move.enemies and
                            simulated_game_field[item] is None):
                        root_move.force_birth(further_sq)
                    previous_sq = item

        # after first set of childern has been generated the algorithm can repeat itself recursively
        for child in root_move.children:
            temp_gamefield = copy.deepcopy(simulated_game_field)
            self.move_execution(child.data, temp_gamefield)
            self._simulation_subprocess(child, temp_gamefield)

    def move_execution(self, move, game_field):
        """
        Takes game_field dictionary and move on input.
        Performs the move and changes game_field accordingly.
        Returns changed game_field on output.
        """
        for i in range(len(move) - 1):
            # selected "friendly" figure transportation
            game_field[move[i + 1]] = game_field[move[i]]
            game_field[move[i]] = None

            # possible uprank
            if game_field[move[i + 1]] == 'b' and move[i + 1] in ['a1', 'c1', 'e1', 'g1']:
                game_field[move[i + 1]] = 'bb'

            if game_field[move[i + 1]] == 'w' and move[i + 1] in ['b8', 'd8', 'f8', 'h8']:
                game_field[move[i + 1]] = 'ww'

            # "enemy" figure deletion
            squares_to_destroy = self.find_inbetween_coords(move[i], move[i + 1])
            for sq in squares_to_destroy:
                game_field[sq] = None
'''