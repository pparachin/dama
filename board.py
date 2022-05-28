
class Board:

    def game_field_to2D(field):
        ranksToRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, "5" : 3, "6" : 2, "7" : 1, "8" : 0}
        filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "h" : 7}
        count = -1
        board = []
        for dimension in range(8):
            board.append(["-", "-", "-", "-", "-", "-", "-", "-",])

        for square in range(len(field)):
            row = ranksToRows.get(f"{list(field.keys())[square][1]}")
            col = filesToCols.get(f"{list(field.keys())[square][0]}")
            if square % 8 == 0:
                count += 1
            if list(field.values())[square] != None:
                board[row][col] = list(field.values())[square]

        return board
