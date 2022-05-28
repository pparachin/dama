import pygame as pg



class GUI:

    def __init__(self, WIDTH, HEIGHT, DIMENSION, SQ_SIZE, images, FPS, WHITE, BLACK, RED, SWIDTH, board):
        self._WIDTH = WIDTH
        self._HEIGHT = HEIGHT
        self._DIMENSION = DIMENSION  #dimensions of a checkers board are 8x8
        self._SQ_SIZE = SQ_SIZE #size of one square in the board
        self._images = images
        self._FPS = FPS
        self._WHITE = WHITE
        self._BLACK = BLACK
        self._RED = RED
        self._SWIDTH = SWIDTH #width of the score board window
        pg.display.set_caption("CHECKERS by team PINK") #title of the game
        self._board = board


    def loadimages(self):
        self._images["b"] = pg.image.load("data/b.png") #loads image from the file
        self._images["b"] = pg.transform.scale(self._images["b"], (self._SQ_SIZE, self._SQ_SIZE)) #scales the image to the size of one square
        self._images["bb"] = pg.image.load("data/bb.png")
        self._images["bb"] = pg.transform.scale(self._images["bb"], (self._SQ_SIZE, self._SQ_SIZE))
        self._images["w"] = pg.image.load("data/w.png")
        self._images["w"] = pg.transform.scale(self._images["w"], (self._SQ_SIZE, self._SQ_SIZE))
        self._images["ww"] = pg.image.load("data/ww.png")
        self._images["ww"] = pg.transform.scale(self._images["ww"], (self._SQ_SIZE, self._SQ_SIZE))
        self._images["wood"] = pg.image.load("data/wood.png")
        self._images["homescreen"] = pg.image.load("data/homescreen.png")
      

    def drawGameState(self, screen, selectedSQ, board):
        self.drawBoard(screen) #draw squares on the board
        self.highlightSQ(screen, selectedSQ, board) #highlightes selected square
        self.drawPieces(screen, self._board) #draw pieces on the top of the squares
        self.drawScore(screen, 0, 0) #draw players score on the right window


    def drawBoard(self, screen):
        screen.fill(self._BLACK)
        for row in range(self._DIMENSION):
            for col in range(row % 2, self._DIMENSION, 2):
                pg.draw.rect(screen, self._WHITE, (col*self._SQ_SIZE, row*self._SQ_SIZE, self._SQ_SIZE, self._SQ_SIZE))


    def drawPieces(self, screen, board):
        for row in range(self._DIMENSION):
            for col in range(self._DIMENSION):
                piece = board[row][col]
                if piece != "-":
                    screen.blit(self._images[piece], (col*self._SQ_SIZE, row*self._SQ_SIZE, self._SQ_SIZE, self._SQ_SIZE))


    def drawScore(self, screen, blackScore, whiteScore):
        screen.blit(self._images["wood"], (self._WIDTH, 0, self._SWIDTH, self._HEIGHT))
        screen.blit(self._images["ww"], (self._WIDTH + 10, 0))
        screen.blit(self._images["bb"], (self._WIDTH + 140, 0))
        playerFont = pg.font.Font("data/FROSTBITE.ttf", 30)
        quitGame = playerFont.render("QUIT GAME", True, self._RED)
        screen.blit(quitGame, (self._WIDTH + 30, 750))

        scoreFont = pg.font.Font("data/FROSTBITE.ttf", 70)
        bScore = scoreFont.render("{%d}" % int(blackScore), True, self._WHITE)
        wScore = scoreFont.render("{%d}" % int(whiteScore), True, self._WHITE)
        screen.blit(wScore, (self._WIDTH + 40, 120))  if whiteScore < 10 else screen.blit(wScore, (self._WIDTH + 25, 120))
        screen.blit(bScore, (self._WIDTH + 165, 120)) if blackScore < 10 else screen.blit(bScore, (self._WIDTH + 150, 120))


    def menu(self, screen):
        red = self._RED

        screen.blit(self._images["homescreen"], (0, 0, self._WIDTH, self._HEIGHT))
        screen.blit(self._images["wood"], (self._WIDTH, 0, self._SWIDTH, self._HEIGHT))

        whiteK = pg.image.load("data/ww.png")
        screen.blit(whiteK, (200, 265))

        blackK = pg.image.load("data/bb.png")
        screen.blit(blackK, (330, 300))

        headLineFont = pg.font.Font("data/FROSTBITE.ttf", 125)
        headLine = headLineFont.render("CHECKERS", True, red)
        screen.blit(headLine, (15, 170))

        creditFont = pg.font.Font("data/FROSTBITE.ttf", 50)
        credit = creditFont.render("Created by team PINK", True, red)
        screen.blit(credit, (100, 490))

        playerFont = pg.font.Font("data/FROSTBITE.ttf", 30)
        onePlayer = playerFont.render("Player vs PC", True, red)
        screen.blit(onePlayer, (self._WIDTH + 10, 50))
        screen.blit(self._images["b"], (self._WIDTH + 50, 100))
        screen.blit(self._images["ww"], (self._WIDTH + 100, 120))

        twoPlayer = playerFont.render("Two players", True, red)
        screen.blit(twoPlayer, (self._WIDTH + 10, 250))
        screen.blit(self._images["bb"], (self._WIDTH + 50, 300))
        screen.blit(self._images["ww"], (self._WIDTH + 100, 320))

        loadGame = playerFont.render("LOAD GAME", True, red)
        screen.blit(loadGame, (self._WIDTH + 30, 700))

        quitGame = playerFont.render("QUIT GAME", True, red)
        screen.blit(quitGame, (self._WIDTH + 30, 750))


    def highlightSQ(self, screen, selectedSQ, board):
        if selectedSQ != () and selectedSQ[1] < 8:
            r = selectedSQ[0]
            c = selectedSQ[1]
            if board[r][c] != "-":
                s = pg.Surface((self._SQ_SIZE, self._SQ_SIZE))
                s.set_alpha(100)
                s.fill(pg.Color("blue"))
                screen.blit(s, (self._SQ_SIZE * c, self._SQ_SIZE * r))


    def run_game(self):
        pg.init()
        screen = pg.display.set_mode((self._WIDTH + self._SWIDTH, self._HEIGHT))
        clock = pg.time.Clock()
        self.loadimages()
        self.menu(screen)
        selectedSQ = () #last clicked square (row, col)
        playerClicks = [] #most recent 2 clicks of the player
        run = True

        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    location = pg.mouse.get_pos() #(x, y) position of mouse clicked
                    col = location[0]//self._SQ_SIZE
                    row = location[1]//self._SQ_SIZE
                    if selectedSQ == (row, col): #selected square is the same as previous one
                        selectedSQ = () #deselect
                        playerClicks = []
                    else:
                        selectedSQ = (row, col)
                        playerClicks.append(selectedSQ)
                    if len(playerClicks) == 2: #check if it was 2nd click
                        pass

            self.drawGameState(screen, selectedSQ, self._board)
            clock.tick(self._FPS)
            pg.display.flip()

        pg.quit()

