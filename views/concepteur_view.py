# views/concepteur_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.concepteur_controller import ConcepteurController

class ConcepteurView(tk.Frame):
    def __init__(self, parent, user_role, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.user_role = user_role
        self.controller = ConcepteurController()

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Concepteurs", font=("Arial", 14)).pack(pady=10)

        columns = ("nom", "prenom", "description", "nb_products", "actions")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("nom", text="Nom")
        self.tree.heading("prenom", text="Prénom")
        self.tree.heading("description", text="Description")
        self.tree.heading("nb_products", text="Nb Produits")
        self.tree.heading("actions", text="Actions")

        for col in columns:
            self.tree.column(col, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bouton de création si rôle admin ou concepteur
        if self.user_role in ["admin", "concepteur"]:
            create_btn = tk.Button(self, text="Créer un Concepteur", command=self.open_create_concepteur_window)
            create_btn.pack(pady=5)

        self.load_concepteurs()

        # Événement double-clic pour “Modifier”
        self.tree.bind("<Double-1>", self.on_double_click)

    def load_concepteurs(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        concepteurs = self.controller.get_all_concepteurs()
        for c in concepteurs:
            self.tree.insert(
                "", tk.END,
                values=(c.nom, c.prenom, c.description, c.nb_products, "Modifier")
            )

    def on_double_click(self, event):
        item_id = self.tree.selection()
        if not item_id:
            return
        column = self.tree.identify_column(event.x)
        # La 5e colonne (#5) est "Actions"
        if column == "#5":
            messagebox.showinfo("Modifier", "Fonction de modification non implémentée.")

    def open_create_concepteur_window(self):
        win = tk.Toplevel(self)
        win.title("Créer un nouveau Concepteur")

        tk.Label(win, text="Nom:").pack()
        nom_entry = tk.Entry(win)
        nom_entry.pack()

        tk.Label(win, text="Prénom:").pack()
        prenom_entry = tk.Entry(win)
        prenom_entry.pack()

        tk.Label(win, text="Description:").pack()
        desc_entry = tk.Entry(win)
        desc_entry.pack()

        def create_concepteur():
            nom = nom_entry.get()
            prenom = prenom_entry.get()
            description = desc_entry.get()
            if nom and prenom and description:
                self.controller.create_concepteur(nom, prenom, description)
                messagebox.showinfo("Succès", "Concepteur créé avec succès.")
                win.destroy()
                self.load_concepteurs()
            else:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

        tk.Button(win, text="Créer", command=create_concepteur).pack(pady=10)
