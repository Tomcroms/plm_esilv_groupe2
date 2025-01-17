# main.py
import tkinter as tk
from views.login_view import LoginView
from views.main_view import MainView
from views.register_view import RegisterView

class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x800")  # Définir la taille de la fenêtre
        self.show_login_view()

    def show_login_view(self):
        """Affiche la vue de connexion."""
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginView(self.root, on_login_success=self.show_main_view, show_register_view=self.show_register_view)

    def show_register_view(self):
        """Affiche la vue d'inscription."""
        for widget in self.root.winfo_children():
            widget.destroy()
        RegisterView(self.root, show_login_view=self.show_login_view)

    def show_main_view(self, user_role):
        """Affiche la vue principale après connexion."""
        for widget in self.root.winfo_children():
            widget.destroy()
        MainView(self.root, user_role=user_role, logout_callback=self.show_login_view)

# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
