from tkinter import Listbox, Text, Button, END, messagebox, NORMAL, DISABLED
from client.login_client.messages.CM_LOGIN import CM_LOGIN
from NIO_python.client.NIOClient import Client
from NIO_python.client.messages.SM_CONNECTED import SM_CONNECTED
from NIO_python.client.messages.SM_DISCONNECTED import SM_DISCONNECTED
from client.login_client.messages.SM_CLIENTLIST import SM_CLIENTLIST
from client.login_client.messages.SM_WELCOME import SM_WELCOME
from client.login_client.messages.SM_LOGINFAILED import SM_LOGINFAILED
from client.login_client.messages.SM_LOGGEDIN import SM_LOGGEDIN
import socket
import queue

from NIO_python.common.log_optional import Logger
from ui.models.user import User

class LobbyUI:
    def __init__(self, master, tick_rate, username_, password_, udp_port):
        self.tick_rate = tick_rate
        self.logger = Logger(1)
        self.master = master
        self.client = None
        self.udp_port = udp_port

        listbox = Listbox(master, width=30, font = ('Arial',15))
        listbox.grid(row=0, columnspan=2)
        listbox.bind('<<ListboxSelect>>', self.onselect)

        username = Text(master, height=2, width=10)
        username.delete(1.0, END)
        username.insert(END, username_)
        username.grid(row=1, column=0, columnspan=2, sticky="WE")
        self.username = username

        password = Text(master, height=2, width=10)
        password.delete(1.0, END)
        password.insert(END, password_)
        password.grid(row=2, column=0, columnspan=2, sticky="WE")
        self.password=password

        login = Button(master, text="Login", command=self.login)
        login.grid(row=3, column=0, columnspan=2)
        self.login_button=login

        disconnect = Button(master, text="Disconnect", command=self.disconnect)
        self.disconnect_button = disconnect

        send_request = Button(master, text="Send request", command=self.send_request)
        self.send_request_button = send_request
        self.send_request_button.configure(state=DISABLED)

        self.listbox = listbox

        self.clients = {}

    def login(self):
        try:
            c = Client(("localhost", 10000), self.udp_port, False, None, None)
            c.start()
            self.client = c

            self.logger.log('Login')
            msg = CM_LOGIN(self.username.get("1.0", "end-1c"), self.password.get("1.0", "end-1c"))
            self.client.handler.write_queue.put([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b'1', ('127.0.0.1', self.client.udp_port))

            self.login_button.grid_forget()
            self.disconnect_button.grid(row=3, column=0)
            self.send_request_button.grid(row=3, column=1)

            self.master.after(self.tick_rate, self.tick)
        except ConnectionRefusedError:
            messagebox.showerror("Connection failed", "Failed to connect to server")

    def disconnect(self):
        self.client.shutdown()
        self.client = None
        self.disconnect_button.grid_forget()
        self.send_request_button.grid_forget()
        self.login_button.grid(row=3, column=0, columnspan=2)
        self.clients = {}
        self.listbox.delete(0, END)
        self.send_request_button.configure(state=DISABLED)

    def send_request(self):
        pass

    def onselect(self, event):
        print('onselect')
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))
        self.send_request_button.configure(state=NORMAL)

    def add(self, user):
        user.set_index(self.listbox.size())
        self.clients[user.client_id]=user
        self.listbox.insert(END, user)

    def add_multiple(self, users):
        for client_id in users.keys():
            self.add(User(client_id, users[client_id]['username']))

    def delete(self, client_id):
        user = self.clients[client_id]
        self.listbox.delete(user.index)
        del self.clients[client_id]

        for client_id in self.clients.keys():
            self.clients[client_id].index = self.listbox.get(0, "end").index(self.clients[client_id].username)

    def tick(self):
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
                        self.client.handler.write_queue.put(processed_messages)

                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.sendto(b'1', ('127.0.0.1', self.client.udp_port))
                except Exception as ex:
                    self.logger.log("forward_messages: exception: {0}".format(ex))

        self.master.after(self.tick_rate, self.tick)

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
                    self.delete(msg.idx)
                elif message["opcode"]==SM_CLIENTLIST.OP_CODE:
                    msg = SM_CLIENTLIST(message["data"])
                    self.add_multiple(msg.clients)
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
                    self.add(User(msg.client_id, msg.username))

            return smessages
        except Exception as ex:
            self.logger.log('process_messages exception: {0}'.format(ex))
