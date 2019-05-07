from NIO_python.messages.server.server_message import ServerMessage


class SM_MOVEOK(ServerMessage):
    OP_CODE = 19

    def __init__(self, source, target):
        ServerMessage.__init__(self)

        self.put_object(source)
        self.put_object(target)

