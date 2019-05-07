class GameRequest:
    def __init__(self, request_id, client_id, username, flag):
        self.request_id = request_id
        self.client_id = client_id
        self.flag = flag
        self.username = username
        self.index = None

    def set_index(self, index):
        self.index = index

    def get_key(self):
        return self.request_id

    def __str__(self):
        if self.flag == 0:
            return "From {0}".format(self.username)
        elif self.flag == 1:
            return "To {0}".format(self.username)
        return ""
