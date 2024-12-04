from models.database import Database

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password  # Note : En production, hachez les mots de passe
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }
