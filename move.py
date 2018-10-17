from datetime import datetime
from constants import X, Y
from figure.blank import Blank


class Move:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.time = datetime.now

    def validate(self, board):
        return self.source.validate_move(board, self.target.position,
                                         board.board[self.target.position[X]][self.target.position[Y]])
