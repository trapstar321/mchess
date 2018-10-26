from tkinter import Listbox, Text, Button, END, messagebox, NORMAL, DISABLED, LabelFrame
from client.login_client.messages.CM_LOGIN import CM_LOGIN
from NIO_python.client.NIOClient import Client
from NIO_python.client.messages.SM_CONNECTED import SM_CONNECTED
from NIO_python.client.messages.SM_DISCONNECTED import SM_DISCONNECTED
from client.login_client.messages.SM_CLIENTLIST import SM_CLIENTLIST
from client.login_client.messages.SM_WELCOME import SM_WELCOME
from client.login_client.messages.SM_LOGINFAILED import SM_LOGINFAILED
from client.login_client.messages.SM_LOGGEDIN import SM_LOGGEDIN
from client.login_client.messages.CM_GAMEREQUEST import CM_GAMEREQUEST
from client.login_client.messages.SM_GAMEREQUEST import SM_GAMEREQUEST
import socket
import queue
from client.login_client.listbox_controller import ListBoxController

from NIO_python.common.log_optional import Logger
from ui.models.user import User
from ui.models.gamerequest import GameRequest

class LobbyUI:
    def __init__(self, master, tick_rate, username_, password_, udp_port):
        self.tick_rate = tick_rate
        self.logger = Logger(1)
        self.master = master
        self.client = None
        self.udp_port = udp_port
        self.clients = {}
        self.requests = {}

        group_usersonline = LabelFrame(master, text="Users online", padx=5, pady=5)
        group_usersonline.grid(row=0, column=0)
        group_pendingrequests = LabelFrame(master, text="Pending requests", padx=5, pady=5)
        group_pendingrequests.grid(row=0, column=1)

        usersonline_listbox = Listbox(group_usersonline, width=30, font = ('Arial',15))
        usersonline_listbox.pack()
        usersonline_listbox.bind('<<ListboxSelect>>', self.onselect_user)
        self.usersonline_controller = ListBoxController(self.clients, usersonline_listbox)

        pendingrequests_listbox = Listbox(group_pendingrequests, width=30, font=('Arial', 15))
        pendingrequests_listbox.pack()
        pendingrequests_listbox.bind('<<ListboxSelect>>', self.onselect_request)
        self.pendingrequests_controller = ListBoxController(self.requests, pendingrequests_listbox)

        group_requestactions = LabelFrame(master, text="Request actions", padx=5, pady=5)
        group_requestactions.grid(row=1, column=1)
        self.group_requestactions = group_requestactions

        accept = Button(group_requestactions, text="Accept", command=self.accept)
        accept.grid(row=0, column=0)
        accept.configure(state=DISABLED)
        self.accept_button = accept

        reject = Button(group_requestactions, text="Reject", command=self.reject)
        reject.grid(row=0, column=1)
        reject.configure(state=DISABLED)
        self.reject_button = reject

        cancel = Button(group_requestactions, text="Cancel", command=self.cancel)
        cancel.grid(row=0, column=2)
        cancel.configure(state=DISABLED)
        self.cancel_button = cancel

        username = Text(master, height=2, width=10)
        username.delete(1.0, END)
        username.insert(END, username_)
        username.grid(row=2, column=0, columnspan=2, sticky="WE")
        self.username = username

        password = Text(master, height=2, width=10)
        password.delete(1.0, END)
        password.insert(END, password_)
        password.grid(row=3, column=0, columnspan=2, sticky="WE")
        self.password=password

        login = Button(master, text="Login", command=self.login)
        login.grid(row=4, column=0, columnspan=2)
        self.login_button=login

        disconnect = Button(master, text="Disconnect", command=self.disconnect)
        self.disconnect_button = disconnect

        send_request = Button(master, text="Send request", command=self.send_request)
        self.send_request_button = send_request
        self.send_request_button.configure(state=DISABLED)

        self.usersonline_listbox = usersonline_listbox
        self.pendingrequests_listbox = pendingrequests_listbox

    def login(self):
        try:
            c = Client(("localhost", 10000), self.udp_port, False, None, None)
            c.start()
            self.client = c

            self.logger.log('Login')
            msg = CM_LOGIN(self.username.get("1.0", "end-1c"), self.password.get("1.0", "end-1c"))
            self.send_messages([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])

            self.login_button.grid_forget()
            self.disconnect_button.grid(row=4, column=0)
            self.send_request_button.grid(row=4, column=1)

            self.master.after(self.tick_rate, self.tick)
        except ConnectionRefusedError:
            messagebox.showerror("Connection failed", "Failed to connect to server")

    def disconnect(self):
        self.client.shutdown()
        self.client = None
        self.disconnect_button.grid_forget()
        self.send_request_button.grid_forget()
        self.login_button.grid(row=4, column=0, columnspan=2)

        self.usersonline_controller.clear()
        self.pendingrequests_controller.clear()
        self.send_request_button.configure(state=DISABLED)
        self.cancel_button.configure(state=DISABLED)
        self.accept_button.configure(state=DISABLED)
        self.reject_button.configure(state=DISABLED)

    def accept(self):
        pass

    def reject(self):
        pass

    def cancel(self):
        pass

    def send_request(self):
        user = self.usersonline_controller.get_selected()
        self.logger.log("Send game request to user {0}".format(user.client_id))

        msg = CM_GAMEREQUEST(user.client_id)
        self.send_messages([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])

    def onselect_user(self, event):
        user = self.usersonline_controller.get_selected()
        if user is not None:
            self.send_request_button.configure(state=NORMAL)
        else:
            self.send_request_button.configure(state=DISABLED)

    def onselect_request(self, event):
        request = self.pendingrequests_controller.get_selected()

        if request is not None:
            if request.flag == 0:
                self.cancel_button.configure(state=DISABLED)
                self.accept_button.configure(state=NORMAL)
                self.reject_button.configure(state=NORMAL)
            elif request.flag == 1:
                self.cancel_button.configure(state=NORMAL)
                self.accept_button.configure(state=DISABLED)
                self.reject_button.configure(state=DISABLED)
            else:
                self.cancel_button.configure(state=DISABLED)
                self.accept_button.configure(state=DISABLED)
                self.reject_button.configure(state=DISABLED)
        else:
            self.cancel_button.configure(state=DISABLED)
            self.accept_button.configure(state=DISABLED)
            self.reject_button.configure(state=DISABLED)


    def add_user(self, user):
        self.usersonline_controller.add(user)

    def add_multiple_users(self, users):
        for client_id in users.keys():
            self.add_user(User(client_id, users[client_id]['username']))

    def delete_user(self, client_id):
        self.usersonline_controller.delete(client_id)

    def add_request(self, request):
        self.pendingrequests_controller.add(request)

    def delete_request(self, request_id):
        self.pendingrequests_controller.delete(request_id)

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
                        self.send_messages(processed_messages)
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
                    self.delete_user(msg.idx)
                elif message["opcode"]==SM_CLIENTLIST.OP_CODE:
                    msg = SM_CLIENTLIST(message["data"])
                    self.add_multiple_users(msg.clients)
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
                    self.add_user(User(msg.client_id, msg.username))
                elif message["opcode"] == SM_GAMEREQUEST.OP_CODE:
                    msg = SM_GAMEREQUEST(message["data"])

                    if msg.flag == 1:
                        print('Received id {0} for request sent to {1}'.format(msg.request_id, msg.client))
                        self.add_request(GameRequest(msg.request_id, msg.client, msg.username, msg.flag))
                    elif msg.flag == 0:
                        print('New game request {0} from user {1}'.format(msg.request_id, msg.client))
                        self.add_request(GameRequest(msg.request_id, msg.client, msg.username, msg.flag))

            return smessages
        except Exception as ex:
            self.logger.log('process_messages exception: {0}'.format(ex))

    def send_messages(self, messages):
        self.client.handler.write_queue.put(messages)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b'1', ('127.0.0.1', self.client.udp_port))
