class User:
    def __init__(self, client_id, username, status):
        self.client_id = client_id
        self.username = username
        self.index = None
        self.status = status

    def set_index(self, index):
        self.index = index

    def get_key(self):
        return self.client_id

    def set_status(self, status):
        self.status = status

    def __str__(self):
        return self.username + (" (in game)" if self.status == 1 else "")
