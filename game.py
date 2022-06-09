from player import Player
from alias import PlayerColor, PlayerType, StoneColor
from gui import GUI
from alias import GameDirection
from validator import Validator
from stone import Stone


class Game:

    def __init__(self, type_of_game, status):
        self._type_of_game = type_of_game
        self._status = status
        validator = Validator()
        self._game_field = validator.game_field_to2D(validator.generate_game_field("data/moves.csv"))
        self._players = []
        self._figures = []
        self.game(self._status, validator)

    def game(self, status, validator):
        gui = GUI(WIDTH=800, HEIGHT=800, DIMENSION=8, SQ_SIZE=100, images={}, FPS=30, WHITE=(255, 255, 255),
                  BLACK=(0, 0, 0), RED=(255, 0, 52), SWIDTH=250,
                  board=self._game_field)
        self.figures(self._game_field)

        print(self.get_figures()[0].show())

        typ = gui.menu_run(status)

        if typ == 0:
            self._type_of_game = typ
            self._players.append(Player(PlayerColor.WHITE, PlayerType.PLAYER, 1))
            self._players.append(Player(PlayerColor.BLACK, PlayerType.PC, 0))
            self._status = True
            gui.run_game(validator, self, status, self._players)
        elif type == 1:
            self._type_of_game = typ
            self._players.append(Player(PlayerColor.WHITE, PlayerType.PLAYER, 0))
            self._players.append(Player(PlayerColor.BLACK, PlayerType.PLAYER, 0))
            self._status = True
            gui.run_game(validator, self, status, self._players)

    def figures(self, game_field):
        for i in range(len(game_field)):
            for j in range(len(game_field[i])):
                if game_field[i][j] == 'b':
                    self._figures.append(Stone(i, StoneColor.BLACK, 1, "b", 0))
                elif game_field[i][j] == 'w':
                    self._figures.append(Stone(i, StoneColor.WHITE, 1, "w", 0))
                else:
                    continue

    def get_players(self):
        return self._players

    def get_status(self):
        return self._status

    def get_figures(self):
        return self._figures
