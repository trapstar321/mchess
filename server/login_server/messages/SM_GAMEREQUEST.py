from NIO_python.messages.server.server_message import ServerMessage


class SM_GAMEREQUEST(ServerMessage):
    OP_CODE = 9

    def __init__(self, request_id, client, username, flag):
        ServerMessage.__init__(self)

        self.put_object(request_id)
        self.put_object(client)
        self.put_string(username)
        self.put_int(flag)

