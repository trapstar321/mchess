from tkinter import Listbox, Text, Button, END
from client.login_client.messages.CM_LOGIN import CM_LOGIN
from NIO_python.client.messages.SM_CONNECTED import SM_CONNECTED
from NIO_python.client.messages.SM_DISCONNECTED import SM_DISCONNECTED
from client.login_client.messages.SM_CLIENTLIST import SM_CLIENTLIST
from client.login_client.messages.SM_WELCOME import SM_WELCOME
from client.login_client.messages.SM_LOGINFAILED import SM_LOGINFAILED
from client.login_client.messages.SM_LOGGEDIN import SM_LOGGEDIN
import socket
import queue

from NIO_python.common.log_optional import Logger

class LobbyUI:
    def __init__(self, master, client, username_, password_):
        self.logger = Logger(1)
        self.master = master
        self.client = client

        listbox = Listbox(master, width=30)
        listbox.pack()

        username = Text(master, height=2, width=10)
        username.delete(1.0, END)
        username.insert(END, username_)
        username.pack()
        self.username = username

        password = Text(master, height=2, width=10)
        password.delete(1.0, END)
        password.insert(END, password_)
        password.pack()
        self.password=password

        login = Button(master, text="Login", command=self.login)
        login.pack()

        self.listbox = listbox

    def login(self):
        self.logger.log('Login')
        msg = CM_LOGIN(self.username.get("1.0", "end-1c"), self.password.get("1.0", "end-1c"))
        self.client.handler.write_queue.put([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b'1', ('127.0.0.1', self.client.udp_port))

    def add(self, val):
        self.listbox.insert(END, val)

    def tick(self):
        try:
            messages = self.client.handler.read_queue.get(True, 0.1)
        except queue.Empty:
            self.master.after(1000, self.tick)
            return
        else:
            try:
                processed_messages = self.process_messages(messages)

                if len(processed_messages)>0:
                    self.client.handler.write_queue.put(processed_messages)

                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.sendto(b'1', ('127.0.0.1', self.client.udp_port))
            except Exception as ex:
                self.logger.log("forward_messages: exception: {0}".format(ex))

            self.master.after(1000, self.tick)


    def process_messages(self, messages):
        try:
            smessages = []
            for message in messages:
                self.logger.log("Processor received message: {0}".format(message))

                if message["opcode"]==SM_CONNECTED.OP_CODE:
                    msg = SM_CONNECTED(message["data"])
                    self.logger.log("Client id={0} connected".format(msg.idx))
                elif message["opcode"]==SM_DISCONNECTED.OP_CODE:
                    msg = SM_DISCONNECTED(message["data"])
                    self.logger.log("Client id={0} disconnected".format(msg.idx))
                elif message["opcode"]==SM_CLIENTLIST.OP_CODE:
                    msg = SM_CLIENTLIST(message["data"])
                    self.logger.log("Clients on login server={0}".format(msg.clients))
                elif message["opcode"]==SM_LOGINFAILED.OP_CODE:
                    msg = SM_LOGINFAILED(message["data"])
                    self.logger.log("Failed to login => {0}".format(msg.msg))
                elif message["opcode"] == SM_WELCOME.OP_CODE:
                    msg = SM_WELCOME(message["data"])
                    self.logger.log("Successfull login => {0}".format(msg.msg))
                elif message["opcode"] == SM_LOGGEDIN.OP_CODE:
                    msg = SM_LOGGEDIN(message["data"])
                    self.logger.log("User {0} logged in".format(msg.username))

            return smessages
        except Exception as ex:
            self.logger.log('process_messages exception: {0}'.format(ex))
