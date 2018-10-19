from NIO_python.messages.server.server_message import ServerMessage


class SM_LOGINFAILED(ServerMessage):
    OP_CODE = 5

    def __init__(self, data):
        ServerMessage.__init__(self)

        self.put_string(data)

