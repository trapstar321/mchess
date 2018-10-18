from datetime import datetime
from constants import X, Y
from figure.blank import Blank


class Move:
    def __init__(self, source, target, turn):
        self.source = source
        self.target = target
        self.time = datetime.now
        self.turn = turn

    def validate(self, board):
        if self.turn != self.source.side:
            return False

        return self.source.validate_move(board, self.target.position,
                                         self.target)
