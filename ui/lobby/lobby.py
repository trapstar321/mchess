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
from client.login_client.messages.CM_USERSTATUS import CM_USERSTATUS
from client.login_client.messages.SM_GAMEREQUEST import SM_GAMEREQUEST
from client.login_client.messages.SM_GAMEREQUESTERROR import SM_GAMEREQUESTERROR
from client.login_client.messages.SM_CANCELGAMEREQUEST import SM_CANCELGAMEREQUEST
from client.login_client.messages.SM_REJECTGAMEREQUEST import SM_REJECTGAMEREQUEST
from client.login_client.messages.CM_ACCEPTGAMEREQUEST import CM_ACCEPTGAMEREQUEST
from client.login_client.messages.CM_REJECTGAMEREQUEST import CM_REJECTGAMEREQUEST
from client.login_client.messages.CM_CANCELGAMEREQUEST import CM_CANCELGAMEREQUEST
from client.login_client.messages.SM_GAMEKEY import SM_GAMEKEY
from client.login_client.messages.SM_USERSTATUS import SM_USERSTATUS

import socket
import queue
from ui.listbox_controller import ListBoxController

from NIO_python.common.log_optional import Logger
from models.user import User
from models.gamerequest import GameRequest

from ui.game.game import GameUI

import threading
import time
from random import randint
import traceback

class StatusCallback:
    def __init__(self, logger, send_messages):
        self.logger = logger
        self.send_messages = send_messages
        self.status = 0

    def in_game(self):
        self.logger.log("Status: in game")
        self.status = 1
        msg = CM_USERSTATUS(1)
        self.send_messages([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])

    def available(self):
        self.logger.log("Status: available")
        self.status = 0
        msg = CM_USERSTATUS(0)
        self.send_messages([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])

class LobbyUI:
    def __init__(self, master, tick_rate, username_, password_, udp_port):
        self.tick_rate = tick_rate
        self.logger = Logger(1)
        self.master = master
        self.client = None
        self.udp_port = udp_port
        self.clients = {}
        self.requests = {}
        self.exit_tick = False
        self.scb = StatusCallback(self.logger, self.send_messages)

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
            self.exit_tick = False
            c = Client(("127.0.0.1", 10000), self.udp_port, False, None, None)
            c.start()
            self.client = c

            self.logger.log('Login')
            msg = CM_LOGIN(self.username.get("1.0", "end-1c"), self.password.get("1.0", "end-1c"))
            self.send_messages([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])

            self.login_button.grid_forget()
            self.disconnect_button.grid(row=4, column=0)
            self.send_request_button.grid(row=4, column=1)

            #self.master.after(self.tick_rate, self.tick)
            t = threading.Thread(target=self.tick)
            t.daemon=True
            t.start()
        except ConnectionRefusedError:
            messagebox.showerror("Connection failed", "Failed to connect to server")

    def disconnect(self):
        self.exit_tick = True
        self.client.shutdown()
        self.client = None
        self.disconnect_button.grid_forget()
        self.send_request_button.grid_forget()
        self.login_button.grid(row=4, column=0, columnspan=2)

        self.clients = {}
        self.requests = {}
        self.usersonline_controller.clear(self.clients)
        self.pendingrequests_controller.clear(self.requests)
        self.send_request_button.configure(state=DISABLED)
        self.cancel_button.configure(state=DISABLED)
        self.accept_button.configure(state=DISABLED)
        self.reject_button.configure(state=DISABLED)

    def accept(self):
        request = self.pendingrequests_controller.get_selected()
        msg = CM_ACCEPTGAMEREQUEST(request.request_id)
        self.send_messages([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])

    def reject(self):
        request = self.pendingrequests_controller.get_selected()
        msg = CM_REJECTGAMEREQUEST(request.request_id)
        self.send_messages([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])

    def cancel(self):
        request = self.pendingrequests_controller.get_selected()
        msg = CM_CANCELGAMEREQUEST(request.request_id)
        self.send_messages([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])
        self.cancel_button.configure(state=DISABLED)

    def send_request(self):
        user = self.usersonline_controller.get_selected()
        self.logger.log("Send game request to user {0}".format(user.client_id))

        msg = CM_GAMEREQUEST(user.client_id)
        self.send_messages([{"opcode": type(msg).OP_CODE, "data": msg.get_data()}])

    def onselect_user(self, event):
        user = self.usersonline_controller.get_selected()
        if user is not None and user.status == 0 and self.scb.status == 0:
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
            self.add_user(User(client_id, users[client_id]['username'], users[client_id]['status']))

    def delete_user(self, client_id):
        self.usersonline_controller.delete(client_id)

        if self.usersonline_controller.get_selected() is None:
            self.send_request_button.configure(state=DISABLED)

    def add_request(self, request):
        self.pendingrequests_controller.add(request)

    def delete_request(self, request_id):
        self.pendingrequests_controller.delete(request_id)

        if self.pendingrequests_controller.get_selected() is None:
            self.cancel_button.configure(state=DISABLED)
            self.accept_button.configure(state=DISABLED)
            self.reject_button.configure(state=DISABLED)

    def remove_requests(self, client_id):
        to_delete = []
        for request_id in self.requests.keys():
            request = self.requests[request_id]
            if request.client_id == client_id:
                to_delete.append(request_id)

        for request_id in to_delete:
            self.delete_request(request_id)

    def canceled_rejected(self):
        selected = self.pendingrequests_controller.get_selected()

        if selected is None:
            self.cancel_button.configure(state=DISABLED)
            self.accept_button.configure(state=DISABLED)
            self.reject_button.configure(state=DISABLED)


    def tick(self):
        while True:
            if self.exit_tick:
                return

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

                if message["opcode"]==SM_CONNECTED.OP_CODE:
                    msg = SM_CONNECTED(message["data"])
                    self.logger.log("Client id={0} connected".format(msg.idx))
                elif message["opcode"]==SM_DISCONNECTED.OP_CODE:
                    msg = SM_DISCONNECTED(message["data"])
                    self.logger.log("Client id={0} disconnected".format(msg.idx))
                    self.delete_user(msg.idx)
                    self.remove_requests(msg.idx)
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
                    self.add_user(User(msg.client_id, msg.username, 0))
                elif message["opcode"] == SM_GAMEREQUEST.OP_CODE:
                    msg = SM_GAMEREQUEST(message["data"])

                    if msg.flag == 1:
                        print('Received id {0} for request sent to {1}'.format(msg.request_id, msg.client))
                        self.add_request(GameRequest(msg.request_id, msg.client, msg.username, msg.flag))
                    elif msg.flag == 0:
                        print('New game request {0} from user {1}'.format(msg.request_id, msg.client))
                        self.add_request(GameRequest(msg.request_id, msg.client, msg.username, msg.flag))
                elif message["opcode"] == SM_GAMEREQUESTERROR.OP_CODE:
                    msg = SM_GAMEREQUESTERROR(message["data"])
                    messagebox.showerror("Request error", msg.msg)
                elif message["opcode"] == SM_CANCELGAMEREQUEST.OP_CODE:
                    msg = SM_CANCELGAMEREQUEST(message["data"])
                    self.pendingrequests_controller.delete(msg.request_id)
                    self.canceled_rejected()
                elif message["opcode"] == SM_REJECTGAMEREQUEST.OP_CODE:
                    msg = SM_REJECTGAMEREQUEST(message["data"])
                    self.pendingrequests_controller.delete(msg.request_id)
                    self.canceled_rejected()
                elif message["opcode"] == SM_GAMEKEY.OP_CODE:
                    msg = SM_GAMEKEY(message["data"])
                    GameUI(self.master, msg, randint(50000, 51000), self.scb)
                    self.logger.log("Game request key={0}, game server ip={1}, port={2}".format(msg.key, msg.ip, msg.port))
                    #self.delete_request(msg.request_id)
                elif message["opcode"] == SM_USERSTATUS.OP_CODE:
                    msg = SM_USERSTATUS(message["data"])
                    self.logger.log("Client {0} status = {1}".format(msg.idx, "in game" if msg.status == 1 else "available"))
                    self.usersonline_controller.get(msg.idx).set_status(msg.status)
                    self.usersonline_listbox.update()
                    self.usersonline_controller.refresh(msg.idx)

            return smessages
        except Exception as ex:
            self.logger.log('process_messages exception: {0}'.format(ex))
            traceback.print_tb(ex.__traceback__)

    def send_messages(self, messages):
        self.client.handler.write_queue.put(messages)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b'1', ('127.0.0.1', self.client.udp_port))
