import hashlib
import sqlite3
import vars

# Demander le mot de passe à l'utilisateur
password = input("Veuillez entrer le mot de passe administrateur : ")

# Hacher le mot de passe avec SHA-1
hashed_password = hashlib.sha1(password.encode()).hexdigest()

# Chemin vers votre base de données
db_path = f"{vars.ASSET_DIR}/game.db"

# Connexion à la base de données et insertion
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Insérez ou mettez à jour le mot de passe
cursor.execute("INSERT OR REPLACE INTO settings (name, value) VALUES (?, ?)", ('admin_password', hashed_password))
connection.commit()
connection.close()

print(f"Mot de passe haché inséré : {hashed_password}")
