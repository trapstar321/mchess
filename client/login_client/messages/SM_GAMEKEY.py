from NIO_python.client.messages.server_message import ServerMessage


class SM_GAMEKEY(ServerMessage):
    OP_CODE = 16

    def __init__(self, data):
        ServerMessage.__init__(self, data)

        self.ip = self.get_string()
        self.port = self.get_int()
        self.key = self.get_string()