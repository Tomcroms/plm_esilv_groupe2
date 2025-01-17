
from models.product import Product
from models.database import Database
from controllers.subproduct_controller import SubProductController
from controllers.concepteur_controller import ConcepteurController

class ProductController:
    def __init__(self):
        self.db = Database()
        self.product_collection = self.db.get_collection("products")
        self.subproduct_controller = SubProductController()
        self.concepteur_controller = ConcepteurController()

    def get_all_products(self):
        results = self.product_collection.find()
        products = []
        for r in results:
            p = Product(
                r["marge"],
                r["price"],
                r["description"],
                r["category"],
                r["image"],
                r["reference"],
                r["subproducts"],
                r["concepteur"],
                _id=r["_id"]
            )
            products.append(p)
        return products

    def create_product(self, marge, price, description, category, image, reference, subproduct_ids, concepteur_id):
        new_product = Product(marge, price, description, category, image, reference, subproduct_ids, concepteur_id)

        # Supprimer _id=None avant insertion
        product_dict = new_product.to_dict()
        if product_dict["_id"] is None:
            del product_dict["_id"]

        result = self.product_collection.insert_one(product_dict)
        return result.inserted_id

    # Méthode update (pour plus tard)
    # def update_product(self, product_id, updated_data):
    #     pass
