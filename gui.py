from tkinter import Tk, Button
from constants import X, Y, UI_BLACK, UI_WHITE
from figure.blank import Blank

class MChessGUI:
    def __init__(self, master, board):
        self.master = master
        master.title("mchess")

        # replace = Button(self.master, text="Replace")
        # replace.grid(row=1, column=1)
        # replace.bind("<Button-1>", self.replace_test)

        for x in range(0, 8):
            start_background = UI_WHITE if x % 2 == 0 else UI_BLACK
            for y in range(0, 8):
                if y == 0:
                    self.gen_button(board.board[x][y], start_background)
                else:
                    if y % 2 == 0:
                        self.gen_button(board.board[x][y], start_background)
                    else:
                        self.gen_button(board.board[x][y], UI_WHITE if start_background == UI_BLACK else UI_BLACK)


        for col in range(0, 8):
            master.grid_columnconfigure(col, minsize=60, weight=1)

        for row in range(0, 8):
            master.grid_rowconfigure(row, minsize=60, weight=1)

    def gen_button(self, figure, background):
        img = figure.load_icon()
        figure.image = img

        button = Button(self.master, image=img, bg=background)
        button.position = figure.position
        button.figure = figure
        button.configure(cursor="hand1")
        button.grid(row=figure.position[X], column=figure.position[Y])

        if not isinstance(figure, Blank):
            button.bind("<ButtonPress-1>", self.on_start)
            button.bind("<B1-Motion>", self.on_drag)
        button.bind("<ButtonRelease-1>", self.on_drop)

        return button

    def replace_test(self, event):
        self.replace(self.bishop_white_button, self.bishop_black_button)

    def replace(self, target, source):
        target.grid(row=source.figure.position[X], column=source.figure.position[Y])
        source.grid(row=target.figure.position[X], column=target.figure.position[Y])

        source_pos = (source.figure.position[X], source.figure.position[Y])
        target_pos = (target.figure.position[X], target.figure.position[Y])

        source.figure.position = target_pos
        target.figure.position = source_pos

    def on_start(self, event):
        # you could use this method to create a floating window
        # that represents what is being dragged.
        pass

    def on_drag(self, event):
        # you could use this method to move a floating window that
        # represents what you're dragging
        pass

    def on_drop(self, event):
        # find the widget under the cursor
        x, y = event.widget.winfo_pointerxy()

        source = event.widget
        target = event.widget.winfo_containing(x, y)
        print(source.cget("text"))
        print(target.cget("text"))

