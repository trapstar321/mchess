from NIO_python.messages.client.client_message import ClientMessage


class CM_GAMEKEY(ClientMessage):
    OP_CODE = 16

    def __init__(self, key):
        ClientMessage.__init__(self)

        self.put_string(key)


