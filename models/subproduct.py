# models/subproduct.py

class SubProduct:
    def __init__(self, price, description, category, reference, nb_products=0, _id=None):
        self._id = _id
        self.price = price
        self.description = description
        self.category = category
        self.reference = reference
        self.nb_products = nb_products

    def to_dict(self):
        return {
            "_id": self._id,
            "price": self.price,
            "description": self.description,
            "category": self.category,
            "reference": self.reference,
            "nb_products": self.nb_products
        }
