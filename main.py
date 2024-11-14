import tkinter as tk
from views.login_view import LoginView
from views.main_view import MainView

class App:
    def __init__(self, root):
        self.root = root
        self.show_login_view()

    def show_login_view(self):
        """Affiche la vue de connexion."""
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginView(self.root, on_login_success=self.show_main_view)

    def show_main_view(self):
        """Affiche la vue principale après connexion."""
        for widget in self.root.winfo_children():
            widget.destroy()
        MainView(self.root)

# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
