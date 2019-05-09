from ui.game.figure.figure import Figure
from constants import X, Y
from os.path import join as combine_path
from constants import BLACK, WHITE


class King(Figure):
    def __init__(self, side, position):
        super().__init__(side, position)
        self.symbol = "K"

    def __str__(self):
        if self.side == BLACK:
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

    def short_name(self):
        return "K"

    @classmethod
    def make_instances(cls):
        return [King(BLACK, (0, 4)), King(WHITE, (7, 4))]

    def icon_path(self):
        return combine_path(Figure.base_icon_path, "king_black.png") \
            if self.side == BLACK else combine_path(Figure.base_icon_path, "king_white.png")

