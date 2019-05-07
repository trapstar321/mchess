from tkinter import Tk
from ui.lobby.lobby import LobbyUI



if __name__ == "__main__":
    root = Tk()
    my_gui = LobbyUI(root, 200)

    root.after(my_gui.tick_rate, my_gui.tick)
    root.mainloop()
