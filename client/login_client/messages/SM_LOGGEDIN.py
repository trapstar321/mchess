from NIO_python.client.messages.server_message import ServerMessage


class SM_LOGGEDIN(ServerMessage):
    OP_CODE = 7

    def __init__(self, data):
        ServerMessage.__init__(self, data)

        self.client_id = self.get_object()
        self.username = self.get_string()
