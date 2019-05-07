from NIO_python.client.messages.server_message import ServerMessage


class SM_CANCELGAMEREQUEST(ServerMessage):
    OP_CODE = 14

    def __init__(self, data):
        ServerMessage.__init__(self, data)

        self.request_id = self.get_object()
