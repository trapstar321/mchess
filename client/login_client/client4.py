from tkinter import Tk
from ui.lobby.lobby import LobbyUI

if __name__=="__main__":
    root = Tk()
    tick_rate=0.2
    my_gui = LobbyUI(root, tick_rate, "user4", "1234", 60006)

    #root.after(my_gui.tick_rate, my_gui.tick)
    root.mainloop()
