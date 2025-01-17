# controllers/concepteur_controller.py

from models.concepteur import Concepteur
from models.database import Database

class ConcepteurController:
    def __init__(self):
        self.db = Database()
        self.concepteur_collection = self.db.get_collection("concepteurs")

    def get_all_concepteurs(self):
        results = self.concepteur_collection.find()
        concepteurs = []
        for r in results:
            c = Concepteur(
                r["nom"],
                r["prenom"],
                r["description"],
                r.get("nb_products", 0),
                _id=r["_id"]
            )
            concepteurs.append(c)
        return concepteurs

    def create_concepteur(self, nom, prenom, description):
        new_concepteur = Concepteur(nom, prenom, description)
        # Convertit l'objet en dictionnaire
        concepteur_data = new_concepteur.to_dict()
        
        # Supprime la clé _id si elle est None, pour laisser MongoDB générer un _id unique
        if concepteur_data.get("_id") is None:
            del concepteur_data["_id"]
        result = self.concepteur_collection.insert_one(concepteur_data)
        return result.inserted_id

    # Méthode update (pour plus tard)
    # def update_concepteur(self, concepteur_id, updated_data):
    #     pass
