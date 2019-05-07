from ui.game.figure.figure import Figure
from constants import X, Y, BLACK, WHITE
from os.path import join as combine_path
from ui.game.figure.blank import Blank


class Pawn(Figure):
    def __init__(self, side, position):
        super().__init__(side, position)
        self.symbol = "P"

    def __str__(self):
        if self.side == BLACK:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    def allowed_vertical_direction(self):
        if self.side == BLACK:
            return 1
        else:
            return -1

    def validate_move(self, board, new_position, target):
        valid = False
        # can move two cells only if is at beginning and horizontal hasn't changed
        if self.is_at_beginning() \
                and new_position[Y] == self.position[Y]:
            # two cells forward is ok
            if new_position[X] - self.position[X] == self.allowed_vertical_direction()*2:
                valid = True
            elif new_position[X] - self.position[X] == self.allowed_vertical_direction():
                valid = True
        else:
            # one cell forward is ok
            # diagonal movement only if its enemy figure
            horizontal_movement = abs(new_position[Y]-self.position[Y])
            vertical_movement = new_position[X] - self.position[X]
            if horizontal_movement == 0:
                # black moves from 0 to 7 only if target is blank
                if self.side == BLACK:
                    if vertical_movement == 1:
                        valid = False if not isinstance(target, Blank) else True
                    else:
                        valid = False
                # white moves from 7 to 0 only if target is blank
                elif self.side == WHITE:
                    if vertical_movement == -1:
                        valid = False if not isinstance(target, Blank) else True
            elif horizontal_movement == 1:
                if new_position[X] - self.position[X] == self.allowed_vertical_direction()*1:
                    if not isinstance(target, Blank) and not target.side == self.side:
                        valid = True
                    else:
                        valid = False

        if valid:
            return super().validate_move(board, new_position, target)
        else:
            return valid

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
            Pawn(BLACK, (1, 0)), Pawn(BLACK, (1, 1)), Pawn(BLACK, (1, 2)), Pawn(BLACK, (1, 3)),
            Pawn(BLACK, (1, 4)), Pawn(BLACK, (1, 5)), Pawn(BLACK, (1, 6)), Pawn(BLACK, (1, 7)),

            Pawn(WHITE, (6, 0)), Pawn(WHITE, (6, 1)), Pawn(WHITE, (6, 2)), Pawn(WHITE, (6, 3)),
            Pawn(WHITE, (6, 4)), Pawn(WHITE, (6, 5)), Pawn(WHITE, (6, 6)), Pawn(WHITE, (6, 7))
        ]

    def icon_path(self):
        return combine_path(Figure.base_icon_path, "pawn_black.png") \
            if self.side == BLACK else combine_path(Figure.base_icon_path, "pawn_white.png")
