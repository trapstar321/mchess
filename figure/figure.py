from constants import X, Y
from PIL import Image, ImageTk

class Figure:
    base_icon_path = "figure/icons"

    def __init__(self, side, position):
        self.side = side
        self.position = position
        self.begin_position = position[X], position[Y]
        self.is_blank = False

    def start_position(self):
        pass

    @classmethod
    def make_instances(cls):
        pass

    def validate_move(self, board, new_position, target):
        valid = True
        moves = self.move_positions(new_position)

        # cannot jump across other figures
        for move in moves[1:-1]:
            if not board.board[move[X]][move[Y]].is_blank:
                valid = False
                break

        if valid:
            # if target is not blank then it must be from other team
            if not target.is_blank and not target.side == self.side:
                valid = True
            elif not target.is_blank and target.side == self.side:
                valid = False

        return valid

    def move_positions(self, new_position):
        pass

    def is_at_beginning(self):
        return self.begin_position[X] == self.position[X] \
            and self.begin_position[Y] == self.position[Y]

    def icon_path(self):
        pass

    def load_icon(self):
        return ImageTk.PhotoImage(Image.open(self.icon_path()))
