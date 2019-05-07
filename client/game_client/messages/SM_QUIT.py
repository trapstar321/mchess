from NIO_python.messages.client.server_message import ServerMessage


class SM_QUIT(ServerMessage):
    OP_CODE = 22

    def __init__(self, data):
        ServerMessage.__init__(self, data)

        self.key = self.get_string()

