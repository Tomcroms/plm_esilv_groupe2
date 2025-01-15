from models.database import Database
from models.product import Product

class ProductController:
    def __init__(self):
        self.db = Database()
        self.products_collection = self.db.get_collection('products')
        self.suppliers_collection = self.db.get_collection('suppliers')  # Nouvelle collection pour les fournisseurs

    # Récupérer tous les produits
    def get_all_products(self):
        """Récupère tous les produits dans la base de données."""
        products = self.products_collection.find()
        return list(products)

    # Ajouter un produit
    def create_product(self, name, price, flacon_supplier, liquide_supplier, emballage_supplier, category):
        """Crée un produit dans la base de données."""
        product = {
            "name": name,
            "price": price,
            "category": category,
            "flacon_supplier": flacon_supplier,
            "liquide_supplier": liquide_supplier,
            "emballage_supplier": emballage_supplier,
        }
        try:
            self.products_collection.insert_one(product)
            return True, "Produit créé avec succès."
        except Exception as e:
            return False, f"Erreur lors de la création du produit : {e}"

    # Récupérer tous les fournisseurs
    def get_all_suppliers(self):
        """Récupère tous les fournisseurs dans la base de données."""
        suppliers = self.suppliers_collection.find()
        return [{"type": supplier["type"], "name": supplier["name"], "furnishing_type": supplier["furnishing_type"], "version": supplier["version"]} for supplier in suppliers]

    # Ajouter un fournisseur
    def create_supplier(self, supplier_name, furnishing_type, version):
        """Crée un fournisseur dans la base de données."""
        supplier = {
            "name": supplier_name,
            "furnishing_type": furnishing_type,
            "version": version,
        }

        try:
            self.suppliers_collection.insert_one(supplier)
            return True, "Fournisseur créé avec succès."
        except Exception as e:
            return False, f"Erreur lors de la création du fournisseur : {e}"
