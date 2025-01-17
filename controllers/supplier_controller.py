# controllers/supplier_controller.py

from models.supplier import Supplier
from models.database import Database

class SupplierController:
    def __init__(self):
        self.db = Database()
        self.supplier_collection = self.db.get_collection("suppliers")

    def get_all_suppliers(self):
        results = self.supplier_collection.find()
        suppliers = []
        for r in results:
            s = Supplier(
                r["name"],
                r["location"],
                r.get("subproducts_count", 0),
                _id=r["_id"]
            )
            suppliers.append(s)
        return suppliers

    def create_supplier(self, name, location):
        new_supplier = Supplier(name, location)
        # Convertit l'objet en dictionnaire
        supplier_data = new_supplier.to_dict()
        
        # Supprime la clé _id si elle est None, pour laisser MongoDB générer un _id unique
        if supplier_data.get("_id") is None:
            del supplier_data["_id"]
        result = self.supplier_collection.insert_one(supplier_data)
        return result.inserted_id

    # Méthode update (pour plus tard)
    # def update_supplier(self, supplier_id, updated_data):
    #     pass
