from tkinter import Tk
from ui.lobby import LobbyUI



if __name__ == "__main__":
    root = Tk()
    my_gui = LobbyUI(root)

    root.after(1000, my_gui.tick)
    root.mainloop()
