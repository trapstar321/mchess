from datetime import datetime
from constants import X, Y
from figure.blank import Blank


class Move:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.time = datetime.now

    def validate(self, board):
        valid = self.source.validate_move(self.target.position, board.board[self.target.position[X]][self.target.position[Y]])

        if valid:
            moves = self.source.move_positions(self.target.position)

            for move in moves[1:]:
                # move is not valid if target is of same team
                if not isinstance(board.board[move[X]][move[Y]], Blank) and self.source.is_black == self.target.is_black:
                    valid = False
                    break

        return valid
