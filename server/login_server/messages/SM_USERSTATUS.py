from NIO_python.messages.server.server_message import ServerMessage


class SM_USERSTATUS(ServerMessage):
    OP_CODE = 23

    def __init__(self, idx, status):
        ServerMessage.__init__(self)

        self.put_object(idx)
        self.put_int(status)

