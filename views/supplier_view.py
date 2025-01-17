# views/supplier_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.supplier_controller import SupplierController

class SupplierView(tk.Frame):
    def __init__(self, parent, user_role, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.user_role = user_role
        self.controller = SupplierController()

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Fournisseurs", font=("Arial", 14)).pack(pady=10)

        columns = ("name", "location", "subproducts_count", "actions")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("name", text="Nom")
        self.tree.heading("location", text="Localisation")
        self.tree.heading("subproducts_count", text="Nb Sous-Prod.")
        self.tree.heading("actions", text="Actions")

        for col in columns:
            self.tree.column(col, width=120)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bouton de création si rôle admin ou fournisseur
        if self.user_role in ["admin", "fournisseur"]:
            create_btn = tk.Button(self, text="Créer un Fournisseur", command=self.open_create_supplier_window)
            create_btn.pack(pady=5)

        self.load_suppliers()

        # Événement double-clic pour “Modifier”
        self.tree.bind("<Double-1>", self.on_double_click)

    def load_suppliers(self):
        # Vider la table avant de recharger
        for item in self.tree.get_children():
            self.tree.delete(item)

        suppliers = self.controller.get_all_suppliers()
        for sup in suppliers:
            self.tree.insert(
                "", tk.END,
                values=(sup.name, sup.location, sup.subproducts_count, "Modifier")
            )

    def on_double_click(self, event):
        item_id = self.tree.selection()
        if not item_id:
            return
        column = self.tree.identify_column(event.x)
        # La 4e colonne (#4) est "Actions"
        if column == "#4":
            # Implémentation de la modification lors d’une prochaine étape
            messagebox.showinfo("Modifier", "Fonction de modification non implémentée.")

    def open_create_supplier_window(self):
        win = tk.Toplevel(self)
        win.title("Créer un nouveau Fournisseur")

        tk.Label(win, text="Nom:").pack()
        name_entry = tk.Entry(win)
        name_entry.pack()

        tk.Label(win, text="Localisation:").pack()
        location_entry = tk.Entry(win)
        location_entry.pack()

        def create_supplier():
            name = name_entry.get()
            location = location_entry.get()
            if name and location:
                self.controller.create_supplier(name, location)
                messagebox.showinfo("Succès", "Fournisseur créé avec succès.")
                win.destroy()
                self.load_suppliers()
            else:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

        tk.Button(win, text="Créer", command=create_supplier).pack(pady=10)
