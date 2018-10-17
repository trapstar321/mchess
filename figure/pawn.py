from figure.figure import Figure
from constants import X, Y
from os.path import join as combine_path
from figure.blank import Blank


class Pawn(Figure):
    def __init__(self, is_black, position):
        super().__init__(is_black, position)
        self.symbol = "P"

    def __str__(self):
        if self.is_black:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    def allowed_vertical_direction(self):
        if self.is_black:
            return 1
        else:
            return -1

    def validate_move(self, new_position, target):
        # can move two cells only if is at beginning and horizontal hasn't changed
        if self.is_at_beginning() \
                and new_position[Y] == self.position[Y]:
            # two cells forward is ok
            if new_position[X] - self.position[X] == self.allowed_vertical_direction()*2:
                return True
            elif new_position[X] - self.position[X] == self.allowed_vertical_direction():
                return True
        else:
            # one cell forward is ok
            # diagonal movement only if its enemy figure
            horizontal_movement = abs(new_position[Y]-self.position[Y])
            vertical_movement = new_position[X] - self.position[X]
            if horizontal_movement == 0:
                # black moves from 0 to 7 only if target is blank
                if self.is_black:
                    if vertical_movement == 1:
                        return False if not isinstance(target, Blank) else True
                    else:
                        return False
                # white moves from 7 to 0 only if target is blank
                elif not self.is_black:
                    if vertical_movement == -1:
                        return False if not isinstance(target, Blank) else True
            elif horizontal_movement == 1:
                if new_position[X] - self.position[X] == self.allowed_vertical_direction()*1:
                    if not isinstance(target, Blank) and not target.is_black == self.is_black:
                        return True
                    else:
                        return False

        return False

    def move_positions(self, new_position):
        vertical_diff = abs(self.position[X] - new_position[X])

        moves = [self.position]

        if vertical_diff == 2:
            moves.append((self.position[X]+(-1 if self.position[X] > new_position[X] else 1), self.position[Y]))

        moves.append(new_position)
        return tuple(moves)

    @classmethod
    def make_instances(cls):
        return [
            Pawn(True, (1, 0)), Pawn(True, (1, 1)), Pawn(True, (1, 2)), Pawn(True, (1, 3)),
            Pawn(True, (1, 4)), Pawn(True, (1, 5)), Pawn(True, (1, 6)), Pawn(True, (1, 7)),

            Pawn(False, (6, 0)), Pawn(False, (6, 1)), Pawn(False, (6, 2)), Pawn(False, (6, 3)),
            Pawn(False, (6, 4)), Pawn(False, (6, 5)), Pawn(False, (6, 6)), Pawn(False, (6, 7))
        ]

    def icon_path(self):
        return combine_path(Figure.base_icon_path, "pawn_black.png") \
            if self.is_black else combine_path(Figure.base_icon_path, "pawn_white.png")
