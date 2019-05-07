from NIO_python.messages.server.server_message import ServerMessage


class SM_CANCELGAMEREQUEST(ServerMessage):
    OP_CODE = 14

    def __init__(self, data):
        ServerMessage.__init__(self)

        self.put_object(data)

