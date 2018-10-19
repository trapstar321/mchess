from client.login_client.create_login_client import create_client
from tkinter import Tk
from ui.lobby import LobbyUI

if __name__=="__main__":
    c = create_client(60001)
    c.start()

    root = Tk()
    my_gui = LobbyUI(root, c, "user1", "1234")

    root.after(1000, my_gui.tick)
    root.mainloop()
