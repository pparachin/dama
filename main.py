from gui import GUI
from board import Board 
from validator import Validator


def main():
    pass

if __name__ == "__main__":
    GUI.run_game(GUI(800,800,8,100,{},30,(255,255,255),(0,0,0), (255, 0, 52), 250, Board.game_field_to2D(Validator.generate_game_field("data/moves.csv"))))
