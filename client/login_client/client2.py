from tkinter import Tk
from ui.lobby.lobby import LobbyUI

if __name__=="__main__":
    root = Tk()
    tick_rate=0.2
    my_gui = LobbyUI(root, tick_rate, "user2", "1234", 60000)

    #root.after(my_gui.tick_rate, my_gui.tick)
    root.mainloop()
