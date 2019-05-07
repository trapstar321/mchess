from NIO_python.messages.server.client_message import ClientMessage


class CM_USERSTATUS(ClientMessage):
    OP_CODE = 23

    def __init__(self, data):
        ClientMessage.__init__(self, data)

        self.status = self.get_int()

