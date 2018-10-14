from figure.figure import Figure


class Bishop(Figure):
    def __init__(self, is_black, position):
        super().__init__(is_black, position)
        self.symbol = "B"

    def __str__(self):
        if self.is_black:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    @classmethod
    def make_instances(cls):
        return [Bishop(True, (0, 2)), Bishop(True, (0, 5)), Bishop(False, (7, 2)), Bishop(False, (7, 5))]
