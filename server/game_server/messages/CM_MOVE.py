from NIO_python.messages.server.client_message import ClientMessage


class CM_MOVE(ClientMessage):
    OP_CODE = 18

    def __init__(self, data):
        ClientMessage.__init__(self, data)

        self.key = self.get_string()
        self.target = self.get_object()
        self.source = self.get_object()


