from NIO_python.messages.client.client_message import ClientMessage


class CM_USERSTATUS(ClientMessage):
    OP_CODE = 23

    def __init__(self, status):
        ClientMessage.__init__(self)

        self.put_int(status)


