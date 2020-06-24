class Response:
    def __init__(self, totalObjects: int, newLastWeek: int, catalogs: list):
        self.totalObjects = totalObjects
        self.newLastWeek = newLastWeek
        self.catalogs = catalogs
