from models.product import Product
from models.database import db_session
from models.lifecycle import BOM

class ProductController:
    def __init__(self):
        self.products = []

    def create_product(self, category, reference, description):
        product = Product(category=category, reference=reference, description=description)
        self.products.append(product)
        db_session.add(product)
        db_session.commit()
        print(f"Produit {reference} créé.")

    def add_bom(self, category, reference, details):
        product = self._get_product_by_reference(category, reference)
        if product:
            bom = BOM(product_id=product.id, details=details)
            db_session.add(bom)
            db_session.commit()
            print(f"BOM ajouté pour {reference}.")

    def extract_documentation(self, category, reference):
        product = self._get_product_by_reference(category, reference)
        if product:
            # Ici on peut ajouter une logique pour générer les documents d'approvisionnement et de facturation
            print(f"Documentation pour {reference} extraite.")

    def _get_product_by_reference(self, category, reference):
        return db_session.query(Product).filter_by(category=category, reference=reference).first()
