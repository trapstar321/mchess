from NIO_python.messages.client.client_message import ClientMessage


class CM_ACCEPTGAMEREQUEST(ClientMessage):
    OP_CODE = 11

    def __init__(self, request_id):
        ClientMessage.__init__(self)

        self.put_object(request_id)


