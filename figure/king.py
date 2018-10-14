from figure.figure import Figure
from constants import X, Y


class King(Figure):
    def __init__(self, is_black, position):
        super().__init__(is_black, position)
        self.symbol = "K"

    def __str__(self):
        if self.is_black:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    def validate_move(self, position):
            #one cell forward is ok, also +1/-1 in diagonal
        horizontal_movement = abs(position[Y]-self.position[Y])
        vertical_movement = abs(position[X] - self.position[X])

        if horizontal_movement in (0, 1) and vertical_movement in (0, 1):
            return True

        return False

    @classmethod
    def make_instances(cls):
        return [King(True, (0, 4)), King(False, (7, 4))]

