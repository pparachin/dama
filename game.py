from player import Player
from alias import PlayerColor, PlayerType, StoneColor
from gui import GUI
from alias import GameDirection
from validator import Validator
from stone import Stone
from lady import Lady
from move_tree import MovesTree
from move_tree import Move


class Game:

    def __init__(self, type_of_game, status, is_new_game=True):
        self._is_new_game = is_new_game
        self._type_of_game = type_of_game
        self.status = status
        self.validator = Validator()
        self.game_field = self.generate_game_field_2("data/moves.csv")
        self.players = []
        self._figures = []
        self.game(self.status, self.validator)
        self.player_to_turn = None

    def get_player_to_turn(self):
        return self.player_to_turn

    def next_turn(self, players):
        if self.player_to_turn is PlayerColor.WHITE: self.player_to_turn = PlayerColor.BLACK
        elif self.player_to_turn is PlayerColor.BLACK: self.player_to_turn = PlayerColor.WHITE

    def game(self, status, validator):
        gui = GUI(WIDTH=800, HEIGHT=800, DIMENSION=8, SQ_SIZE=100, images={}, FPS=30, WHITE=(255, 255, 255),
                  BLACK=(0, 0, 0), RED=(255, 0, 52), SWIDTH=250,
                  board=self.game_field)

        typ = gui.menu_run(status)

        if typ == 0:
            self._type_of_game = typ
            self.players.append(Player(PlayerColor.WHITE, PlayerType.PLAYER, 0))
            self.players.append(Player(PlayerColor.BLACK, PlayerType.PC, 0))
            self.status = True
            self.player_to_turn = self.players[0].get_color()
            print(self.player_to_turn)
            gui.run_game(validator, self.status, self.players, self.game_field, self, self.player_to_turn)
        elif typ == 1:
            self._type_of_game = typ
            self.players.append(Player(PlayerColor.WHITE, PlayerType.PLAYER, 0))
            self.players.append(Player(PlayerColor.BLACK, PlayerType.PLAYER, 0))
            self.status = True
            self.player_to_turn = self.players[0].get_color()
            gui.run_game(validator, self.status, self.players, self.game_field, self, self.player_to_turn)

    def generate_game_field_2(self, game_file_path):
        if self._is_new_game:
            if self.validator.validate_base_setup(game_file_path) != 0:
                return None
            else:
                self._is_new_game = False

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
            #create figure and place it on the board
            position = key
            color = StoneColor.WHITE if temp_dict_field[key] in ['w', 'ww'] else StoneColor.BLACK
            status = 1
            label = temp_dict_field[key]
            temp_figure = Lady(position, color, status, label) if is_lady else Stone(position, color, status, label)
            rowcol = self.validator.get_rowcol_from_sq_string(key)
            row, col = rowcol[0], rowcol[1]
            temp_2D_field[row][col] = temp_figure

        return temp_2D_field

    def get_players(self):
        return self.players

    def get_status(self):
        return self.status

    def sync_figure_positions_with_field(self, input_field):
        field = input_field
        for figure in self._figures:
            for r in range(8):
                for c in range(8):
                    if field[r][c] is figure:
                        figure.set_position(self.validator.get_sq_string_from_2D_board(r, c))

    def get_game_field(self):
        return self.game_field

    def check_win(self, player_to_turn):
        if not self.validator.find_all_valid_moves(self, player_to_turn):
            return True
        else:
            return False
