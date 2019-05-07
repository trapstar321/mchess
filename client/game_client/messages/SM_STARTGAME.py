from NIO_python.messages.client.server_message import ServerMessage


class SM_STARTGAME(ServerMessage):
    OP_CODE = 17

    def __init__(self, data):
        ServerMessage.__init__(self, data)

        self.is_white = self.get_bool()

