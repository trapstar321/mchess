from NIO_python.messages.server.server_message import ServerMessage


class SM_LOGGEDIN(ServerMessage):
    OP_CODE = 7

    def __init__(self, client_id, username):
        ServerMessage.__init__(self)

        self.put_object(client_id)
        self.put_string(username)

