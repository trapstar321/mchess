from NIO_python.messages.client.server_message import ServerMessage


class SM_TURN(ServerMessage):
    OP_CODE = 21

    def __init__(self, data):
        ServerMessage.__init__(self, data)

        self.turn = self.get_bool()
