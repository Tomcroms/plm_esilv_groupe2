# models/supplier.py

class Supplier:
    def __init__(self, name, location, subproducts_count=0, _id=None):
        self._id = _id
        self.name = name
        self.location = location
        self.subproducts_count = subproducts_count

    def to_dict(self):
        return {
            "_id": self._id,
            "name": self.name,
            "location": self.location,
            "subproducts_count": self.subproducts_count
        }
