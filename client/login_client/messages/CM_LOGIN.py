from NIO_python.messages.client.client_message import ClientMessage


class CM_LOGIN(ClientMessage):
    OP_CODE = 4

    def __init__(self, username, password):
        ClientMessage.__init__(self)

        self.put_string(username)
        self.put_string(password)


