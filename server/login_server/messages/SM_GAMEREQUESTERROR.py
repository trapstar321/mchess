from NIO_python.messages.server.server_message import ServerMessage


class SM_GAMEREQUESTERROR(ServerMessage):
    OP_CODE = 10

    def __init__(self, data):
        ServerMessage.__init__(self)

        self.put_string(data)

