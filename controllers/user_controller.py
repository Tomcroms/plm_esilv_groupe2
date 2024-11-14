from models.database import Database
from hashlib import sha256

class UserController:
    def __init__(self):
        self.db = Database()
        self.users = self.db.get_collection("users")

    def register_user(self, username, password):
        """Enregistre un nouvel utilisateur avec un mot de passe hashé."""
        hashed_password = sha256(password.encode()).hexdigest()
        if self.users.find_one({"username": username}):
            return False, "Nom d'utilisateur déjà pris."
        self.users.insert_one({"username": username, "password": hashed_password})
        return True, "Inscription réussie."

    def login_user(self, username, password):
        """Vérifie les identifiants d'un utilisateur."""
        hashed_password = sha256(password.encode()).hexdigest()
        user = self.users.find_one({"username": username, "password": hashed_password})
        if user:
            return True, "Connexion réussie."
        return False, "Nom d'utilisateur ou mot de passe incorrect."
