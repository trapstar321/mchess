from NIO_python.messages.server.client_message import ClientMessage


class CM_ACCEPTGAMEREQUEST(ClientMessage):
    OP_CODE = 11

    def __init__(self, data):
        ClientMessage.__init__(self, data)

        self.request_id = self.get_object()

