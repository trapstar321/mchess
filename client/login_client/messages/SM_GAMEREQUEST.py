from NIO_python.client.messages.server_message import ServerMessage


class SM_GAMEREQUEST(ServerMessage):
    OP_CODE = 9

    def __init__(self, data):
        ServerMessage.__init__(self, data)

        self.request_id = self.get_object()
        self.client = self.get_object()
        self.username = self.get_string()
        self.flag = self.get_int()
