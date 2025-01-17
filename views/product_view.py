# views/product_view.py

import tkinter as tk
from tkinter import ttk, messagebox
import os

from PIL import Image, ImageTk

from controllers.product_controller import ProductController
from controllers.subproduct_controller import SubProductController
from controllers.concepteur_controller import ConcepteurController


def sanitize_for_tk(value):
    """
    Retire ou échappe les accolades (et éventuels backslashes) 
    afin d'éviter l'erreur _tkinter.TclError dans un Treeview.
    """
    # Version simple : on retire juste les accolades
    s = str(value).replace("{", "").replace("}", "")
    # Optionnel : tu peux aussi retirer/backslasher d'autres caractères spéciaux
    return s


class ProductView(tk.Frame):
    def __init__(self, parent, user_role, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.images_cache = {}
        self.user_role = user_role

        self.product_controller = ProductController()
        self.subproduct_controller = SubProductController()
        self.concepteur_controller = ConcepteurController()

        # Chargement des sous-produits et concepteurs existants
        self.subproducts_data = self.subproduct_controller.get_all_subproducts()
        self.concepteurs_data = self.concepteur_controller.get_all_concepteurs()

        self.setup_ui()

        # On charge la liste des produits après avoir défini l'UI
        self.load_products()

    def setup_ui(self):
        tk.Label(self, text="Produits", font=("Arial", 14)).pack(pady=10)

        # Déclare 8 colonnes en plus de la colonne #0 (dite "tree")
        columns = ("marge", "price", "description", "category", "reference", "subproducts", "concepteur", "actions")

        # show="tree headings" -> on affiche la colonne #0 (le "tree") + les headings
        self.tree = ttk.Treeview(self, columns=columns, show="tree headings")

        # Personnalise la colonne #0 (pour l'image)
        self.tree.heading("#0", text="Image")
        self.tree.column("#0", width=140)

        # Définition des en-têtes (headings) pour les colonnes
        self.tree.heading("marge", text="Marge")
        self.tree.heading("price", text="Prix")
        self.tree.heading("description", text="Description")
        self.tree.heading("category", text="Catégorie")
        self.tree.heading("reference", text="Référence")
        self.tree.heading("subproducts", text="Sous Produits")
        self.tree.heading("concepteur", text="Concepteur")
        self.tree.heading("actions", text="Actions")

        # Ajuste la largeur si nécessaire
        for col in columns:
            self.tree.column(col, width=110)

        self.tree.pack(fill=tk.BOTH, expand=True)
        # Bouton de création si rôle admin ou concepteur
        if self.user_role in ["admin", "concepteur"]:
            create_btn = tk.Button(self, text="Créer un Produit", command=self.open_create_product_window)
            create_btn.pack(pady=5)

        # Double-clic pour "Modifier" (à implémenter plus tard)
        self.tree.bind("<Double-1>", self.on_double_click)

    def load_products(self):
        # Vider la table
        for item in self.tree.get_children():
            self.tree.delete(item)

        products = self.product_controller.get_all_products()
        # Réinitialiser notre cache d'images pour éviter le garbage collector
        self.images_cache = {}

        for p in products:
            # 1) Charger l'image (si fichier existe dans img/<nom_fichier>)
            image_path = os.path.join("img", p.image)  # ex: "img/image1.png"
            tk_photo = None
            if os.path.isfile(image_path):
                try:
                    pil_img = Image.open(image_path)
                    pil_img = pil_img.resize((100, 100), Image.LANCZOS)  # Redimensionne à 100x100 pixels
                    tk_photo = ImageTk.PhotoImage(pil_img)
                    # On stocke la référence dans un dict pour éviter le garbage collector
                    self.images_cache[p._id] = tk_photo
                except Exception as e:
                    print("Impossible de charger l'image :", image_path, e)

            # 2) Préparer les chaînes pour éviter les accolades
            marge_str = sanitize_for_tk(p.marge)
            price_str = sanitize_for_tk(p.price)
            desc_str = sanitize_for_tk(p.description)
            category_str = sanitize_for_tk(p.category)
            reference_str = sanitize_for_tk(p.reference)

            # subproducts : on les affiche en liste, ex. "id1, id2, id3"
            subp_str = ", ".join(str(sp_id) for sp_id in p.subproducts)
            subp_str = sanitize_for_tk(subp_str)

            concepteur_str = sanitize_for_tk(p.concepteur)

            # 3) Insertion dans le Treeview
            self.tree.insert(
                "",
                tk.END,
                text="",        # texte de la colonne #0 (on n'affiche rien)
                image=tk_photo, # on y met l'image
                values=(
                    marge_str,
                    price_str,
                    desc_str,
                    category_str,
                    reference_str,
                    subp_str,
                    concepteur_str,
                    "Modifier"
                ),
            )

    def on_double_click(self, event):
        item_id = self.tree.selection()
        if not item_id:
            return
        column = self.tree.identify_column(event.x)
        # La 8e colonne (valeurs = "marge", "price", "desc", "cat", "ref", "subp", "conc", "#8=actions")
        if column == "#8":
            messagebox.showinfo("Modifier", "Fonction de modification non implémentée.")

    def open_create_product_window(self):
        win = tk.Toplevel(self)
        win.title("Créer un nouveau Produit")

        # VARIABLES DE SAISIE
        marge_var = tk.StringVar()
        description_var = tk.StringVar()
        category_var = tk.StringVar(value="flacon")  # flacon/bouteille
        image_var = tk.StringVar()
        reference_var = tk.StringVar()

        # Affichage dynamique du prix
        price_var = tk.StringVar(value="0.0")

        # Champs basiques
        tk.Label(win, text="Marge:").pack()
        marge_entry = tk.Entry(win, textvariable=marge_var)
        marge_entry.pack()

        tk.Label(win, text="Description:").pack()
        desc_entry = tk.Entry(win, textvariable=description_var)
        desc_entry.pack()

        tk.Label(win, text="Catégorie (flacon/bouteille):").pack()
        cat_menu = tk.OptionMenu(win, category_var, "flacon", "bouteille")
        cat_menu.pack()

        tk.Label(win, text="Image (fichier.png dans img/):").pack()
        image_entry = tk.Entry(win, textvariable=image_var)
        image_entry.pack()

        tk.Label(win, text="Référence Produit:").pack()
        ref_entry = tk.Entry(win, textvariable=reference_var)
        ref_entry.pack()

        # --- FILTRAGE DES SOUS-PRODUITS PAR CATÉGORIE ---
        subproducts_recip = [sp for sp in self.subproducts_data if sp.category == "récipient"]
        subproducts_liquide = [sp for sp in self.subproducts_data if sp.category == "liquide"]
        subproducts_emballage = [sp for sp in self.subproducts_data if sp.category == "emballage"]

        # Format "ID - REF - PRIX"
        subp_recip_options = [f"{sp._id} - {sp.reference} - {sp.price}" for sp in subproducts_recip]
        subp_liquide_options = [f"{sp._id} - {sp.reference} - {sp.price}" for sp in subproducts_liquide]
        subp_emballage_options = [f"{sp._id} - {sp.reference} - {sp.price}" for sp in subproducts_emballage]

        subp_var1 = tk.StringVar()  # récipient
        subp_var2 = tk.StringVar()  # liquide
        subp_var3 = tk.StringVar()  # emballage

        tk.Label(win, text="Sous Produit (récipient):").pack()
        subp_menu1 = tk.OptionMenu(win, subp_var1, *subp_recip_options)
        subp_menu1.pack()

        tk.Label(win, text="Sous Produit (liquide):").pack()
        subp_menu2 = tk.OptionMenu(win, subp_var2, *subp_liquide_options)
        subp_menu2.pack()

        tk.Label(win, text="Sous Produit (emballage):").pack()
        subp_menu3 = tk.OptionMenu(win, subp_var3, *subp_emballage_options)
        subp_menu3.pack()

        # Concepteur
        tk.Label(win, text="Concepteur:").pack()
        conc_var = tk.StringVar(value="")
        conc_options = [f"{c._id} - {c.nom} {c.prenom}" for c in self.concepteurs_data]
        conc_menu = tk.OptionMenu(win, conc_var, *conc_options)
        conc_menu.pack()

        # Calcul du prix total
        def update_total_price(*args):
            try:
                marge_val = float(marge_var.get())
            except ValueError:
                marge_val = 0.0

            subp_sum = 0.0
            for var in (subp_var1, subp_var2, subp_var3):
                val = var.get()
                if val:
                    parts = val.split(" - ")
                    if len(parts) == 3:
                        try:
                            subp_sum += float(parts[2])
                        except ValueError:
                            pass
            total_price = marge_val + subp_sum
            price_var.set(str(total_price))

        # Traces
        marge_var.trace("w", update_total_price)
        subp_var1.trace("w", update_total_price)
        subp_var2.trace("w", update_total_price)
        subp_var3.trace("w", update_total_price)

        tk.Label(win, text="Prix total (calculé):").pack()
        tk.Label(win, textvariable=price_var, font=("Arial", 12, "bold")).pack(pady=5)

        # Création du produit
        def create_product():
            marge = marge_var.get()
            description = description_var.get()
            category = category_var.get()
            image = image_var.get()
            reference = reference_var.get()

            subp_ids = []
            for var in (subp_var1, subp_var2, subp_var3):
                if var.get():
                    parts = var.get().split(" - ")
                    subp_id = parts[0]  # L'_id
                    subp_ids.append(subp_id)

            conc_id = None
            if conc_var.get():
                conc_id = conc_var.get().split(" - ")[0]

            # Vérif
            if not (marge and description and category and reference and subp_ids and conc_id):
                messagebox.showerror(
                    "Erreur",
                    "Veuillez renseigner marge, description, catégorie, référence, 3 sous-produits et un concepteur."
                )
                return

            try:
                marge_val = float(marge)
            except ValueError:
                messagebox.showerror("Erreur", "La marge doit être un nombre.")
                return

            price_str = price_var.get()
            try:
                price_val = float(price_str)
            except ValueError:
                messagebox.showerror("Erreur", "Le prix calculé est invalide.")
                return

            # Appel au contrôleur
            # Nota: si tu veux passer price_val pour l'enregistrer vraiment
            # modifie la signature create_product(...) pour accepter le param price
            self.product_controller.create_product(
                marge_val, 
                price_val,       #  <-- on ajoute le price ici
                description,
                category,
                image,
                reference,
                subp_ids,
                conc_id
            )
            messagebox.showinfo("Succès", "Produit créé avec succès.")
            win.destroy()
            self.load_products()

        tk.Button(win, text="Créer le Produit", command=create_product).pack(pady=10)
