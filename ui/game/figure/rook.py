from ui.game.figure.figure import Figure
from ui.game.figure.movement.horizontal import *
from os.path import join as combine_path
from constants import BLACK, WHITE


class Rook(Figure):
    def __init__(self, side, position):
        super().__init__(side, position)
        self.symbol = "R"

    def __str__(self):
        if self.side == BLACK:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    def validate_move(self, board, new_position, target):
        if validate_move(self.position, new_position):
            return super().validate_move(board, new_position, target)

        return False

    def move_positions(self, new_position):
        return move_positions(self.position, new_position)

    @classmethod
    def make_instances(cls):
        return [Rook(BLACK, (0, 0)), Rook(BLACK, (0, 7)), Rook(WHITE, (7, 0)), Rook(WHITE, (7, 7))]

    def icon_path(self):
        return combine_path(Figure.base_icon_path, "rook_black.png") \
            if self.side == BLACK else combine_path(Figure.base_icon_path, "rook_white.png")
