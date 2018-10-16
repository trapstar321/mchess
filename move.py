from datetime import datetime
from constants import X, Y
from figure.blank import Blank


class Move:
    def __init__(self, figure, position):
        self.figure = figure
        self.target_position = position
        self.time = datetime.now

    def validate(self, board):
        valid = self.figure.validate_move(self.target_position)

        if valid and not self.figure.can_skip_figures():
            moves = self.figure.move_positions(self.target_position)

            for move in moves[1:-1]:
                if not isinstance(board.board[move[X]][move[Y]], Blank):
                    valid = False
                    break

        return valid
