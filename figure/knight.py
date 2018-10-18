from figure.figure import Figure
from constants import X, Y, BLACK, WHITE
from os.path import join as combine_path


class Knight(Figure):
    def __init__(self, side, position):
        super().__init__(side, position)
        self.symbol = "K"

    def __str__(self):
        if self.side == BLACK:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    def validate_move(self, board, new_position, target):
        # one axis must be 2x and other 1x in difference
        vertical_diff = abs(self.position[X] - new_position[X])
        horizontal_diff = abs(self.position[Y] - new_position[Y])

        valid = False

        if (vertical_diff == 2 and horizontal_diff == 1) or (vertical_diff == 1 and horizontal_diff == 2):
            valid = True
        else:
            valid = False

        if valid:
            return super().validate_move(board, new_position, target)
        else:
            return valid

    def move_direction(self, new_position, axis):
        if new_position[axis]>self.position[axis]:
            return 1
        else:
            return -1

    def move_positions(self, new_position):
        moves = (self.position, new_position)
        return moves

    @classmethod
    def make_instances(cls):
        return [Knight(BLACK, (0, 1)), Knight(BLACK, (0, 6)), Knight(WHITE, (7, 1)), Knight(WHITE, (7, 6))]

    def icon_path(self):
        return combine_path(Figure.base_icon_path, "knight_black.png") \
            if self.side == BLACK else combine_path(Figure.base_icon_path, "knight_white.png")
