# models/concepteur.py

class Concepteur:
    def __init__(self, nom, prenom, description, nb_products=0, _id=None):
        self._id = _id
        self.nom = nom
        self.prenom = prenom
        self.description = description
        self.nb_products = nb_products

    def to_dict(self):
        return {
            "_id": self._id,
            "nom": self.nom,
            "prenom": self.prenom,
            "description": self.description,
            "nb_products": self.nb_products
        }
