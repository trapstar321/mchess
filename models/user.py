class User:
    def __init__(self, client_id, username):
        self.client_id = client_id
        self.username = username
        self.index = None

    def set_index(self, index):
        self.index = index

    def get_key(self):
        return self.client_id

    def __str__(self):
        return self.username
