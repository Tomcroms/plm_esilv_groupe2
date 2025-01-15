class Product:
    def __init__(self, name, price, category, flacon_supplier, liquide_supplier, emballage_supplier):
        self.name = name
        self.price = price
        self.category = category
        self.flacon_supplier = flacon_supplier
        self.liquide_supplier = liquide_supplier
        self.emballage_supplier = emballage_supplier

    def to_dict(self):
        """Retourne un dictionnaire avec les données du produit."""
        return {
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "flacon_supplier": self.flacon_supplier,
            "liquide_supplier": self.liquide_supplier,
            "emballage_supplier": self.emballage_supplier
        }
