from figure.figure import Figure
from constants import X, Y


class Bishop(Figure):
    def __init__(self, is_black, position):
        super().__init__(is_black, position)
        self.symbol = "B"

    def __str__(self):
        if self.is_black:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    def validate_move(self, position):
        vertical_diff = abs(self.position[X]-position[X])
        horizontal_diff = abs(self.position[Y]-position[Y])

        if vertical_diff == horizontal_diff:
            return True

        return False

    @classmethod
    def make_instances(cls):
        return [Bishop(True, (0, 2)), Bishop(True, (0, 5)), Bishop(False, (7, 2)), Bishop(False, (7, 5))]
