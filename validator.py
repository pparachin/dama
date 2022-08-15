# general modules
import copy
from types import NoneType

# our modules
from alias import *
from figure import Figure
from move_tree import *
from stone import Stone
from lady import Lady


class Validator():

    def __init__(self):
        ...

    @staticmethod
    def check_valid_board(game_file_path):
        invalid_squares = ["a2", "a4", "a6", "a8", "b1", "b3", "b5", "b7", "c2", "c4", "c6", "c8", "d1", "d3", "d5",
                           "d7",
                           "e2", "e4", "e6", "e8", "f1", "f3", "f5", "f7", "g2", "g4", "g6", "g8", "h1", "h3", "h5",
                           "h7"]
        squares_checked = []

        try:
            with open(game_file_path) as game_file:
                game_file_contents = game_file.read().splitlines()

                for line in game_file_contents:
                    if line[0:2] in invalid_squares or line[0:2] in squares_checked:
                        return False
                    squares_checked.append(line[0:2])
        except FileNotFoundError:
            return False
        return True

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
        except FileNotFoundError:
            output = None

        return playing_field

    def game_field_to2D(self, field):
        board = []
        for dimension in range(8):
            board.append([None, None, None, None, None, None, None, None])

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

        base_setup = ["a1,w",
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
                      "h8,b"]

        output = None
        try:
            with open(game_file_path) as game_file:
                game_file_contents = game_file.read().splitlines()
                setup_v1 = None

                for valid_line in base_setup:
                    if valid_line not in game_file_contents:
                        setup_v1 = False
                        break
                    setup_v1 = True

                if setup_v1:
                    for line in game_file_contents:
                        if line not in base_setup:
                            output = 1
                            break
                    output = 0
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
        output = None

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

    def get_circle(self, position, diameter=1):
        """
        Returns list of positions that are diameter away from the input position in each diagonal direction.
        """
        game_field = self.generate_empty_field()  # for reference only
        output = []
        for letter in [chr(ord(position[0]) - diameter), chr(ord(position[0]) + diameter)]:
            if (letter + str((int(position[1]) - diameter))) in game_field:
                output.append((letter + str((int(position[1]) - diameter))))
            if (letter + str((int(position[1]) + diameter))) in game_field:
                output.append((letter + str((int(position[1]) + diameter))))
        return output

    def get_std_twin(self, position, diameter=1, color=StoneColor.WHITE):
        circle = self.get_circle(position, diameter)
        if color == StoneColor.WHITE:
            is_white = True
        else:
            is_white = False
        min_sq = 9
        max_sq = 0
        for sq in circle:
            if int(sq[1]) < min_sq: min_sq = int(sq[1])
            if int(sq[1]) > max_sq: max_sq = int(sq[1])
        sqs_to_remove = []
        for sq in circle:
            if is_white and int(sq[1]) < max_sq:
                sqs_to_remove.append(sq)
            elif not is_white and int(sq[1]) > min_sq:
                sqs_to_remove.append(sq)
        for sq in sqs_to_remove:
            try:
                circle.remove(sq)
            except ValueError:
                pass  # ignoring exceptions caused by trying to delete an item that is not in the list
        return circle

    def get_figure_from_move(self, move_as_a_list, game_field):
        """
        Takes a move in the form of a list on input and returns the figure at the first position as pointer to object.
        This function DOES NOT assert correctness.
        """
        return game_field[self.get_rowcol_from_sq_string(move_as_a_list[0])[0]][self.get_rowcol_from_sq_string(move_as_a_list[0])[1]]

    def find_all_valid_moves(self, game, player_to_turn):
        """
        Generates all possible moves for each figure but returns only valid moves.
        Output depends on which player is to turn.
        Function expects validated and correctly typed game file.
        Output values:
        list of moves   - success
        empty list      - stalemate
        None            - game file error or other error
        """
        game_field = game.get_game_field()
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        all_square_names = self.generate_list_of_square_names()

        # GENERATING ALL MOVES
        moves = []  # contains lists [from, inbetween1, inbetween2, ... , to]

        # which figures to evaluate
        if player_to_turn == PlayerColor.BLACK:
            figures_for_evaluation = ["b", "bb"]
        else:
            figures_for_evaluation = ["w", "ww"]

        # getting all moves for current player, even impossible ones
        for square in all_square_names:

            rowcol = self.get_rowcol_from_sq_string(square)
            r = rowcol[0]
            c = rowcol[1]

            for figure in figures_for_evaluation:
                if not isinstance(game_field[r][c], (str, NoneType)) and isinstance(game_field[r][c], Figure) and (game_field[r][c].get_label() == figure):

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
                        if player_to_turn == PlayerColor.BLACK or (len(figure) > 1):
                            if cL and lD:  # and playing_field[(cL + lD)] not in figures_for_evaluation:
                                moves.append([square, (cL + lD)])
                            if cR and lD:  # and playing_field[(cR + lD)] not in figures_for_evaluation:
                                moves.append([square, (cR + lD)])

                        if player_to_turn == PlayerColor.WHITE or (len(figure) > 1):
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

            if (player_to_turn == PlayerColor.BLACK and game_field[r0][c0].get_label() in ['b', 'bb']) \
                    or (player_to_turn == PlayerColor.WHITE and game_field[r0][c0].get_label() in ['w',
                                                                                                   'ww']):
                temp_line = self.span(move)
                temp_direction = self.get_move_direction(move)
                temp_occupied_sq_list = []


                for square in temp_line:

                    tmpln_rowcol = self.get_rowcol_from_sq_string(square)
                    r_sq = tmpln_rowcol[0]
                    c_sq = tmpln_rowcol[1]

                    if isinstance(game_field[r_sq][c_sq], Figure):
                        # if (player_to_turn == PlayerColor.BLACK and game_field[r_sq][
                        #     c_sq].get_label() in ['b', 'bb']) or (
                        #         player_to_turn == PlayerColor.WHITE and game_field[r_sq][
                        #     c_sq].get_label() in ['w', 'ww']):
                        #     temp_occupied_sq_list.append(square)
                        temp_occupied_sq_list.append(square)

                for temp_occupied_sq in temp_occupied_sq_list:
                    temp_squares_to_delete_for_this_move = [temp_occupied_sq]
                    for sq in self.span([temp_occupied_sq], temp_direction):
                        temp_squares_to_delete_for_this_move.append(sq)

                    temp_squares_to_delete_for_this_move.append(temp_occupied_sq)

                    for sq_to_delete in temp_squares_to_delete_for_this_move:
                        moves_to_delete.append([move[0], sq_to_delete])


        # checking for jump moves
        jumping_moves = []
        for move in moves:

            rowcol0 = self.get_rowcol_from_sq_string(move[0])
            r0 = rowcol0[0]
            c0 = rowcol0[1]

            rowcol1 = self.get_rowcol_from_sq_string(move[1])
            r1 = rowcol1[0]
            c1 = rowcol1[1]

            # if there is enemy figure in vicinity
            if isinstance(game_field[r1][c1], Figure):
                if (player_to_turn == PlayerColor.WHITE and game_field[r1][c1].get_label() in ['b', 'bb']) or (
                        player_to_turn == PlayerColor.BLACK and game_field[r1][c1].get_label() in ['w', 'ww']):

                    if isinstance(game_field[r0][c0], Stone):
                        for sq in self.get_std_twin(game_field[r0][c0].get_position(), diameter=2,
                                                    color=(game_field[r0][c0].get_color())):
                            direction = self.get_move_direction([move[0], sq])
                            if direction == self.get_move_direction(move) and game_field[self.get_rowcol_from_sq_string(sq)[0]][self.get_rowcol_from_sq_string(sq)[1]] is None:
                                jumping_moves.append([move[0], sq])
                        
            if isinstance(game_field[r0][c0], Lady) and game_field[r1][c1] is None:
                stone_count = 0
                for square in self.find_inbetween_coords(move[0], move[1]):
                    if isinstance(game_field[self.get_rowcol_from_sq_string(square)[0]][self.get_rowcol_from_sq_string(square)[1]], Figure) and \
                    ((player_to_turn == PlayerColor.WHITE and game_field[self.get_rowcol_from_sq_string(square)[0]][self.get_rowcol_from_sq_string(square)[1]].get_label() in ['b', 'bb']) or
                    (player_to_turn == PlayerColor.BLACK and game_field[self.get_rowcol_from_sq_string(square)[0]][self.get_rowcol_from_sq_string(square)[1]].get_label() in ['w', 'ww'])):
                        stone_count += 1

                    elif isinstance(game_field[self.get_rowcol_from_sq_string(square)[0]][self.get_rowcol_from_sq_string(square)[1]], Figure) and \
                    ((player_to_turn == PlayerColor.BLACK and game_field[self.get_rowcol_from_sq_string(square)[0]][self.get_rowcol_from_sq_string(square)[1]].get_label() in ['b', 'bb']) or
                    (player_to_turn == PlayerColor.WHITE and game_field[self.get_rowcol_from_sq_string(square)[0]][self.get_rowcol_from_sq_string(square)[1]].get_label() in ['w', 'ww'])):
                        stone_count = 0
                        break
            
                if stone_count == 1:
                    jumping_moves.append(move)

        for move in moves_to_delete:
            try:
                moves.remove(move)
            except ValueError:
                pass  # ignoring exceptions caused by trying to delete an item that is not in the list


        # eliminating simple moves if any jumping moves are available
        if jumping_moves:
            moves = jumping_moves
            are_queen_moves = False

            # eliminating stone moves if any queen/king moves are available
            queen_moves = []
            for move in moves:

                rowcol0 = self.get_rowcol_from_sq_string(move[0])
                r0 = rowcol0[0]
                c0 = rowcol0[1]

                if game_field[r0][c0].get_label() in ['bb', 'ww']:
                    queen_moves.append(move)

            if queen_moves:
                moves = queen_moves
                are_queen_moves = True

            # if there are any jumping moves, they need to be simulated further for compulsory chained jumps
            moves = self.jump_move_simulation(moves, game, are_queen_moves)

        # creating move objects
        # obj_moves = []
        # for move in moves:
        #     rowcol = self.get_rowcol_from_sq_string(move[0])
        #     r = rowcol[0]
        #     c = rowcol[1]
        #     temp_move = Move(move, game_field[r][c])
        #     obj_moves.append(temp_move)

        control_output = moves

        # REMOVED BECAUSE OF DUPLICITY ISSUES
        # adding move objects to move trees of figures
        #for obj_move in obj_moves:
        #    obj_figure = obj_move.get_figure()
        #    obj_figure.moves_tree.add_move(obj_move)

        # control output
        return control_output

    def jump_move_simulation(self, moves, game, are_queen_moves):
        """
        Takes moves list on input, presumes all of them are jumping moves.
        Simulates all possible outcomes of these moves a tests for any compulsory jump moves.
        Returns list of moves and chained moves, if any.
        Any chained moves would replace their predecessors - no need to check that after this function ended.
        """
        # IMPORTANT_NOTE: Multijumps / chained jumps are not superior to single-jumps, meaning if the player can perform a single-jump with one figure and chained
        # jump with other, they can choose which one they'll perform. However it is not allowed to jump fewer times than possible with one particular figure. Also
        # queen / lady jumps are ALWAYS prioritized to regular stone moves and regular stone jumps.

        output = moves
        game_field = game.get_game_field()
        while True:
            jump_is_possible = False
            for move in output:
                jump_is_possible = False # try to chain as many jumps as possible
                # test only 2 directions and only first tile
                current_figure = game_field[self.get_rowcol_from_sq_string(move[0])[0]][self.get_rowcol_from_sq_string(move[0])[1]]
                move_direction = self.get_move_direction(move)
                candidate_moves = []
                stone_color = StoneColor.WHITE if move_direction[0] == 'n' else StoneColor.BLACK
                candidate_enemy_tiles = self.get_std_twin(move[-1], 1, stone_color)
                candidate_empty_tiles = self.get_std_twin(move[-1], 2, stone_color)
                for tile1 in candidate_enemy_tiles:
                    for tile2 in candidate_empty_tiles:
                        if (self.get_move_direction([tile1, tile2]) in ['ne', 'nw'] and move_direction[0] == 'n') or (self.get_move_direction([tile1, tile2]) in ['se', 'sw'] and move_direction[0] == 's'):
                            #candidate_move = copy.deepcopy(move)
                            candidate_move = copy.copy(move)
                            candidate_move.append(tile2)
                            candidate_moves.append(candidate_move)

                # test for enemies and empty spaces in candidate_moves (ONLY REGULAR STONES)
                # 1) enemy on closer tile
                # 2) empty space OR CURRENT FIGURE on farther tile
                # 3) NO TILE REPETITION <- not handeled in current version
                for candidate_move in candidate_moves:
                    row_minus2, col_minus2 = self.get_rowcol_from_sq_string(candidate_move[-2])
                    row_minus1, col_minus1 = self.get_rowcol_from_sq_string(candidate_move[-1])
                    betw_tile = self.find_inbetween_coords(candidate_move[-2], candidate_move[-1])
                    row_betw, col_betw = self.get_rowcol_from_sq_string(betw_tile[0]) 
                    # betw_tile is output of function, that typically returns list of n strings with length of 2 characters
                    # but this time we know it will always return len=1 string, thus the betw_tile[0]
                    full_move_chain = []
                    for i in range(1, len(candidate_move)):
                        if candidate_move[i-1] not in full_move_chain: full_move_chain.append(candidate_move[i-1])
                        extensions = self.find_inbetween_coords(candidate_move[i], candidate_move[i-1])
                        for extension in extensions:
                            if extension not in full_move_chain: full_move_chain.append(extension)
                        if candidate_move[i] not in full_move_chain: full_move_chain.append(candidate_move[i])
                    #if (candidate_move[-2] not in full_move_chain) and (game_field[row_betw][col_betw] is None) and (game[row_minus1][col_minus1] is None or game[row_minus1][col_minus1] == current_figure):
                    if ((game_field[row_betw][col_betw] is not None and game_field[row_betw][col_betw].get_color() is StoneColor.WHITE and current_figure.get_color() is StoneColor.BLACK) or (game_field[row_betw][col_betw] is not None and game_field[row_betw][col_betw].get_color() is StoneColor.BLACK and current_figure.get_color() is StoneColor.WHITE)) and (game_field[row_minus1][col_minus1] is None or game_field[row_minus1][col_minus1] == current_figure):
                        moves.append(candidate_move)
                        print(candidate_move)
                        jump_is_possible = True

                if are_queen_moves:
                    pass
                    # test other 2 directions and all tiles for all directions
                    # tiles can repeat themselves
            
            output = moves
            if not jump_is_possible:
                break

        return output
        
        # OLD CODE

        # simulated_move_trees = []
        # output = []

        # # 1) transfering lists of strings into Move objects
        # for move in moves:
            
        #     # copying playing field so we avoid editing actual game and are just simulating what could happen
        #     simulated_game_field = copy.deepcopy(game.game_field)

        #     # for better navigation chained jumps will be stored in trees
        #     simulated_moves_tree = MovesTree()

        #     rowcol = self.get_rowcol_from_sq_string(move[0])
        #     r = rowcol[0]
        #     c = rowcol[1]

        #     root_move = Move(input_list_of_squares=[move[0], move[1]], input_figure=game.game_field[r][c],
        #                      input_board=simulated_game_field)
        #     simulated_moves_tree.set_root_move(root_move)
        #     simulated_move_trees.append(simulated_moves_tree)

        # # 2) calculating all possible chained jump variations
        # for move_tree in simulated_move_trees:
        #     game.sync_figure_positions_with_field(game.get_game_field())
        #     self._simulation_subprocess(move_tree.get_root(), simulated_game_field, game)

        # # 3) transfering Move objects into lists of string
        # for tree in simulated_move_trees:
        #     for move in get_moves(tree):
        #         output.append(move)

        # # 4) repairing figure positions that may have been changed during _simulation_subprocess
        # game.sync_figure_positions_with_field(game.get_game_field())

        # return output

        # END OF OLD CODE


    def _simulation_subprocess(self, move, simulated_game_field, game):

        game.sync_figure_positions_with_field(simulated_game_field)
        to_be_calculated = []

        # considering all cases for Stone()
        if move.get_figure().get_label() in ['w', 'b']:
            enemies = ['w', 'ww'] if move.get_figure().get_label() == 'b' else ['b', 'bb']
            close_vicinity = self.get_std_twin(move.get_figure().get_position(), diameter=1,
                                               color=move.get_figure().get_color())
            further_vicinity = self.get_std_twin(move.get_figure().get_position(), diameter=2,
                                                 color=move.get_figure().get_color())
            for closer_sq in close_vicinity:
                for further_sq in further_vicinity:

                    rowcol = self.get_rowcol_from_sq_string(closer_sq)
                    clo_r = rowcol[0]
                    clo_c = rowcol[1]
                    rowcol = self.get_rowcol_from_sq_string(further_sq)
                    fur_r = rowcol[0]
                    fur_c = rowcol[1]

                    if (self.get_move_direction([move.get_data()[0], closer_sq]) == self.get_move_direction(
                            [move.get_data()[0], further_sq]) and
                            isinstance(simulated_game_field[clo_r][clo_c], Figure) and
                            simulated_game_field[clo_r][clo_c].get_label() in enemies and
                            isinstance(simulated_game_field[fur_r][fur_c], str)):
                        newchild = move.force_birth(further_sq)
                        to_be_calculated.append(newchild)

        # considering all cases for Lady()
        # TODO:

        # simulating the moves
        for child in to_be_calculated:
            self.move_simulation(move, simulated_game_field)
            # repeating itself until no new children were generated
            self._simulation_subprocess(child, simulated_game_field, game)

    def move_simulation(self, input_move, game_field):
        """
        Same as self.move_execution(), but does not eliminate enemy figures to ensure chained
        jumps are calculated according to game rules (e.g. if 'ww' jumped over 'b' to north-east,
        it cannot immediately after jump over 'b' on south-west because the first 'b' is still there
        until the whole jumping chain is completed)
        """

        for move in get_moves(input_move):

            for i in range(len(move) - 1):
                # selected "friendly" figure transportation
                old_stone = game_field[self.get_rowcol_from_sq_string(move[i + 1])[0]][
                    self.get_rowcol_from_sq_string(move[i + 1])[1]]

                game_field[self.get_rowcol_from_sq_string(move[i + 1])[0]][
                    self.get_rowcol_from_sq_string(move[i + 1])[1]] = \
                    game_field[self.get_rowcol_from_sq_string(move[i])[0]][self.get_rowcol_from_sq_string(move[i])[1]]

    def move_execution(self, input_move, game_field, player_to_turn, players):
        """
        Takes game_field dictionary and move on input.
        Logs the move into selected figure's move_tree.
        Performs the move and changes game_field accordingly.
        Returns changed game_field on output.
        """
        move = input_move

        # adding the move into figure's move_tree
        selected_figure = self.get_figure_from_move(input_move, game_field)
        selected_figure.set_as_chosen_move_in_tree(input_move)

        for i in range(len(move) - 1):
            # selected "friendly" figure transportation
            old_stone = game_field[self.get_rowcol_from_sq_string(move[i])[0]][
                self.get_rowcol_from_sq_string(move[i])[1]]

            # transport figure to next square
            game_field[self.get_rowcol_from_sq_string(move[i + 1])[0]][
                self.get_rowcol_from_sq_string(move[i + 1])[1]] = \
                game_field[self.get_rowcol_from_sq_string(move[i])[0]][self.get_rowcol_from_sq_string(move[i])[1]]
            
            # set new position for figure
            game_field[self.get_rowcol_from_sq_string(move[i + 1])[0]][self.get_rowcol_from_sq_string(move[i + 1])[1]].set_position(move[i + 1])

            # delete figure reference from old square
            game_field[self.get_rowcol_from_sq_string(move[i])[0]][self.get_rowcol_from_sq_string(move[i])[1]] = None

            # possible uprank
            contents_of_next_square = game_field[self.get_rowcol_from_sq_string(move[i + 1])[0]][
                self.get_rowcol_from_sq_string(move[i + 1])[1]]
            if contents_of_next_square.get_label() == 'b' and contents_of_next_square.get_position() in ['a1', 'c1',
                                                                                                            'e1',
                                                                                                            'g1']:
                game_field[self.get_rowcol_from_sq_string(move[i + 1])[0]][
                    self.get_rowcol_from_sq_string(move[i + 1])[1]].set_label('bb')
                new_lady = Lady(old_stone.get_position(), old_stone.get_color(), old_stone.get_status(), old_stone.get_label())
                game_field[self.get_rowcol_from_sq_string(move[i + 1])[0]][
                    self.get_rowcol_from_sq_string(move[i + 1])[1]] = new_lady

            contents_of_next_square = game_field[self.get_rowcol_from_sq_string(move[i + 1])[0]][
                self.get_rowcol_from_sq_string(move[i + 1])[1]]
            if contents_of_next_square.get_label() == 'w' and contents_of_next_square.get_position() in ['b8', 'd8',
                                                                                                            'f8',
                                                                                                            'h8']:
                game_field[self.get_rowcol_from_sq_string(move[i + 1])[0]][
                    self.get_rowcol_from_sq_string(move[i + 1])[1]].set_label('ww')
                new_lady = Lady(old_stone.get_position(), old_stone.get_color(), old_stone.get_status(), old_stone.get_label())

                game_field[self.get_rowcol_from_sq_string(move[i + 1])[0]][
                    self.get_rowcol_from_sq_string(move[i + 1])[1]] = new_lady

            # "enemy" figure deletion
            squares_to_destroy = self.find_inbetween_coords(move[i], move[i + 1])

            if squares_to_destroy:
                if player_to_turn == players[0].get_color():
                    players[0].set_score(players[0].get_score() + 1)
                else:
                    players[1].set_score(players[1].get_score() + 1)

            for sq in squares_to_destroy:
                game_field[self.get_rowcol_from_sq_string(sq)[0]][self.get_rowcol_from_sq_string(sq)[1]] = None

        return game_field