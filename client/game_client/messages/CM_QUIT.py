from NIO_python.messages.client.client_message import ClientMessage


class CM_QUIT(ClientMessage):
    OP_CODE = 22

    def __init__(self, key):
        ClientMessage.__init__(self)

        self.put_string(key)



