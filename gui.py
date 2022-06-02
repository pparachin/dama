import pygame as pg
from validator import Validator
from alias import PlayerColor
from alias import GameDirection


class GUI:

    def __init__(self, WIDTH, HEIGHT, DIMENSION, SQ_SIZE, images, FPS, WHITE, BLACK, RED, SWIDTH, board):
        self._WIDTH = WIDTH
        self._HEIGHT = HEIGHT
        self._DIMENSION = DIMENSION  # dimensions of a checkers board are 8x8
        self._SQ_SIZE = SQ_SIZE  # size of one square in the board
        self._images = images
        self._FPS = FPS
        self._WHITE = WHITE
        self._BLACK = BLACK
        self._RED = RED
        self._SWIDTH = SWIDTH  # width of the score board window
        pg.display.set_caption("CHECKERS by team PINK")  # title of the game
        self._board = board

    def load_images(self):
        self._images["b"] = pg.image.load("data/b.png")  # loads image from the file
        self._images["b"] = pg.transform.scale(self._images["b"], (
            self._SQ_SIZE, self._SQ_SIZE))  # scales the image to the size of one square
        self._images["bb"] = pg.image.load("data/bb.png")
        self._images["bb"] = pg.transform.scale(self._images["bb"], (self._SQ_SIZE, self._SQ_SIZE))
        self._images["w"] = pg.image.load("data/w.png")
        self._images["w"] = pg.transform.scale(self._images["w"], (self._SQ_SIZE, self._SQ_SIZE))
        self._images["ww"] = pg.image.load("data/ww.png")
        self._images["ww"] = pg.transform.scale(self._images["ww"], (self._SQ_SIZE, self._SQ_SIZE))
        self._images["wood"] = pg.image.load("data/wood.png")
        self._images["homescreen"] = pg.image.load("data/homescreen.png")

    def draw_game_state(self, screen, selectedSQ, board, valid_moves):
        self.draw_board(screen)  # draw squares on the board
        self.highlight_SQ(screen, selectedSQ, board, valid_moves)  # highlights selected square
        self.draw_pieces(screen, self._board)  # draw pieces on the top of the squares
        self.draw_score(screen, 0, 0)  # draw players score on the right window

    def draw_board(self, screen):
        screen.fill(self._BLACK)
        for row in range(self._DIMENSION):
            for col in range(row % 2, self._DIMENSION, 2):
                pg.draw.rect(screen, self._WHITE,
                             (col * self._SQ_SIZE, row * self._SQ_SIZE, self._SQ_SIZE, self._SQ_SIZE))

    def draw_pieces(self, screen, board):
        for row in range(self._DIMENSION):
            for col in range(self._DIMENSION):
                piece = board[row][col]
                if piece != "-":
                    screen.blit(self._images[piece],
                                (col * self._SQ_SIZE, row * self._SQ_SIZE, self._SQ_SIZE, self._SQ_SIZE))

    def draw_score(self, screen, black_score, white_score):
        screen.blit(self._images["wood"], (self._WIDTH, 0, self._SWIDTH, self._HEIGHT))
        screen.blit(self._images["ww"], (self._WIDTH + 10, 0))
        screen.blit(self._images["bb"], (self._WIDTH + 140, 0))
        player_font = pg.font.Font("data/FROSTBITE.ttf", 30)
        quit_game = player_font.render("QUIT GAME", True, self._RED)
        screen.blit(quit_game, (self._WIDTH + 30, 750))

        score_font = pg.font.Font("data/FROSTBITE.ttf", 70)
        b_score = score_font.render("{%d}" % int(black_score), True, self._WHITE)
        w_score = score_font.render("{%d}" % int(white_score), True, self._WHITE)
        screen.blit(w_score, (self._WIDTH + 40, 120)) if white_score < 10 else screen.blit(w_score,
                                                                                           (self._WIDTH + 25, 120))
        screen.blit(b_score, (self._WIDTH + 165, 120)) if black_score < 10 else screen.blit(b_score,
                                                                                            (self._WIDTH + 150, 120))

    def menu(self, screen):
        red = self._RED

        screen.blit(self._images["homescreen"], (0, 0, self._WIDTH, self._HEIGHT))
        screen.blit(self._images["wood"], (self._WIDTH, 0, self._SWIDTH, self._HEIGHT))

        white_k = pg.image.load("data/ww.png")
        screen.blit(white_k, (200, 265))

        black_k = pg.image.load("data/bb.png")
        screen.blit(black_k, (330, 300))

        head_line_font = pg.font.Font("data/FROSTBITE.ttf", 125)
        head_line = head_line_font.render("CHECKERS", True, red)
        screen.blit(head_line, (15, 170))

        credit_font = pg.font.Font("data/FROSTBITE.ttf", 50)
        credit = credit_font.render("Created by team PINK", True, red)
        screen.blit(credit, (100, 490))

        player_font = pg.font.Font("data/FROSTBITE.ttf", 30)
        one_player = player_font.render("Player vs PC", True, red)
        screen.blit(one_player, (self._WIDTH + 10, 50))
        screen.blit(self._images["b"], (self._WIDTH + 50, 100))
        screen.blit(self._images["ww"], (self._WIDTH + 100, 120))

        two_player = player_font.render("Two players", True, red)
        screen.blit(two_player, (self._WIDTH + 10, 250))
        screen.blit(self._images["bb"], (self._WIDTH + 50, 300))
        screen.blit(self._images["ww"], (self._WIDTH + 100, 320))

        load_game = player_font.render("LOAD GAME", True, red)
        screen.blit(load_game, (self._WIDTH + 30, 700))

        quitGame = player_font.render("QUIT GAME", True, red)
        screen.blit(quitGame, (self._WIDTH + 30, 750))

    def highlight_SQ(self, screen, selectedSQ, board, validMoves):
        validator = Validator()
        if selectedSQ != () and selectedSQ[1] < 8:
            r = selectedSQ[0]
            c = selectedSQ[1]
            if board[r][c] != "-":
                s = pg.Surface((self._SQ_SIZE, self._SQ_SIZE))
                s.set_alpha(100)
                s.fill(pg.Color("blue"))
                screen.blit(s, (self._SQ_SIZE * c, self._SQ_SIZE * r))

                s.fill(pg.Color("yellow"))
                for move in validMoves:
                    if selectedSQ == validator.get_rowcol_from_sq_string(move[0]):
                        screen.blit(s, (self._SQ_SIZE * validator.get_rowcol_from_sq_string(move[1])[1],
                                        self._SQ_SIZE * validator.get_rowcol_from_sq_string(move[1])[0]))

    def run_game(self):
        pg.init()
        validator = Validator()
        screen = pg.display.set_mode((self._WIDTH + self._SWIDTH, self._HEIGHT))
        clock = pg.time.Clock()
        self.load_images()
        self.menu(screen)
        selectedSQ = ()  # last clicked square (row, col)
        finalSQ = ()
        valid_moves = []
        player_clicks = []  # most recent 2 clicks of the player
        run = True

        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    location = pg.mouse.get_pos()  # (x, y) position of mouse clicked
                    col = int(location[0] // self._SQ_SIZE)
                    row = int(location[1] // self._SQ_SIZE)
                    valid_moves = validator.find_all_valid_moves(
                        validator.translate_GUI_board_to_Validator_board(self._board), PlayerColor.WHITE)

                    # for move in valid_moves:
                    #     if move[0] == Validator.get_sq_string_from_2D_board(row, col):
                    #         finalSQ[0] = Validator.get_rowcol_from_sq_string(move[-1])[0]
                    #         finalSQ[1] = Validator.get_rowcol_from_sq_string(move[-1])[1]

                    if selectedSQ == (row, col):  # selected square is the same as previous one
                        selectedSQ = ()  # deselect
                        player_clicks = []
                    else:
                        selectedSQ = (row, col)
                        player_clicks.append(selectedSQ)
                    if len(player_clicks) == 2:  # check if it was 2nd click
                        pass

            self.draw_game_state(screen, selectedSQ, self._board, valid_moves)
            clock.tick(self._FPS)
            pg.display.flip()

        pg.quit()
