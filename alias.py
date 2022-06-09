from enum import Enum


class PlayerColor(Enum):
    BLACK = 0
    WHITE = 1


class GameDirection(Enum):
    WHITE_IS_UP = 0
    WHITE_IS_DOWN = 1


class StoneColor(Enum):
    BLACK = 0
    WHITE = 1


class PlayerType(Enum):
    PLAYER = 0
    PC = 1
