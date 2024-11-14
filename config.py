import os

# Configuration de la base de données en ligne
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///plm_database.db")

# D'autres paramètres globaux
PRODUCT_RANGES = {
    "Agrifood": ["AG_00CH000", "RE_00CH001"],
    "Perfumery": ["PE_00HGO000", "RE_00HGO001"]
}

# Références
REFERENCES = {
    "Agrifood": {
        "Standard": "AG_00CH000",
        "Modified": "RE_00CH001"
    },
    "Perfumery": {
        "Standard": "PE_00HGO000",
        "Modified": "RE_00HGO001"
    }
}
