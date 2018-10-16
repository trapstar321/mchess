from figure.figure import Figure
from constants import X, Y
from os.path import join as combine_path

class Knight(Figure):
    def __init__(self, is_black, position):
        super().__init__(is_black, position)
        self.symbol = "K"

    def __str__(self):
        if self.is_black:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    def validate_move(self, new_position):
        #one axis must be 2x and other 1x in difference
        vertical_diff = abs(self.position[X] - new_position[X])
        horizontal_diff = abs(self.position[Y] - new_position[Y])

        if (vertical_diff == 2 and horizontal_diff == 1) or (vertical_diff == 1 and horizontal_diff == 2):
            return True

        return False

    def move_direction(self, new_position, axis):
        if new_position[axis]>self.position[axis]:
            return 1
        else:
            return -1

    def move_positions(self, new_position):
        #knight does not have move position because he can jump over other figures
        return None

    def can_skip_figures(self):
        return True

    @classmethod
    def make_instances(cls):
        return [Knight(True, (0, 1)), Knight(True, (0, 6)), Knight(False, (7, 1)), Knight(False, (7, 6))]

    def icon_path(self):
        return combine_path(Figure.base_icon_path, "knight_black.png") \
            if self.is_black else combine_path(Figure.base_icon_path, "knight_white.png")
