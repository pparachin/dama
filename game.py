from random import randint
from player import Player
from alias import PlayerColor, PlayerType, StoneColor
from gui import GUI
from validator import Validator
from stone import Stone
from lady import Lady
from move_tree import get_moves as treemoves
from custom_errors import *


class Game:

    def __init__(self, type_of_game, status, is_new_game=True, file_path="data/moves.csv"):
        self._is_new_game = is_new_game
        self._type_of_game = type_of_game
        self.status = status
        self.validator = Validator()
        self._figures = []
        self.game_field = self.generate_game_field(file_path)
        self.players = []
        self.game(self.status, self.validator)
        self.player_to_turn = None

    def game(self, status, validator):
        gui = GUI(WIDTH=800, HEIGHT=800, DIMENSION=8, SQ_SIZE=100, images={}, FPS=30, WHITE=(255, 255, 255),
                  BLACK=(0, 0, 0), RED=(255, 0, 52), SWIDTH=250,
                  board=self.game_field)

        self._type_of_game = gui.menu_run(status)
        self.players.append(Player(PlayerColor.WHITE, PlayerType.PLAYER, 0))

        if self._type_of_game == 0:
            self.players.append(Player(PlayerColor.BLACK, PlayerType.PC, 0))
            self.status = True
            self.player_to_turn = self.players[0].get_color()
            gui.run_game(validator, self.status, self.players, self.game_field, self, self.player_to_turn)
        elif self._type_of_game == 1:
            self.players.append(Player(PlayerColor.BLACK, PlayerType.PLAYER, 0))
            self.status = True
            self.player_to_turn = self.players[0].get_color()
            gui.run_game(validator, self.status, self.players, self.game_field, self, self.player_to_turn)

    def next_turn(self):
        output = None
        
        if self.player_to_turn is PlayerColor.WHITE:
            self.player_to_turn = PlayerColor.BLACK
            output = self.player_to_turn
        elif self.player_to_turn is PlayerColor.BLACK:
            self.player_to_turn = PlayerColor.WHITE
            output = self.player_to_turn

        # FOR DEBUGGING ONLY
        # for _fig in self._figures:
        #     print(f"{_fig.show()}:{treemoves(_fig.moves_tree)}")
        # print("--------------------")

        return output

    def generate_game_field(self, game_file_path):
        if self._is_new_game:
            error_state = self.validator.validate_base_setup(game_file_path)
            if error_state == 0:
                self._is_new_game = False
            elif self.validator.validate_base_setup(game_file_path) == 1:
                raise IncorrectBaseGameSetupError()
            elif self.validator.validate_base_setup(game_file_path) == 2:
                raise FailedToReadFileError()
        else:
            error_state = self.validator.validate_any_setup(game_file_path)
            if error_state == 1:
                raise SetupNotMatchingRulesError()
            elif error_state == 2:
                raise InvalidFigurePositionError()
            elif error_state == 3:
                raise MoreFiguresOnOneTileError()
            elif error_state == 4:
                raise FailedToReadFileError()

        temp_dict_field = self.validator.old_generate_game_field(game_file_path)
        temp_2D_field = self.validator.game_field_to2D(temp_dict_field)

        for key in temp_dict_field.keys():
            # skip empty squares
            if temp_dict_field[key] is None:
                continue
            # different object for lady/queen/king etc.
            is_lady = False
            if temp_dict_field[key] in ['bb', 'ww']:
                is_lady = True
            # create figure and place it on the board
            position = key
            color = StoneColor.WHITE if temp_dict_field[key] in ['w', 'ww'] else StoneColor.BLACK
            status = 1
            label = temp_dict_field[key]
            temp_figure = Lady(position, color, status, label) if is_lady else Stone(position, color, status, label)
            row_col = self.validator.get_rowcol_from_sq_string(key)
            row, col = row_col[0], row_col[1]
            temp_2D_field[row][col] = temp_figure
            # add figure to actual game for iterating purposes
            self._figures.append(temp_figure)
            
        return temp_2D_field

    def sync_figure_positions_with_field(self, input_field):
        field = input_field
        for figure in self._figures:
            for r in range(8):
                for c in range(8):
                    if field[r][c] is figure:
                        figure.set_position(self.validator.get_sq_string_from_2D_board(r, c))

    def check_win(self, player_to_turn):
        if not self.validator.find_all_valid_moves(self, player_to_turn):
            return True
        else:
            return False

    def AI_move(self, validator, game, player_to_turn):
        possible_moves = validator.find_all_valid_moves(game, player_to_turn)
        max_num = len(possible_moves) - 1
        rnd = randint(0, max_num)
        validator.move_execution([possible_moves[rnd][0], possible_moves[rnd][-1]], game.get_game_field(), player_to_turn, game.get_players())
        return True

    # Getters

    def get_players(self):
        return self.players

    def get_status(self):
        return self.status

    def get_player_to_turn(self):
        return self.player_to_turn

    def get_game_field(self):
        return self.game_field

    def get_game_type(self):
        return self._type_of_game
