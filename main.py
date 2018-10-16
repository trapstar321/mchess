from board import Board
from move import Move
from tkinter import Tk
from gui import MChessGUI

if __name__ == "__main__":
    b = Board()

    # print(b)
    #
    # k = b.board[7][1]
    # move = Move(k, (5, 0))
    #
    # print(move.validate(b))

    root = Tk()
    my_gui = MChessGUI(root, b)
    root.mainloop()
