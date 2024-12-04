import tkinter as tk

class MainView:
    def __init__(self, root, user_role, logout_callback):
        self.root = root
        self.user_role = user_role
        self.logout_callback = logout_callback
        self.root.title(f"PLM - Tableau de Bord ({self.user_role})")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text=f"Bienvenue {self.user_role} dans le PLM", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Déconnexion", command=self.logout).pack(pady=5)

    def logout(self):
        self.logout_callback()  # Retourne à la vue de connexion
