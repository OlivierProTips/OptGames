import os
import shutil
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
import vars

# Définition de la base de données et des modèles SQLAlchemy
Base = declarative_base()

# Modèle pour les challenges
class Challenge(Base):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(Text)
    flag = Column(String, nullable=False)
    file_url = Column(String)
    type = Column(String, nullable=False)

# Modèle pour les utilisateurs
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

# Modèle pour les résultats
class Result(Base):
    __tablename__ = 'results'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    challenge_id = Column(Integer, ForeignKey('challenges.id'), primary_key=True)

# Modèle pour les paramètres
class Setting(Base):
    __tablename__ = 'settings'

    name = Column(String, unique=True)
    value = Column(String)

# Initialisation de la base de données
db_path = f"{vars.ASSET_DIR}/game.db"
engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Chemins de répertoire
challenges_dir = 'challenges'
assets_dir = f"{vars.ASSET_DIR}/files"
os.makedirs(assets_dir, exist_ok=True)

# Fonction pour insérer un challenge
def insert_challenge(title, description, flag, file_url, challenge_type):
    # Vérifier si le challenge existe déjà
    existing_challenge = session.query(Challenge).filter_by(title=title).first()
    if not existing_challenge:
        new_challenge = Challenge(
            title=title,
            description=description,
            flag=flag,
            file_url=file_url,
            type=challenge_type
        )
        session.add(new_challenge)
        session.commit()
        print(f'Challenge "{title}" inséré dans la base de données.')
    else:
        print(f'Challenge "{title}" existe déjà dans la base de données.')

# Parcours des répertoires de challenges
for challenge_name in os.listdir(challenges_dir):
    challenge_path = os.path.join(challenges_dir, challenge_name)
    if os.path.isdir(challenge_path):  # Vérifier que c'est un répertoire
        # Lecture des fichiers description.txt et flag.txt
        description_path = os.path.join(challenge_path, 'description.txt')
        flag_path = os.path.join(challenge_path, 'flag.txt')
        
        if not (os.path.exists(description_path) and os.path.exists(flag_path)):
            print(f"Les fichiers 'description.txt' et/ou 'flag.txt' n'existent pas pour {challenge_name}.")
            continue

        with open(description_path, 'r') as f:
            description = f.read().strip()

        with open(flag_path, 'r') as f:
            flag = f.read().strip()

        # Vérifier si le répertoire file existe et contient un fichier
        file_url = None
        challenge_type = 'simple'
        file_dir = os.path.join(challenge_path, 'file')
        if os.path.isdir(file_dir):
            files = os.listdir(file_dir)
            if files:  # Vérifier qu'il y a au moins un fichier
                if len(files) == 1:  # Un seul fichier
                    file_name = files[0]
                    src_file_path = os.path.join(file_dir, file_name)
                    dest_dir = os.path.join(assets_dir, challenge_name)
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_file_path = os.path.join(dest_dir, file_name)
                    shutil.copy2(src_file_path, dest_file_path)
                    file_url = f'/assets/files/{challenge_name}/{file_name}'
                    challenge_type = 'file'
                else:  # Plusieurs fichiers
                    dest_dir = os.path.join(assets_dir, challenge_name)
                    os.makedirs(dest_dir, exist_ok=True)
                    zip_path = os.path.join(dest_dir, f'{challenge_name}.zip')
                    shutil.make_archive(zip_path.replace('.zip', ''), 'zip', file_dir)
                    file_url = f'/assets/files/{challenge_name}/{challenge_name}.zip'
                    challenge_type = 'file'

        # Insérer le challenge dans la base de données
        insert_challenge(challenge_name, description, flag, file_url, challenge_type)
