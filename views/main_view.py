# views/main_view.py

import tkinter as tk
from tkinter import ttk
from views.supplier_view import SupplierView
from views.subproduct_view import SubProductView
from views.concepteur_view import ConcepteurView
from views.product_view import ProductView

class MainView:
    def __init__(self, root, user_role, logout_callback):
        self.root = root
        self.user_role = user_role
        self.logout_callback = logout_callback
        self.root.title(f"PLM - Tableau de Bord ({self.user_role})")
        self.setup_ui()

    def setup_ui(self):
        # Création du Notebook pour les onglets
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Onglet Fournisseurs
        tab_fournisseurs = SupplierView(notebook, self.user_role)
        notebook.add(tab_fournisseurs, text="Fournisseurs")

        # Onglet Sous Produits
        tab_subproducts = SubProductView(notebook, self.user_role)
        notebook.add(tab_subproducts, text="Sous Produits")

        # Onglet Concepteurs
        tab_concepteurs = ConcepteurView(notebook, self.user_role)
        notebook.add(tab_concepteurs, text="Concepteurs")

        # Onglet Produits
        tab_products = ProductView(notebook, self.user_role)
        notebook.add(tab_products, text="Produits")

        # Bouton Déconnexion en bas
        logout_btn = tk.Button(self.root, text="Déconnexion", command=self.logout)
        logout_btn.pack(pady=5)

    def logout(self):
        self.logout_callback()
