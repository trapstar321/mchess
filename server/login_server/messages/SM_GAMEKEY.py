from NIO_python.messages.server.server_message import ServerMessage


class SM_GAMEKEY(ServerMessage):
    OP_CODE = 16

    def __init__(self, ip, port, key):
        ServerMessage.__init__(self)

        self.put_string(ip)
        self.put_int(port)
        self.put_string(key)

