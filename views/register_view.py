import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController

class RegisterView:
    def __init__(self, root, show_login_view):
        self.root = root
        self.controller = UserController()
        self.show_login_view = show_login_view  # Callback pour revenir à la vue de connexion

        # Initialisation de l'interface d'inscription
        self.root.title("PLM - Inscription")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Inscription", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Nom d'utilisateur").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Mot de passe").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Label(self.root, text="Rôle").pack()
        self.role_var = tk.StringVar()
        self.role_var.set("client")  # Valeur par défaut
        roles = ["admin", "user", "client"]
        self.role_menu = tk.OptionMenu(self.root, self.role_var, *roles)
        self.role_menu.pack()

        tk.Label(self.root, text="Code (si nécessaire)").pack()
        self.code_entry = tk.Entry(self.root)
        self.code_entry.pack()

        tk.Button(self.root, text="S'inscrire", command=self.register).pack(pady=5)
        tk.Button(self.root, text="Retour à la connexion", command=self.show_login_view).pack(pady=5)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()
        code = self.code_entry.get()

        success, message = self.controller.register_user(username, password, role, code)
        if success:
            messagebox.showinfo("Succès", message)
            self.show_login_view()  # Retourne à la vue de connexion après inscription
        else:
            messagebox.showerror("Erreur", message)
