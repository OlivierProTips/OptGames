from sqlalchemy import create_engine, MetaData, Table
import vars

# Chemin vers la base de données SQLite
db_path = f"{vars.ASSET_DIR}/game.db"
engine = create_engine(f"sqlite:///{db_path}")

# Charger les métadonnées
metadata = MetaData()
metadata.reflect(bind=engine)

# Accéder aux tables
results_table = Table('results', metadata, autoload_with=engine)
users_table = Table('users', metadata, autoload_with=engine)
dockers_table = Table('docker_ports', metadata, autoload_with=engine)

# Connexion à la base de données
with engine.connect() as connection:
    # Vider la table results
    connection.execute(results_table.delete())
    print("Table 'results' vidée avec succès.")
    
    # Vider la table users
    connection.execute(users_table.delete())
    print("Table 'users' vidée avec succès.")
    
    # Vider la table docker_ports
    connection.execute(dockers_table.delete())
    print("Table 'docker_ports' vidée avec succès.")
    
    connection.commit()
