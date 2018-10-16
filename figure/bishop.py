from figure.figure import Figure
from figure.movement.vertical import *
from os.path import join as combine_path

class Bishop(Figure):
    def __init__(self, is_black, position):
        super().__init__(is_black, position)
        self.symbol = "B"

    def __str__(self):
        if self.is_black:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    def validate_move(self, new_position):
        return validate_move(self.position, new_position)

    def move_positions(self, new_position):
        return move_positions(self.position, new_position)

    @classmethod
    def make_instances(cls):
        return [Bishop(True, (0, 2)), Bishop(True, (0, 5)), Bishop(False, (7, 2)), Bishop(False, (7, 5))]

    def icon_path(self):
        return combine_path(Figure.base_icon_path, "bishop_black.png") \
            if self.is_black else combine_path(Figure.base_icon_path, "bishop_white.png")
