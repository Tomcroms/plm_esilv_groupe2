# controllers/subproduct_controller.py

from models.subproduct import SubProduct
from models.database import Database

class SubProductController:
    def __init__(self):
        self.db = Database()
        self.subproduct_collection = self.db.get_collection("subproducts")

    def get_all_subproducts(self):
        results = self.subproduct_collection.find()
        subproducts = []
        for r in results:
            sp = SubProduct(
                r["price"],
                r["description"],
                r["category"],
                r["reference"],
                r.get("nb_products", 0),
                _id=r["_id"]
            )
            subproducts.append(sp)
        return subproducts

    def create_subproduct(self, price, description, category, reference):
        new_subproduct = SubProduct(price, description, category, reference)

        # Convertit l'objet en dictionnaire
        subproduct_data = new_subproduct.to_dict()

        # Supprime la clé _id si elle est None, pour éviter d'insérer _id = null
        if subproduct_data.get("_id") is None:
            del subproduct_data["_id"]

        # Insère le document, MongoDB génèrera l'_id automatiquement
        result = self.subproduct_collection.insert_one(subproduct_data)
        return result.inserted_id

    # Méthode update (pour plus tard)
    # def update_subproduct(self, subproduct_id, updated_data):
    #     pass
