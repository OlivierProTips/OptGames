from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import challenges.orders as orders

# Configuration de la base de données (ajustez le chemin si nécessaire)
BASE_DIR = "app/game.db"
DB_PATH = f"sqlite:///{BASE_DIR}"

# Initialisation SQLAlchemy
Base = declarative_base()
engine = create_engine(DB_PATH)
Session = sessionmaker(bind=engine)
session = Session()

# Modèle de la table Challenge
class Challenge(Base):
    __tablename__ = 'challenges'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    flag = Column(String, nullable=False)
    file_url = Column(String)
    type = Column(String, nullable=False)
    order = Column(Integer, nullable=False, default=100)

def update_challenge_order(orders):
    """
    Met à jour le champ 'order' des challenges dans la base de données.

    :param orders: Liste d'objets ChallengeOrder avec les titres et ordres à mettre à jour.
    """
    for challenge_order in orders:
        # Rechercher et mettre à jour le challenge
        challenge = session.query(Challenge).filter(Challenge.title == challenge_order.title).first()
        if challenge:
            challenge.order = challenge_order.order
            print(f"Updated '{challenge.title}' with order {challenge.order}")
        else:
            print(f"Challenge with title '{challenge_order.title}' not found.")
    
    # Commit des changements dans la base de données
    session.commit()
    print("Order update completed.")

# Exemple d'utilisation
if __name__ == "__main__":
    update_challenge_order(orders)
