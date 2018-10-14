from constants import X,Y

class Figure:
    def __init__(self, is_black, position):
        self.is_black = is_black
        self.position = position
        self.begin_position = position[X], position[Y]

    def start_position(self):
        pass

    @classmethod
    def make_instances(cls):
        pass

    def move(self, position):
        pass

    def validate_move(self, position):
        pass

    def is_at_beginning(self):
        return self.begin_position[X] == self.position[X] \
            and self.begin_position[Y] == self.position[Y]
