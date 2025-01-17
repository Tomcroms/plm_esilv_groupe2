from models.user import User
from models.database import Database

class UserController:
    def __init__(self):
        self.db = Database()
        self.users_collection = self.db.get_collection('users')

    def register_user(self, username, password, role, code=None):
        # Vérifier si l'utilisateur existe déjà
        if self.users_collection.find_one({"username": username}):
            return False, "Nom d'utilisateur déjà pris."

        # Vérifier le rôle et le code
        if role == 'admin' and code != 'admin':
            return False, "Code incorrect pour créer un compte administrateur."
        elif role == 'concepteur' and code != 'concepteur':
            return False, "Code incorrect pour créer un compte concepteur."
        elif role == 'fournisseur' and code != 'fournisseur':
            return False, "Code incorrect pour créer un compte fournisseur."
        elif role == 'visiteur' and code:
            return False, "Aucun code requis pour créer un compte visiteur."

        # Créer l'utilisateur
        user = User(username, password, role)
        self.users_collection.insert_one(user.to_dict())
        return True, "Compte créé avec succès."

    def login_user(self, username, password):
        user = self.users_collection.find_one({"username": username, "password": password})
        if user:
            return True, "Connexion réussie.", user['role']
        else:
            return False, "Nom d'utilisateur ou mot de passe incorrect.", None