from figure.figure import Figure


class Rook(Figure):
    def __init__(self, is_black, position):
        super().__init__(is_black, position)
        self.symbol = "R"


    def __str__(self):
        if self.is_black:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    @classmethod
    def make_instances(cls):
        return [Rook(True, (0, 0)), Rook(True, (0, 7)), Rook(False, (7, 0)), Rook(False, (7, 7))]
