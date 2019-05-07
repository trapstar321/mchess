from NIO_python.messages.client.client_message import ClientMessage


class CM_MOVE(ClientMessage):
    OP_CODE = 18

    def __init__(self, key, target, source):
        ClientMessage.__init__(self)

        self.put_string(key)
        self.put_object(target)
        self.put_object(source)



