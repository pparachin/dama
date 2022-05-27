from alias import PlayerColor
from alias import GameDirection


class Validator():


    def __init__(self):
        pass


    def validate_base_setup(self, game_file_path):
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

                elif setup_v2:
                    for line in game_file_contents:
                        if line not in base_setups[1]:
                            output = 1
                            break
                    output = 0

                else:
                    output = 1
                
                game_file.close()

        except FileNotFoundError:
            output = 2

        return output


    def find_all_valid_moves(self, playing_field, player_to_turn, game_direction):
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
        moves = [] # contains touples (from, to)

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
                        if (ord(square[0]) - 61 - i) >= 0:
                            cL = letters[letters.index(square[0]) - i]
                        if (ord(square[0]) - 61 + i) <= (len(letters) - 1):
                            cR = letters[letters.index(square[0]) + i]
                        if (int(square[1]) - i) >= 1:
                            lD = int(square[1]) - i
                            lD = str(lD)
                        if (int(square[1]) + i) <= 8:
                            lU = int(square[1]) + i
                            lU = str(lU)

                        # appending moves considering game direction (which player started up)
                        if (game_direction == GameDirection.WHITE_IS_UP and player_to_turn == PlayerColor.WHITE) or (game_direction == GameDirection.WHITE_IS_DOWN and player_to_turn == PlayerColor.BLACK):
                            if cL and lD:
                                moves.append( (square, (cL + lD)) )
                            if cR and lD:
                                moves.append( (square, (cR + lD)) )
                        else:
                            if cL and lU:
                                moves.append( (square, (cL + lU)) )
                            if cR and lU:
                                moves.append( (square, (cR + lU)) )

        # removing moves leading to squares occupated by own figures
        moves_to_be_removed = []
        for move in moves:
            if playing_field[move[1]] in figures_for_evaluation:
                moves_to_be_removed.append(move)
        for move in moves_to_be_removed:
            moves.remove(move)

        return output