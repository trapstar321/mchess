from NIO_python.messages.server.client_message import ClientMessage


class CM_GAMEREQUEST(ClientMessage):
    OP_CODE = 8

    def __init__(self, data):
        ClientMessage.__init__(self, data)

        self.client = self.get_object()

