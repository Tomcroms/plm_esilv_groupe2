from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Configuration de la session de la base de données
def init_db(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    global db_session
    Session = sessionmaker(bind=engine)
    db_session = Session()

# Ajoute plus tard des méthodes pour interagir avec la base de données
