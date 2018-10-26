from NIO_python.messages.client.client_message import ClientMessage


class CM_GAMEREQUEST(ClientMessage):
    OP_CODE = 8

    def __init__(self, client):
        ClientMessage.__init__(self)

        self.put_object(client)


