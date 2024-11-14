class UserController:
    def __init__(self):
        self.logged_in_user = None

    def login(self, username):
        # Authentifier l'utilisateur (simplifié)
        self.logged_in_user = username
        print(f"{username} connecté.")

    def logout(self):
        self.logged_in_user = None
        print("Déconnecté.")
