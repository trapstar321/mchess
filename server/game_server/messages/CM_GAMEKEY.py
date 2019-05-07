from NIO_python.messages.server.client_message import ClientMessage


class CM_GAMEKEY(ClientMessage):
    OP_CODE = 16

    def __init__(self, data):
        ClientMessage.__init__(self, data)

        self.key = self.get_string()

