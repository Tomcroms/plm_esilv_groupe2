import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController

class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.controller = UserController()
        self.on_login_success = on_login_success  # Callback pour passer à la vue principale

        # Initialisation de l'interface de connexion
        self.root.title("PLM - Connexion")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Connexion", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Nom d'utilisateur").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Mot de passe").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Se connecter", command=self.login).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = self.controller.login_user(username, password)
        if success:
            messagebox.showinfo("Succès", message)
            self.on_login_success()  # Appelle le callback pour ouvrir la vue principale
        else:
            messagebox.showerror("Erreur", message)
