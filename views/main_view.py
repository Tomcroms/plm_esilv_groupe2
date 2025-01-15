import tkinter as tk
from tkinter import ttk, messagebox
from controllers.product_controller import ProductController

class MainView:
    def __init__(self, root, user_role, logout_callback):
        self.root = root
        self.user_role = user_role
        self.logout_callback = logout_callback
        self.product_controller = ProductController()  # Ajouter le contrôleur des produits
        self.root.title(f"PLM - Tableau de Bord ({self.user_role})")
        self.setup_ui()

    def setup_ui(self):
        # Frame principale pour la gestion de l'interface
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # Frame pour les boutons sur la gauche
        left_frame = tk.Frame(main_frame, width=200, bg="#2e3b4e", relief="sunken")
        left_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5)

        # Frame pour le contenu à droite, qui changera selon les actions de l'utilisateur
        self.right_frame = tk.Frame(main_frame, bg="#f4f4f4")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Configuration des grilles pour le redimensionnement
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Boutons de navigation dans le menu
        tk.Button(left_frame, text="Gestion des produits", command=self.show_product_management, bg="#3e4a61", fg="white", relief="flat").pack(fill="x", pady=10)

        if self.user_role in ['admin', 'concepteur']:
            tk.Button(left_frame, text="Créer un produit", command=self.show_create_product_page, bg="#3e4a61", fg="white", relief="flat").pack(fill="x", pady=10)
            tk.Button(left_frame, text="Gestion des fournisseurs", command=self.show_supplier_management, bg="#3e4a61", fg="white", relief="flat").pack(fill="x", pady=10)

        tk.Button(left_frame, text="Déconnexion", command=self.logout, bg="#f44336", fg="white", relief="flat").pack(fill="x", pady=10)

        # Mise à jour du contenu de la fenêtre de droite
        self.show_welcome()

    def show_welcome(self):
        """Affiche l'écran d'accueil dans la partie droite."""
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        tk.Label(self.right_frame, text=f"Bienvenue {self.user_role} dans le PLM", font=("Arial", 16), bg="#f4f4f4").pack(pady=20)

    def show_product_management(self):
        """Affiche la gestion des produits dans la partie droite."""
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        if self.user_role in ['admin', 'concepteur']:
            tk.Label(self.right_frame, text="Gestion des produits", font=("Arial", 16)).pack(pady=20)

            # Tableau des produits
            self.display_product_table()
        else:
            self.show_product_view()

    def show_product_view(self):
        """Affiche seulement la liste des produits pour les visiteurs et fournisseurs."""
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        tk.Label(self.right_frame, text="Produits disponibles", font=("Arial", 16)).pack(pady=20)
        self.display_product_table()

    def display_product_table(self):
        """Affiche les produits dans un tableau avec Treeview."""
        products = self.product_controller.get_all_products()  # Récupère tous les produits

        # Créer le tableau
        tree = ttk.Treeview(self.right_frame, columns=("Nom", "Prix", "Fournisseur", "Catégorie", "Stock"), show="headings", height=15)
        tree.pack(fill="both", expand=True)

        # Configurer les colonnes
        tree.heading("Nom", text="Nom du produit")
        tree.heading("Prix", text="Prix (€)")
        tree.heading("Fournisseur", text="Fournisseur")
        tree.heading("Catégorie", text="Catégorie")
        tree.heading("Stock", text="Stock")

        tree.column("Nom", width=150, anchor="w")
        tree.column("Prix", width=80, anchor="center")
        tree.column("Fournisseur", width=150, anchor="w")
        tree.column("Catégorie", width=100, anchor="center")
        tree.column("Stock", width=80, anchor="center")

        # Ajouter les produits au tableau
        for product in products:
            category_color = "#ffcc99" if product['category'] == "flacon" else "#add8e6"
            tree.insert("", "end", values=(product['name'], product['price'], product['supplier'], product['category'], product['stock']),
                        tags=(category_color,))

        # Appliquer des couleurs aux catégories
        tree.tag_configure("#ffcc99", background="#ffcc99")  # Orange pastel pour flacons
        tree.tag_configure("#add8e6", background="#add8e6")  # Bleu pastel pour bouteilles

    def show_create_product_page(self):
        """Affiche la page de création de produit uniquement pour Admin et Concepteur."""
        if self.user_role not in ['admin', 'concepteur']:
            messagebox.showerror("Accès non autorisé", "Vous n'avez pas l'autorisation de créer un produit.")
            return

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        tk.Label(self.right_frame, text="Créer un nouveau produit", font=("Arial", 16)).pack(pady=10)

        # Champs pour entrer les informations du produit
        self.create_product_fields()

    def create_product_fields(self):
        """Ajoute les champs pour la création d'un produit avec fournisseurs et catégorie."""
        tk.Label(self.right_frame, text="Nom du produit:").pack(anchor="w", padx=10)
        name_entry = tk.Entry(self.right_frame)
        name_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(self.right_frame, text="Prix (€):").pack(anchor="w", padx=10)
        price_entry = tk.Entry(self.right_frame)
        price_entry.pack(fill="x", padx=10, pady=5)

        tk.Label(self.right_frame, text="Fournisseur pour Flacon:").pack(anchor="w", padx=10)
        flacon_supplier = self.create_supplier_dropdown()
        flacon_supplier.pack(fill="x", padx=10, pady=5)

        tk.Label(self.right_frame, text="Fournisseur pour Liquide:").pack(anchor="w", padx=10)
        liquide_supplier = self.create_supplier_dropdown()
        liquide_supplier.pack(fill="x", padx=10, pady=5)

        tk.Label(self.right_frame, text="Fournisseur pour Emballage:").pack(anchor="w", padx=10)
        emballage_supplier = self.create_supplier_dropdown()
        emballage_supplier.pack(fill="x", padx=10, pady=5)

        tk.Label(self.right_frame, text="Catégorie (bouteille ou flacon):").pack(anchor="w", padx=10)
        category_dropdown = self.create_category_dropdown()
        category_dropdown.pack(fill="x", padx=10, pady=5)

        tk.Button(self.right_frame, text="Créer", command=lambda: self.create_product(name_entry, price_entry, flacon_supplier, liquide_supplier, emballage_supplier, category_dropdown)).pack(pady=20)

    def create_supplier_dropdown(self):
        """Retourne une liste déroulante des fournisseurs existants."""
        suppliers = self.product_controller.get_all_suppliers()  # Utiliser la méthode pour récupérer les fournisseurs
        supplier_var = tk.StringVar()
        supplier_dropdown = tk.OptionMenu(self.right_frame, supplier_var, *suppliers)
        return supplier_dropdown

    def create_category_dropdown(self):
        """Retourne une liste déroulante pour choisir la catégorie (bouteille ou flacon)."""
        category_var = tk.StringVar()
        category_dropdown = tk.OptionMenu(self.right_frame, category_var, "bouteille", "flacon")
        return category_dropdown

    def create_product(self, name_entry, price_entry, flacon_supplier, liquide_supplier, emballage_supplier, category_dropdown):
        """Crée un nouveau produit dans la base de données."""
        name = name_entry.get()
        price = price_entry.get()
        flacon_supplier = flacon_supplier.get()
        liquide_supplier = liquide_supplier.get()
        emballage_supplier = emballage_supplier.get()
        category = category_dropdown.get()

        if not all([name, price, flacon_supplier, liquide_supplier, emballage_supplier, category]):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        success, message = self.product_controller.create_product(name, float(price), flacon_supplier, liquide_supplier, emballage_supplier, category)
        if success:
            messagebox.showinfo("Succès", message)
            self.show_product_management()
        else:
            messagebox.showerror("Erreur", message)

    def show_supplier_management(self):
        """Affiche la gestion des fournisseurs dans la partie droite."""
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        tk.Label(self.right_frame, text="Gestion des fournisseurs", font=("Arial", 16)).pack(pady=10)

        # Afficher la liste des fournisseurs
        self.display_supplier_table()

        # Ajouter un bouton pour créer un fournisseur
        tk.Button(self.right_frame, text="Créer un nouveau fournisseur", command=self.show_create_supplier_page, bg="#4CAF50", fg="white").pack(pady=10)

    def logout(self):
        """Retourne à la vue de connexion."""
        self.logout_callback()
