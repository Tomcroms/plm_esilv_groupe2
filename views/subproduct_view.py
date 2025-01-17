# views/subproduct_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from controllers.subproduct_controller import SubProductController

class SubProductView(tk.Frame):
    def __init__(self, parent, user_role, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.user_role = user_role
        self.controller = SubProductController()

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Sous Produits", font=("Arial", 14)).pack(pady=10)

        columns = ("price", "description", "category", "reference", "nb_products", "actions")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("price", text="Prix")
        self.tree.heading("description", text="Description")
        self.tree.heading("category", text="Catégorie")
        self.tree.heading("reference", text="Référence")
        self.tree.heading("nb_products", text="Nb Produits")
        self.tree.heading("actions", text="Actions")

        for col in columns:
            self.tree.column(col, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bouton de création si rôle admin ou fournisseur
        if self.user_role in ["admin", "fournisseur"]:
            create_btn = tk.Button(self, text="Créer un Sous Produit", command=self.open_create_subproduct_window)
            create_btn.pack(pady=5)

        self.load_subproducts()

        # Événement double-clic pour “Modifier”
        self.tree.bind("<Double-1>", self.on_double_click)

    def load_subproducts(self):
        # Vider la table
        for item in self.tree.get_children():
            self.tree.delete(item)

        subproducts = self.controller.get_all_subproducts()
        for sp in subproducts:
            self.tree.insert(
                "", tk.END,
                values=(sp.price, sp.description, sp.category, sp.reference, sp.nb_products, "Modifier")
            )

    def on_double_click(self, event):
        item_id = self.tree.selection()
        if not item_id:
            return
        column = self.tree.identify_column(event.x)
        # La 6e colonne (#6) est "Actions"
        if column == "#6":
            messagebox.showinfo("Modifier", "Fonction de modification non implémentée.")

    def open_create_subproduct_window(self):
        win = tk.Toplevel(self)
        win.title("Créer un Sous Produit")

        tk.Label(win, text="Prix:").pack()
        price_entry = tk.Entry(win)
        price_entry.pack()

        tk.Label(win, text="Description:").pack()
        desc_entry = tk.Entry(win)
        desc_entry.pack()

        tk.Label(win, text="Catégorie (récipient/liquide/emballage):").pack()
        cat_var = tk.StringVar(value="récipient")
        cat_menu = tk.OptionMenu(win, cat_var, "récipient", "liquide", "emballage")
        cat_menu.pack()

        tk.Label(win, text="Référence:").pack()
        ref_entry = tk.Entry(win)
        ref_entry.pack()

        def create_subproduct():
            price = price_entry.get()
            description = desc_entry.get()
            category = cat_var.get()
            reference = ref_entry.get()

            if price and description and category and reference:
                try:
                    price_val = float(price)
                except ValueError:
                    messagebox.showerror("Erreur", "Le prix doit être un nombre.")
                    return

                self.controller.create_subproduct(price_val, description, category, reference)
                messagebox.showinfo("Succès", "Sous Produit créé avec succès.")
                win.destroy()
                self.load_subproducts()
            else:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")

        tk.Button(win, text="Créer", command=create_subproduct).pack(pady=10)
