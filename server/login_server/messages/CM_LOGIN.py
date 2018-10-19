from NIO_python.messages.server.client_message import ClientMessage


class CM_LOGIN(ClientMessage):
    OP_CODE = 4

    def __init__(self, data):
        ClientMessage.__init__(self, data)

        self.username = self.get_string()
        self.password = self.get_string()

