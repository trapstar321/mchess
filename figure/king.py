from figure.figure import Figure
from constants import X, Y
from os.path import join as combine_path


class King(Figure):
    def __init__(self, is_black, position):
        super().__init__(is_black, position)
        self.symbol = "K"

    def __str__(self):
        if self.is_black:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    def validate_move(self, board, new_position, target):
        # one cell forward is ok, also +1/-1 in diagonal
        horizontal_movement = abs(new_position[Y]-self.position[Y])
        vertical_movement = abs(new_position[X] - self.position[X])

        valid = False

        if horizontal_movement in (0, 1) and vertical_movement in (0, 1):
            valid = True
        else:
            valid = False

        if valid:
            return super().validate_move(board, new_position, target)
        else:
            return valid

    def move_positions(self, new_position):
        moves = (self.position, new_position)
        return moves

    @classmethod
    def make_instances(cls):
        return [King(True, (0, 4)), King(False, (7, 4))]

    def icon_path(self):
        return combine_path(Figure.base_icon_path, "king_black.png") \
            if self.is_black else combine_path(Figure.base_icon_path, "king_white.png")

