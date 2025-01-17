
class Product:
    def __init__(self, marge, price, description, category, image, reference, subproducts, concepteur, _id=None):
        self._id = _id
        self.marge = marge
        self.price = price
        self.description = description
        self.category = category
        self.image = image
        self.reference = reference
        self.subproducts = subproducts  # liste d'IDs ou de références des sous produits
        self.concepteur = concepteur    # ID ou référence du concepteur

    def to_dict(self):
        return {
            "_id": self._id,
            "marge": self.marge,
            "price": self.price,
            "description": self.description,
            "category": self.category,
            "image": self.image,
            "reference": self.reference,
            "subproducts": self.subproducts,
            "concepteur": self.concepteur
        }
