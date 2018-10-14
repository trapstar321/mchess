from figure.figure import Figure


class Queen(Figure):
    def __init__(self, is_black, position):
        super().__init__(is_black, position)
        self.symbol = "Q"

    def __str__(self):
        if self.is_black:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    @classmethod
    def make_instances(cls):
        return [Queen(True, (0, 3)), Queen(False, (7, 3))]
