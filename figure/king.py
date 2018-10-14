from figure.figure import Figure


class King(Figure):
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
        return [King(True, (0, 4)), King(False, (7, 4))]

