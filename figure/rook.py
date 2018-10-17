from figure.figure import Figure
from figure.movement.horizontal import *
from os.path import join as combine_path


class Rook(Figure):
    def __init__(self, is_black, position):
        super().__init__(is_black, position)
        self.symbol = "R"

    def __str__(self):
        if self.is_black:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    def validate_move(self, new_position, target):
        return validate_move(self.position, new_position)

    def move_positions(self, new_position):
        return move_positions(self.position, new_position)

    @classmethod
    def make_instances(cls):
        return [Rook(True, (0, 0)), Rook(True, (0, 7)), Rook(False, (7, 0)), Rook(False, (7, 7))]

    def icon_path(self):
        return combine_path(Figure.base_icon_path, "rook_black.png") \
            if self.is_black else combine_path(Figure.base_icon_path, "rook_white.png")
