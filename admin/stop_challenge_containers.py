import docker
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config

# Configuration SQLAlchemy
DATABASE_URL = f"sqlite:///{config.ASSET_DIR}/game.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Définition du modèle DockerPort
class DockerPort(Base):
    __tablename__ = 'docker_ports'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    challenge_id = Column(Integer, nullable=False)
    port = Column(Integer, nullable=False)

# Initialiser la base de données (si ce n'est pas encore fait)
Base.metadata.create_all(engine)

def stop_challenge_containers():
    # Initialiser le client Docker
    client = docker.from_env()
    db_session = Session()

    try:
        # Lister tous les conteneurs en cours d'exécution
        containers = client.containers.list()

        for container in containers:
            if container.name.startswith("challenge_"):
                print(f"Stopping container: {container.name}")
                try:
                    container.stop()
                    container.remove()
                except Exception as e:
                    print(f"Error stopping/removing container {container.name}: {e}")

        # Vider la table docker_ports
        db_session.query(DockerPort).delete()
        db_session.commit()
        print("Cleared docker_ports table.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Fermer la session de la base de données
        db_session.close()

if __name__ == "__main__":
    stop_challenge_containers()
