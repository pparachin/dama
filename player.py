class Player:

    def __init__(self, color, typ, score):
        self._color = color
        self._typ = typ
        self._figures = []
        self._score = score

    def get_score(self):
        return self._score

    def set_score(self, score):
        self._score = score

    def get_color(self):
        return self._color

