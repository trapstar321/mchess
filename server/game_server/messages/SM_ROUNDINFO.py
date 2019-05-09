from NIO_python.messages.server.server_message import ServerMessage


class SM_ROUNDINFO(ServerMessage):
    OP_CODE = 24

    def __init__(self, round, description):
        ServerMessage.__init__(self)

        self.put_int(round)
        self.put_string(description)

