import tkinter as tk

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("PLM - Tableau de Bord")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Bienvenue dans le PLM", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Déconnexion", command=self.logout).pack(pady=5)

    def logout(self):
        self.root.quit()  # Ferme l'application (peut être adapté pour revenir à la connexion)
