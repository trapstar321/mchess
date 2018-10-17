#from figure.blank import Blank
from constants import X, Y
from PIL import Image, ImageTk


class Figure:
    base_icon_path = "figure/icons"

    def __init__(self, is_black, position):
        self.is_black = is_black
        self.position = position
        self.begin_position = position[X], position[Y]

    def start_position(self):
        pass

    @classmethod
    def make_instances(cls):
        pass

    def validate_move(self, board, new_position, target):
        valid = True
        moves = self.move_positions(self.position)

        # for move in moves[1:-1]:
        #     # move is not valid if target is of same team
        #     if not isinstance(board.board[move[X]][move[Y]], Blank):
        #         valid = False
        #         break
        #
        # if not isinstance(target, Blank) and not target.is_black == self.is_black:
        #     valid = True

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
