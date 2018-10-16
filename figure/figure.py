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

    def validate_move(self, new_position):
        pass

    def move_positions(self, new_position):
        pass

    def is_at_beginning(self):
        return self.begin_position[X] == self.position[X] \
            and self.begin_position[Y] == self.position[Y]

    def can_skip_figures(self):
        return False

    def icon_path(self):
        pass

    def load_icon(self):
        return ImageTk.PhotoImage(Image.open(self.icon_path()))
