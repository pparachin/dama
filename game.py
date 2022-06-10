from player import Player
from alias import PlayerColor, PlayerType, StoneColor
from gui import GUI
from alias import GameDirection
from validator import Validator
from stone import Stone


class Game:

    def __init__(self, type_of_game, status):
        self._type_of_game = type_of_game
        self.status = status
        validator = Validator()
        self.game_field = self.generate_game_field("data/moves.csv")
        self._players = []
        self.game(self.status, validator)

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
        elif type == 1:
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

    def get_players(self):
        return self._players

    def get_status(self):
        return self.status
