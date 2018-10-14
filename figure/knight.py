from figure.figure import Figure


class Knight(Figure):
    def __init__(self, is_black, position):
        super().__init__(is_black, position)
        self.symbol = "K"

    def __str__(self):
        if self.is_black:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    @classmethod
    def make_instances(cls):
        return [Knight(True, (0, 1)), Knight(True, (0, 6)), Knight(False, (7, 1)), Knight(False, (7, 6))]
