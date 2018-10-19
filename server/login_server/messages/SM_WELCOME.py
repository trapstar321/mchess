from NIO_python.messages.server.server_message import ServerMessage


class SM_WELCOME(ServerMessage):
    OP_CODE = 6

    def __init__(self, data):
        ServerMessage.__init__(self)

        self.put_string(data)

