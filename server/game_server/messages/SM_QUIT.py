from NIO_python.messages.server.server_message import ServerMessage


class SM_QUIT(ServerMessage):
    OP_CODE = 22

    def __init__(self, key):
        ServerMessage.__init__(self)

        self.put_string(key)

