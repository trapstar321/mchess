from tkinter import Tk
from ui.lobby import LobbyUI

if __name__=="__main__":
    root = Tk()
    tick_rate=200
    my_gui = LobbyUI(root, tick_rate, "user1", "1234", 60001)

    #root.after(my_gui.tick_rate, my_gui.tick)
    root.mainloop()
