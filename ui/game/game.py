from tkinter import Button, messagebox, Toplevel, DISABLED, NORMAL
from constants import X, Y, UI_BLACK, UI_WHITE, SWAP, EAT, WHITE, BLACK
from ui.game.figure.blank import Blank
from client.game_client.messages.CM_MOVE import CM_MOVE
from client.game_client.messages.CM_GAMEKEY import CM_GAMEKEY
from client.game_client.messages.SM_MOVEOK import SM_MOVEOK
from client.game_client.messages.SM_MOVEERROR import SM_MOVEERROR
from client.game_client.messages.SM_STARTGAME import SM_STARTGAME
from client.game_client.messages.SM_TURN import SM_TURN

import queue
import socket

from NIO_python.client.NIOClient import Client
from NIO_python.common.log_optional import Logger
from ui.game.board import Board

import time
import threading

class GameUI:
    def __init__(self, master, sm_gamekey, udp_port):
        self.master = master
        self.board = Board()
        self.sm_gamekey = sm_gamekey
        self.udp_port = udp_port
        self.logger = Logger(1)
        self.client = None
        self.tick_rate = 0.2
        self.buttons = []

        self.start_game()

    def create(self):
        self.master = Toplevel(self.master)
        self.master.title("mchess - {0} turn".format("your" if self.is_white else "whites"))

        for x in range(0, 8):
            start_background = UI_WHITE if x % 2 == 0 else UI_BLACK
            for y in range(0, 8):
                if y == 0:
                    self.gen_button(self.board.board[x][y], start_background)
                else:
                    if y % 2 == 0:
                        self.gen_button(self.board.board[x][y], start_background)
                    else:
                        self.gen_button(self.board.board[x][y], UI_WHITE if start_background == UI_BLACK else UI_BLACK)

        for col in range(0, 8):
            self.master.grid_columnconfigure(col, minsize=60, weight=1)

        for row in range(0, 8):
            self.master.grid_rowconfigure(row, minsize=60, weight=1)

        self.setup(NORMAL if self.is_white else DISABLED)

    def gen_button(self, figure, background):
        img = figure.load_icon()
        figure.image = img

        button = Button(self.master, image=img, bg=background)
        button.position = figure.position
        button.figure = figure
        button.configure(cursor="hand1")
        button.grid(row=figure.position[X], column=figure.position[Y])

        self.buttons.append(button)

        if not isinstance(figure, Blank):
            button.bind("<ButtonPress-1>", self.on_start)
            button.bind("<B1-Motion>", self.on_drag)
        button.bind("<ButtonRelease-1>", self.on_drop)

        return button

    def get_button(self, pos):
        for button in self.buttons:
            if button.position[X]==pos[X] and button.position[Y]==pos[Y]:
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

        #print(self.board)

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

        msg = CM_MOVE(self.sm_gamekey.key, target.position, source.position)
        self.send_messages([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])

    def setup(self, state):
        for button in self.buttons:
            side = WHITE if self.is_white else BLACK
            if button.figure.side==side:
                button.configure(state=state)
                if state==NORMAL:
                    button.configure(state=NORMAL)
                    button.bind("<ButtonPress-1>", self.on_start)
                    button.bind("<B1-Motion>", self.on_drag)
                    button.bind("<ButtonRelease-1>", self.on_drop)
                elif state==DISABLED:
                    button.configure(state=DISABLED)
                    button.unbind("<ButtonPress-1>")
                    button.unbind("<B1-Motion>")
                    button.unbind("<ButtonRelease-1>")
            else:
                button.configure(state=DISABLED)
                button.unbind("<ButtonPress-1>")
                button.unbind("<B1-Motion>")
                button.unbind("<ButtonRelease-1>")


    def start_game(self):
        try:
            c = Client((self.sm_gamekey.ip, self.sm_gamekey.port), self.udp_port, False, None, None)
            c.start()
            self.client = c

            msg = CM_GAMEKEY(self.sm_gamekey.key)
            self.send_messages([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])

            #self.master.after(self.tick_rate, self.tick)
            t = threading.Thread(target=self.tick)
            t.start()
        except ConnectionRefusedError:
            messagebox.showerror("Connection failed", "Failed to connect to server")

    def disconnect(self):
        self.client.shutdown()
        self.client = None

    def tick(self):
        while True:
            if self.client is not None:
                status = self.client.status()
                if status == 3 or status == 4:
                    messagebox.showerror("Connection error", "Disconnected from server")
                    self.disconnect()
            else:
                return

            messages = None
            try:
                if self.client is not None:
                    messages = self.client.handler.read_queue.get(True, 0.1)
            except queue.Empty:
                pass
            else:
                if messages is not None:
                    try:
                        processed_messages = self.process_messages(messages)

                        if processed_messages is not None and len(processed_messages)>0:
                            self.send_messages(processed_messages)
                    except Exception as ex:
                        self.logger.log("forward_messages: exception: {0}".format(ex))

        time.sleep(self.tick_rate)
        #self.master.after(self.tick_rate, self.tick)

    def process_messages(self, messages):
        try:
            smessages = []
            for message in messages:
                self.logger.log("Processor received message: {0}".format(message))

                if message["opcode"] == SM_STARTGAME.OP_CODE:
                    msg = SM_STARTGAME(message["data"])
                    self.logger.log("Start game. Am {0}".format("white" if msg.is_white else "black"))
                    self.is_white = msg.is_white
                    self.create()
                elif message["opcode"] == SM_MOVEOK.OP_CODE:
                    msg = SM_MOVEOK(message["data"])

                    source = self.get_button(msg.source)
                    target = self.get_button(msg.target)

                    target_bg = target.cget("bg")
                    source_bg = source.cget("bg")

                    if self.move(target, source):
                        source["bg"] = target_bg
                        target["bg"] = source_bg
                elif message["opcode"] == SM_MOVEERROR.OP_CODE:
                    pass
                elif message["opcode"] == SM_TURN.OP_CODE:
                    msg = SM_TURN(message["data"])
                    self.logger.log("White? {0}".format(self.is_white))
                    self.logger.log("Turn? {0}".format(msg.turn))
                    if msg.turn:
                        self.setup(NORMAL)
                        self.master.title("Your turn")
                    else:
                        self.setup(DISABLED)
                        self.master.title("mchess - blacks turn" if self.is_white else "mchess - whites turn")

            return smessages
        except Exception as ex:
            self.logger.log('process_messages exception: {0}'.format(ex))

    def send_messages(self, messages):
        self.client.handler.write_queue.put(messages)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b'1', ('127.0.0.1', self.client.udp_port))

