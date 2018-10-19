from NIO_python.client.messages.server_message import ServerMessage


class SM_CLIENTLIST(ServerMessage):
    OP_CODE = 3

    def __init__(self, data):
        ServerMessage.__init__(self, data)

        self.clients = self.get_object()
