from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Liste d'utilisateurs à insérer
user_names = [
    "Alice",
    "Bob",
    "Charlie",
    "Diana",
    "Eve",
    ]

# Définir la base et la table
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

# Chemin vers la base de données SQLite
db_path = "app/assets/game.db"
engine = create_engine(f"sqlite:///{db_path}")

# Créer une session
Session = sessionmaker(bind=engine)
session = Session()


# Insérer les utilisateurs
for name in user_names:
    # Vérifier si l'utilisateur existe déjà
    if not session.query(User).filter_by(name=name).first():
        user = User(name=name)
        session.add(user)

# Valider les changements
session.commit()

# Fermer la session
session.close()

print("Utilisateurs ajoutés avec succès !")
