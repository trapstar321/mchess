from figure.figure import Figure
from constants import X, Y

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

    def validate_move(self, position):
        # can move two cells only if horizontal hasn't changed
        if self.is_at_beginning() \
                and position[Y] == self.position[Y]:
            #two cells forward is ok
            if position[X] - self.position[X] == self.allowed_vertical_direction()*2:
                return True
            elif position[X] - self.position[X] == self.allowed_vertical_direction():
                return True
        else:
            #one cell forward is ok, also +1/-1 in diagonal
            diagonal_movement = abs(position[Y]-self.position[Y])
            if diagonal_movement == 1 or diagonal_movement == 0:
                if position[X] - self.position[X] == self.allowed_vertical_direction()*1:
                    return True

        return False


    @classmethod
    def make_instances(cls):
        return [
            Pawn(True, (1, 0)), Pawn(True, (1, 1)), Pawn(True, (1, 2)), Pawn(True, (1, 3)),
            Pawn(True, (1, 4)), Pawn(True, (1, 5)), Pawn(True, (1, 6)), Pawn(True, (1, 7)),

            Pawn(False, (6, 0)), Pawn(False, (6, 1)), Pawn(False, (6, 2)), Pawn(False, (6, 3)),
            Pawn(False, (6, 4)), Pawn(False, (6, 5)), Pawn(False, (6, 6)), Pawn(False, (6, 7))
        ]
