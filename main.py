from game import Game


def main():
    Game(0, True, is_new_game=True, file_path="data/moves.csv") # BASE GAME SETUP (just uncomment)
    # Game(0, True, is_new_game=False, file_path="data/test.csv") # CUSTOM GAME SETUP


if __name__ == "__main__":
    main()
