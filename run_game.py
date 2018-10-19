from board import Board
from tkinter import Tk
from ui.game import GameUI



if __name__ == "__main__":
    b = Board()

    root = Tk()
    my_gui = GameUI(root, b)
    root.mainloop()
