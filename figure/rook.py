from figure.figure import Figure
from constants import X, Y


class Rook(Figure):
    def __init__(self, is_black, position):
        super().__init__(is_black, position)
        self.symbol = "R"


    def __str__(self):
        if self.is_black:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    def validate_move(self, position):
        #on of two axis must be equal to original position
        if self.position[X] == position[X] or self.position[Y] == position[Y]:
            return True

        return False

    @classmethod
    def make_instances(cls):
        return [Rook(True, (0, 0)), Rook(True, (0, 7)), Rook(False, (7, 0)), Rook(False, (7, 7))]
