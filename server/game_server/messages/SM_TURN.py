from NIO_python.messages.server.server_message import ServerMessage


class SM_TURN(ServerMessage):
    OP_CODE = 21

    def __init__(self, turn):
        ServerMessage.__init__(self)

        self.put_bool(turn)

