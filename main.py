from gui import GUI
from validator import Validator


def main():
    validator = Validator()
    GUI.run_game(GUI(800,800,8,100,{},30,(255,255,255),(0,0,0), (255, 0, 52), 250, validator.game_field_to2D(validator.generate_game_field("data/moves.csv"))))
    

if __name__ == "__main__":
    main()