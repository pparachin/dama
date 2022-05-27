import pygame as pg

class GUI:

  def __init__(self, WIDTH, HEIGHT, DIMENSION, SQ_SIZE, IMAGES, FPS, WHITE, BLACK):

    self._WIDTH = WIDTH
    self._HEIGHT = HEIGHT
    self._DIMENSION = DIMENSION  #dimensions of a checkers board are 8x8
    self._SQ_SIZE = SQ_SIZE #size of one square in the board
    self._IMAGES = IMAGES
    self._FPS = FPS
    self._WHITE = WHITE
    self._BLACK = BLACK
    pg.display.set_caption("CHECKERS by team PINK") #title of the game

  def loadImages(self):
    self._IMAGES["b-"] = pg.image.load("Checkers/images/b.png") #loads image from the file
    self._IMAGES["b-"] = pg.transform.scale(self._IMAGES["b-"], (self._SQ_SIZE, self._SQ_SIZE)) #scales the image to the size of one square
    self._IMAGES["bb"] = pg.image.load("Checkers/images/bb.png")
    self._IMAGES["bb"] = pg.transform.scale(self._IMAGES["bb"], (self._SQ_SIZE, self._SQ_SIZE))
    self._IMAGES["w-"] = pg.image.load("Checkers/images/w.png")
    self._IMAGES["w-"] = pg.transform.scale(self._IMAGES["w-"], (self._SQ_SIZE, self._SQ_SIZE))
    self._IMAGES["ww"] = pg.image.load("Checkers/images/ww.png")
    self._IMAGES["ww"] = pg.transform.scale(self._IMAGES["ww"], (self._SQ_SIZE, self._SQ_SIZE))

  def drawGameState(self, screen, gs):
    self.drawBoard(screen) #draw squares on the board
    self.drawPieces(screen, gs.board) #draw pieces on the top of the squares

  def drawBoard(self, screen):
    screen.fill(self._BLACK)
    for row in range(self._DIMENSION):
      for col in range(row % 2, self._DIMENSION, 2):
        pg.draw.rect(screen, self._WHITE, (col*self._SQ_SIZE, row*self._SQ_SIZE, self._SQ_SIZE, self._SQ_SIZE))

  def drawPieces(self, screen, board):
    for row in range(self._DIMENSION):
      for col in range(self._DIMENSION):
        piece = board[row][col]
        if piece != "--" and piece != "xx":
          screen.blit(self._IMAGES[piece], (col*self._SQ_SIZE, row*self._SQ_SIZE, self._SQ_SIZE, self._SQ_SIZE))