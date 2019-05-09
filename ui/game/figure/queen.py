from ui.game.figure.figure import Figure
from os.path import join as combine_path
from ui.game.figure.movement.horizontal import move_positions as move_positions_horizontal
from ui.game.figure.movement.horizontal import validate_move as validate_move_horizontal
from ui.game.figure.movement.vertical import move_positions as move_positions_vertical
from ui.game.figure.movement.vertical import validate_move as validate_move_vertical
from constants import BLACK, WHITE


class Queen(Figure):
    def __init__(self, side, position):
        super().__init__(side, position)
        self.symbol = "Q"

    def __str__(self):
        if self.side == BLACK:
            return self.symbol + "B"
        else:
            return self.symbol + "W"

    def validate_move(self, board, new_position, target):
        vertical_valid = validate_move_vertical(self.position, new_position)
        horizontal_valid = validate_move_horizontal(self.position, new_position)

        valid = True if vertical_valid or horizontal_valid else False

        if valid:
            return super().validate_move(board, new_position, target)
        else:
            return valid

    def move_positions(self, new_position):
        vertical_valid = validate_move_vertical(self.position, new_position)
        horizontal_valid = validate_move_horizontal(self.position, new_position)

        if vertical_valid:
            return move_positions_vertical(self.position, new_position)

        if horizontal_valid:
            return move_positions_horizontal(self.position, new_position)

    def short_name(self):
        return "Q"

    @classmethod
    def make_instances(cls):
        return [Queen(BLACK, (0, 3)), Queen(WHITE, (7, 3))]

    def icon_path(self):
        return combine_path(Figure.base_icon_path, "queen_black.png") \
            if self.side == BLACK else combine_path(Figure.base_icon_path, "queen_white.png")
