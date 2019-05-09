from NIO_python.messages.client.server_message import ServerMessage


class SM_ROUNDINFO(ServerMessage):
    OP_CODE = 24

    def __init__(self, data):
        ServerMessage.__init__(self, data)

        self.round = self.get_int()
        self.description = self.get_string()

