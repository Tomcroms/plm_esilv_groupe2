from config import DATABASE_URL
from controllers.product_controller import ProductController
from controllers.user_controller import UserController
from models.database import init_db

def main():
    # Initialiser la base de données
    init_db(DATABASE_URL)

    # Créer un contrôleur utilisateur et un contrôleur produit
    user_controller = UserController()
    product_controller = ProductController()

    # Simulation de l'ajout d'un produit et de la gestion des références
    user_controller.login("admin")
    product_controller.create_product("Agrifood", "AG_00CH000", "Product description")
    product_controller.add_bom("Agrifood", "AG_00CH000", "BOM details")

    # Extraire la documentation pour l'invoice
    product_controller.extract_documentation("Agrifood", "AG_00CH000")

if __name__ == "__main__":
    main()
