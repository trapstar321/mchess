from figure.king import King
from figure.queen import Queen
from figure.rook import Rook
from figure.knight import Knight
from figure.bishop import Bishop
from figure.pawn import Pawn
from figure.blank import Blank
from constants import X, Y, WHITE, BLACK, EAT, SWAP
from move import Move


class Board:
    BOARD_LENGTH = 8
    X_MAPPING = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    Y_MAPPING = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
    INVERTED_X_MAPPING = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    INVERTED_Y_MAPPING = {8: 0, 7: 1, 6: 2, 5: 3, 4: 4, 3: 5, 2: 6, 1: 7}

    def __init__(self):
        self.board = []
        self.turn = WHITE

        for x in range(0, Board.BOARD_LENGTH):
            self.board.append(['']*Board.BOARD_LENGTH)

        self.moves = []

        figures = []
        figures.extend(King.make_instances())
        figures.extend(Queen.make_instances())
        figures.extend(Rook.make_instances())
        figures.extend(Knight.make_instances())
        figures.extend(Bishop.make_instances())
        figures.extend(Pawn.make_instances())
        figures.extend(Blank.make_instances())

        for figure in figures:
            self.add_figure(figure)

    def add_figure(self, figure):
        self.board[figure.position[X]][figure.position[Y]] = figure

    @classmethod
    def position_to_cell(cls, x, y):
        return Board.X_MAPPING[x], Board.Y_MAPPING[y]

    @classmethod
    def cell_to_position(cls, x, y):
        return Board.INVERTED_X_MAPPING[x], Board.INVERTED_Y_MAPPING[y]

    def move(self, source, target):
        m = Move(source, target, self.turn)

        type_ = SWAP

        if m.validate(self):
            source_pos = (source.position[X], source.position[Y])
            target_pos = (target.position[X], target.position[Y])

            if not source.side == target.side and not target.is_blank:
                type_ = EAT

                target = Blank(WHITE, source.position)
                self.board[source_pos[X]][source_pos[Y]] = target
                self.board[target_pos[X]][target_pos[Y]] = source

                source.position = target_pos
            else:
                self.board[source_pos[X]][source_pos[Y]] = target
                self.board[target_pos[X]][target_pos[Y]] = source

                source.position = target_pos
                target.position = source_pos

            self.moves.append(m)

            self.turn = BLACK if self.turn == WHITE else WHITE

            return True, type_, target

        return False, type_, target

    def __str__(self):
        result = ""
        end = range(0, Board.BOARD_LENGTH)
        for x in end:
            result += "\n"
            for y in end:
                result += "[{}]".format(self.board[x][y])
        return result

