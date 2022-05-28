# general modules
import copy

# our modules
from alias import PlayerColor
from alias import GameDirection
from move_tree import *


class Validator():


    def __init__(self):
        ...


    @staticmethod
    def generate_game_field(game_file_path):
        '''
        This function opens .csv file and outputs corresponding "game field dictionary".
        !!! Note: This function function does NOT validate if the text inside file is correct. !!! 
        '''
        output = None
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


    @staticmethod
    def validate_base_setup(game_file_path):
        '''
        returns 0 if input file path leads to .csv file containing correct setup for Czech dama
        returns 1 for incorrect game setup
        returns 2 for errors connected with reading the file, e.g.: incorrect path
        '''
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
        '''
        Takes simple move on input (that means a list of squares, only consideres first and last).
        Returns string representing direction (ne/nw/se/sw) according to correct board position where:
        a1 is bottom left corner
        a8 is top left corner
        h8 is top right corner
        h1 is bottom right corner
        '''
        output, up, right = None, None, None

        if ord(move[0][0]) < ord(move[1][0]): right = True
        else: right = False
        
        if int(move[0][1]) < int(move[1][1]): up = True
        else: up = False

        if up and right: output = 'ne'
        elif up and not right: output = 'nw'
        elif not up and right: output = 'se'
        elif not up and not right: output = 'sw'

        return output


    def span(self, move, direction=None):
        '''
        Takes simple move on input (that means a list of squares, only consideres first and last).
        Returns list of squares from start of the move (not including start square itself) to the end of the board.
        It is possible to input single square as a one-item list and direction as a string (nw/ne/sw/se).
        '''
        output = []
        border_letter = move[0][0]
        border_number = move[0][1]

        if direction: match_input = direction
        else: match_input = self.get_move_direction(move)

        match match_input:
            case 'ne':
                while ord(border_letter) <= ord('h') and int(border_number) <= 8:
                    border_letter = chr(ord(border_letter)+1)
                    border_number = str(int(border_number)+1)
                output = self.find_inbetween_coords(move[0], (border_letter+border_number))

            case 'nw':
                while ord(border_letter) >= ord('a') and int(border_number) <= 8:
                    border_letter = chr(ord(border_letter)-1)
                    border_number = str(int(border_number)+1)
                output = self.find_inbetween_coords(move[0], (border_letter+border_number))

            case 'se':
                while ord(border_letter) <= ord('h') and int(border_number) >= 1:
                    border_letter = chr(ord(border_letter)+1)
                    border_number = str(int(border_number)-1)
                output = self.find_inbetween_coords(move[0], (border_letter+border_number))

            case 'sw':
                while ord(border_letter) >= ord('a') and int(border_number) >= 1:
                    border_letter = chr(ord(border_letter)-1)
                    border_number = str(int(border_number)-1)
                output = self.find_inbetween_coords(move[0], (border_letter+border_number))
        
        return output        


    @staticmethod
    def find_inbetween_coords(start, end):
        '''
        Returns list of inbetween coordinates.
        Since this is a private method, no safety measures were included,
        works only for correct input == only coords on the same diagonal.
        '''       
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
        output = [start]
        output.append(self.find_inbetween_coords([start, end]))
        output.append(end)
        return output


    def get_circle(self, position, game_field, diameter=1):
        '''
        Returns list of positions that are diameter away from the input position in each diagonal direction.
        '''
        output = []
        for letter in [ chr(ord(position[0]) - diameter), chr(ord(position[0]) + diameter) ]:
            if (letter + str((int(position[1]) - diameter))) in game_field:
                output.append((letter + str((int(position[1]) - diameter))))
            if (letter + str((int(position[1]) + diameter))) in game_field:
                output.append((letter + str((int(position[1]) + diameter))))
        return output


    def find_all_valid_moves(self, playing_field, player_to_turn, game_direction=GameDirection.WHITE_IS_DOWN):
        """
        Generates all possible moves for each figure but returns only valid moves.
        Output depends on which player is to turn.
        Function expects validated and correctly typed game file.
        Output values:
        list of moves   - success
        empty list      - stalemate
        None            - game file error or other error
        """
        output = None
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        player = player_to_turn # 0=BLACK, 1=WHITE
        assert player in [PlayerColor.BLACK, PlayerColor.WHITE]
        
        direction = game_direction # 0=white goes down, 1=black goes down
        assert direction in [GameDirection.WHITE_IS_DOWN, GameDirection.WHITE_IS_UP]

        ### GENERATING ALL MOVES ###
        moves = [] # contains lists [from, inbetween1, inbetween2, ... , to]

        # which figures to evaluate
        figures_for_evaluation = []
        if player_to_turn == PlayerColor.BLACK: figures_for_evaluation = ["b", "bb"]
        else: figures_for_evaluation = ["w", "ww"]

        # getting all moves for current player, even impossible ones
        for square in playing_field:
            for figure in figures_for_evaluation:
                if playing_field[square] == figure:

                    # different figure abilities
                    if len(figure) == 1: hop_range = 2
                    else: hop_range = 8

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
                        if (game_direction == GameDirection.WHITE_IS_UP and player_to_turn == PlayerColor.WHITE) or (game_direction == GameDirection.WHITE_IS_DOWN and player_to_turn == PlayerColor.BLACK) or (len(figure) > 1):
                            if cL and lD:# and playing_field[(cL + lD)] not in figures_for_evaluation:
                                moves.append( [square, (cL + lD)] )
                            if cR and lD:# and playing_field[(cR + lD)] not in figures_for_evaluation:
                                moves.append( [square, (cR + lD)] )

                        if (game_direction == GameDirection.WHITE_IS_UP and player_to_turn == PlayerColor.BLACK) or (game_direction == GameDirection.WHITE_IS_DOWN and player_to_turn == PlayerColor.WHITE) or (len(figure) > 1):
                            if cL and lU:# and playing_field[(cL + lU)] not in figures_for_evaluation:
                                moves.append( [square, (cL + lU)] )
                            if cR and lU:# and playing_field[(cR + lU)] not in figures_for_evaluation:
                                moves.append( [square, (cR + lU)] )

        # removing simple moves that would jump over or step on teammate
        for move in moves:
            if (player_to_turn==PlayerColor.BLACK and playing_field[move[0]] in ['b', 'bb']) or (player_to_turn==PlayerColor.WHITE and playing_field[move[0]] in ['w', 'ww']):
                temp_line = self.span(move)
                temp_direction = self.get_move_direction(move)
                temp_occupied_sq = None

                for square in temp_line:
                    if (player_to_turn==PlayerColor.BLACK and playing_field[square] in ['b', 'bb']) or (player_to_turn==PlayerColor.WHITE and playing_field[square] in ['w', 'ww']):
                        temp_occupied_sq = square
                        break
                
                if temp_occupied_sq:
                    temp_squares_to_delete_for_this_move = [temp_occupied_sq] + self.span([temp_occupied_sq], temp_direction)

                    for sq_to_delete in temp_squares_to_delete_for_this_move:
                        try:
                            moves.remove([move[0], sq_to_delete])
                        except ValueError:
                            pass # ignoring exceptions caused by trying to delete an item that is not in the list

        # checking for jump moves
        jumping_moves = []
        for move in moves:
            if ((player_to_turn==PlayerColor.WHITE and playing_field[move[1]] in ['b', 'bb'])
                or (player_to_turn==PlayerColor.BLACK and playing_field[move[1]] in ['w', 'ww'])):
                
                jump_move = [move[0], ""]
                
                if (player_to_turn==PlayerColor.BLACK and playing_field[move[0]] in ['b', 'bb']) or (player_to_turn==PlayerColor.WHITE and playing_field[move[0]] in ['w', 'ww']):
                    if (ord(move[0][0]) > ord(move[1][0])) and (chr(ord(move[1][0])-1) in letters):
                        jump_move[1] = jump_move[1] + str(chr(ord(move[1][0])-1))
                    elif (ord(move[0][0]) < ord(move[1][0])) and (chr(ord(move[1][0])+1) in letters):
                        jump_move[1] = jump_move[1] + str(chr(ord(move[1][0])+1))

                    if (int(move[0][1]) > int(move[1][1])) and ((int(move[1][1])-1) <= 8) and ((int(move[1][1])-1) >= 1):
                        jump_move[1] = jump_move[1] + str(int(move[1][1])+1)
                    elif (int(move[0][1]) < int(move[1][1])) and ((int(move[1][1])+1) <= 8) and ((int(move[1][1])+1) >= 1):
                        jump_move[1] = jump_move[1] + str(int(move[1][1])+1)

                    if len(jump_move[1]) == 2:
                        jumping_moves.append(jump_move)
    
        # eliminating simple moves if any jumping moves are available
        if jumping_moves:
            moves = jumping_moves

            # eliminating stone moves if any queen/king moves are available
            queen_moves = []
            for move in moves:
                if playing_field[move[0]] in ['bb', 'ww']:
                    queen_moves.append(move)
            if queen_moves:
                moves = queen_moves

            # if there are any jumping moves, they need to be simulated further for compulsory chained jumps
            #moves = self.jump_move_simulation(moves, playing_field)
            moves = jumping_moves # !!! DOES NOT FEATURE FULL FUNCTIONALITY YET

        output = moves
        return output


    def move_execution(self, move, game_field):
        '''
        Takes game_field dictionary and move on input.
        Performs the move and changes game_field accordingly.
        Returns changed game_field on output.
        '''
        for i in range(len(move)-1):
            # selected "friendly" figure transportation
            game_field[move[i+1]] = game_field[move[i]]
            game_field[move[i]] = None

            # possible uprank
            if (game_field[move[i+1]] == 'b' and move[i+1] in ['a1', 'c1', 'e1', 'g1']):
                game_field[move[i+1]] = 'bb'
            if (game_field[move[i+1]] == 'w' and move[i+1] in ['b8', 'd8', 'f8', 'h8']):
                game_field[move[i+1]] = 'ww'

            # "enemy" figure deletion
            squares_to_destroy = self.find_inbetween_coords(move[i], move[i+1])
            for sq in squares_to_destroy:
                game_field[sq] = None


    def jump_move_simulation(self, moves, game_field):
        '''
        Takes moves list on input, presumes all of them are jumping moves.
        Simulates all possible outcomes of these moves a tests for any compulsory jump moves.
        Returns list of moves and chained moves, if any.
        Any chained moves would replace their predecessors - no need to check that after this function ended.
        '''
        simulated_move_trees_pointers = []

        for move in moves:

            # copying playing field so we avoid editing actual game and are just simulating what could happen
            simulated_game_field = copy.deepcopy(game_field)
            self.move_execution(move, simulated_game_field)

            # for better navigation chained jumps will be stored in trees
            simulated_moves_tree = MovesTree()
            simulated_move_trees_pointers.append(simulated_moves_tree)

            root_move = Move(move[0], move[1])
            simulated_moves_tree.set_root_move(root_move)
            root_move.set_figure(simulated_game_field[root_move.data[0]])
            root_move.update_friends_and_foes()

            self._simulation_subprocess(root_move, copy.deepcopy(simulated_game_field))


    def _simulation_subprocess(self, root_move, simulated_game_field):
        # consifering all cases for regular stones
        if root_move.figure in ['w', 'b']:
            close_vicinity = self.get_circle(simulated_game_field, diameter=1)
            further_vicinity = self.get_circle(simulated_game_field, diameter=2)
            for closer_sq in close_vicinity:
                for further_sq in further_vicinity:
                    if (self.get_move_direction([root_move[0], closer_sq]) == self.get_move_direction([root_move[0], further_sq]) and
                        simulated_game_field[closer_sq] in root_move.enemies and
                        simulated_game_field[further_sq] is None):
                            root_move.force_birth(further_sq)

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