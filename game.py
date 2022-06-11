from player import Player
from alias import PlayerColor, PlayerType, StoneColor
from gui import GUI
from alias import GameDirection
from validator import Validator
from stone import Stone
from lady import Lady


class Game:

    def __init__(self, type_of_game, status):
        self._figures = []
        self._type_of_game = type_of_game
        self.status = status
        validator = Validator()
        self.game_field = self.generate_game_field_2("data/moves.csv")
        self._players = []
        self.game(self.status, validator)

    def add_figure(self, figure):
        self._figures.append(figure)

    def game(self, status, validator):
        gui = GUI(WIDTH=800, HEIGHT=800, DIMENSION=8, SQ_SIZE=100, images={}, FPS=30, WHITE=(255, 255, 255),
                  BLACK=(0, 0, 0), RED=(255, 0, 52), SWIDTH=250,
                  board=self.game_field)

        typ = gui.menu_run(status)

        if typ == 0:
            self._type_of_game = typ
            self._players.append(Player(PlayerColor.WHITE, PlayerType.PLAYER, 0))
            self._players.append(Player(PlayerColor.BLACK, PlayerType.PC, 0))
            self.status = True
            gui.run_game(validator, self.status, self._players, self.game_field)
        elif typ == 1:
            self._type_of_game = typ
            self._players.append(Player(PlayerColor.WHITE, PlayerType.PLAYER, 0))
            self._players.append(Player(PlayerColor.BLACK, PlayerType.PLAYER, 0))
            self.status = True
            gui.run_game(validator, self.status, self._players, self.game_field)

    @staticmethod
    def generate_game_field(game_file_path):
        """
        This function opens .csv file and outputs corresponding "game field dictionary".
        !!! Note: This function function does NOT validate if the text inside file is correct. !!!
        """
        temp_playing_field = []
        playing_field = []
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for letter in letters:
            for number in range(1, 9):
                tag = str(letter) + str(number)
                figure = None
                temp_playing_field.append([tag, figure])

        # putting figures in
        try:
            with open(game_file_path) as game_file:
                game_file_contents = game_file.read().splitlines()
                for line in game_file_contents:
                    line = line.split(',')
                    for point in temp_playing_field:
                        if line[0] == point[0]:
                            if line[1] == "w":
                                playing_field.append([line[0], Stone(line[0], StoneColor.WHITE, 1, "w", 0)])
                            else:
                                playing_field.append([line[0], Stone(line[0], StoneColor.BLACK, 1, "b", 0)])
                game_file.close()
        except FileNotFoundError:
            print("File does not exist!")

        return playing_field

    def generate_game_field_2(self, game_file_path):
        temp_dict_field = self.generate_game_field(game_file_path)
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
            status = True
            label = temp_dict_field[key]
            advantage = None
            temp_figure = Lady(position, color, status, label, advantage) if is_lady else Stone(position, color, status, label, advantage)
            self.add_figure(temp_figure)
            temp_dict_field[self.validator.get_rowcol_from_sq_string(key)] = temp_figure

            return temp_dict_field

    def get_players(self):
        return self._players

    def get_status(self):
        return self.status
