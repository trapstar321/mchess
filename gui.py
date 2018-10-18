from tkinter import Button
from constants import X, Y, UI_BLACK, UI_WHITE, SWAP, EAT, WHITE
from figure.blank import Blank


class MChessGUI:
    def __init__(self, master, board):
        self.master = master
        self.board = board
        master.title("mchess - whites turn")

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

    def move(self, target, source):
        source_position_before_move = (source.figure.position[X], source.figure.position[Y])
        target_position_before_move = (target.figure.position[X], target.figure.position[Y])

        result = self.board.move(source.figure, target.figure)

        if result[0] and result[1] == SWAP:
            target.grid(row=source_position_before_move[X], column=source_position_before_move[Y])
            source.grid(row=target_position_before_move[X], column=target_position_before_move[Y])
        elif result[0] and result[1] == EAT:
            target.grid(row=source_position_before_move[X], column=source_position_before_move[Y])
            source.grid(row=target_position_before_move[X], column=target_position_before_move[Y])
            self.gen_button(result[2], source["bg"])

        print(self.board)

        return result[0]

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

        target_bg = target.cget("bg")
        source_bg = source.cget("bg")

        if self.move(target, source):
            source["bg"] = target_bg
            target["bg"] = source_bg

            self.master.title("mchess - whites turn" if self.board.turn == WHITE else "mchess - blacks turn")


