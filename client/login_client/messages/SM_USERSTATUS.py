from NIO_python.client.messages.server_message import ServerMessage


class SM_USERSTATUS(ServerMessage):
    OP_CODE = 23

    def __init__(self, data):
        ServerMessage.__init__(self, data)

        self.idx = self.get_object()
        self.status = self.get_int()
