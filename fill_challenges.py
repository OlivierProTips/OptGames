import os
import sqlite3
import shutil

# Chemins de répertoire
challenges_dir = 'challenges'
assets_dir = 'app/assets/files'
os.makedirs(assets_dir, exist_ok=True)

# Connexion à la base de données SQLite
conn = sqlite3.connect('app/game.db')
cursor = conn.cursor()

# Création de la table challenges si elle n'existe pas déjà
cursor.execute('''
CREATE TABLE IF NOT EXISTS challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    description TEXT,
    flag TEXT NOT NULL,
    file_url TEXT,
    type TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS "results" (
	"user_id"	INTEGER NOT NULL,
	"challenge_id"	INTEGER NOT NULL,
	PRIMARY KEY("challenge_id","user_id"),
	FOREIGN KEY("challenge_id") REFERENCES "challenges"("id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id")
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS "settings" (
	"name"	TEXT UNIQUE,
	"value"	TEXT
)
''')
conn.commit()

# Fonction pour insérer un challenge dans la base de données
def insert_challenge(title, description, flag, file_url, challenge_type):
    cursor.execute('SELECT id FROM challenges WHERE title = ?', (title,))
    if cursor.fetchone() is None:  # Vérifier si le challenge existe déjà
        cursor.execute('''
        INSERT INTO challenges (title, description, flag, file_url, type)
        VALUES (?, ?, ?, ?, ?)
        ''', (title, description, flag, file_url, challenge_type))
        conn.commit()
        print(f'Challenge "{title}" inséré dans la base de données.')
    else:
        print(f'Challenge "{title}" existe déjà dans la base de données.')

# Parcours des répertoires de challenges
for challenge_name in os.listdir(challenges_dir):
    if challenge_name == "__pycache__": continue
    challenge_path = os.path.join(challenges_dir, challenge_name)
    if os.path.isdir(challenge_path):  # Vérifier que c'est un répertoire
        # Lecture des fichiers description.txt et flag.txt
        description_path = os.path.join(challenge_path, 'description.txt')
        flag_path = os.path.join(challenge_path, 'flag.txt')

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
                file_name = files[0]
                src_file_path = os.path.join(file_dir, file_name)
                dest_dir = os.path.join(assets_dir, challenge_name)
                os.makedirs(dest_dir, exist_ok=True)
                dest_file_path = os.path.join(dest_dir, file_name)

                shutil.copy2(src_file_path, dest_file_path)
                file_url = f'/assets/files/{challenge_name}/{file_name}'
                challenge_type = 'file'

        # Insérer le challenge dans la base de données
        insert_challenge(challenge_name, description, flag, file_url, challenge_type)

# Fermeture de la connexion à la base de données
conn.close()
