from NIO_python.client.messages.server_message import ServerMessage


class SM_LOGINFAILED(ServerMessage):
    OP_CODE = 5

    def __init__(self, data):
        ServerMessage.__init__(self, data)

        self.msg = self.get_string()
