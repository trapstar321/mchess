from NIO_python.messages.server.server_message import ServerMessage


class SM_STARTGAME(ServerMessage):
    OP_CODE = 17

    def __init__(self, is_white):
        ServerMessage.__init__(self)

        self.put_bool(is_white)

