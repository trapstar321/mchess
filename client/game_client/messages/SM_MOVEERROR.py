from NIO_python.messages.client.server_message import ServerMessage


class SM_MOVEERROR(ServerMessage):
    OP_CODE = 20

    def __init__(self, data):
        ServerMessage.__init__(self, data)

        self.source = self.get_object()
        self.target = self.get_object()

