class Client():
    def __init__(self, row):
        self._id = row[0]
        self._name = row[1]
        self._id_user = row[2]

    def to_json(self):
        return {
            "id": self._id,
            "name": self._name,
            "id_user" : self._id_user
        }