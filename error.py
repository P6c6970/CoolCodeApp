class Error:
    def __init__(self, status="Ok", data=None):
        self.status = status
        self.data = data

    def get(self):
        return self.data

    def get_status(self):
        return self.status
