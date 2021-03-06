from ui.game.figure.figure import Figure
from os.path import join as combine_path
from constants import WHITE


class Blank(Figure):
    def __init__(self, side, position):
        super().__init__(side, position)
        self.symbol = "  "
        self.is_blank = True

    def __str__(self):
        return self.symbol

    @classmethod
    def make_instances(cls):
        instances = []
        for x in range(2, 6):
            for y in range(0, 8):
                instances.append(Blank(WHITE, (x, y)))
        return instances

    def icon_path(self):
        return combine_path(Figure.base_icon_path, "blank.png")