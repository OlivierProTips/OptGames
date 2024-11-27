from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import re
import hashlib
import random
import docker

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(32).hex())

DOCKER_URL = os.getenv('DOCKER_URL', 'localhost')

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets/game.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèles
class Setting(db.Model):
    __tablename__ = 'settings'
    name = db.Column(db.String, primary_key=True)
    value = db.Column(db.String, nullable=False)
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    
    # Relation avec DockerPort
    containers = db.relationship('DockerPort', back_populates='user')

class Challenge(db.Model):
    __tablename__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    flag = db.Column(db.String, nullable=False)
    file_url = db.Column(db.String)
    type = db.Column(db.String, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    
    # Relation avec DockerPort
    containers = db.relationship('DockerPort', back_populates='challenge')

class Result(db.Model):
    __tablename__ = 'results'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), primary_key=True)
    
class DockerPort(db.Model):
    __tablename__ = 'docker_ports'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    port = db.Column(db.Integer, nullable=False, unique=True)

    # Relations
    user = db.relationship('User', back_populates='containers')
    challenge = db.relationship('Challenge', back_populates='containers')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'challenge_id', name='uq_user_challenge'),
    )
    
# Configurer le dossier où les fichiers sont stockés
FILE_FOLDER = 'assets/files'
app.config['FILE_FOLDER'] = FILE_FOLDER

# Initialisation de Docker SDK
client = docker.from_env()

# Lancement d'un container Docker
def launch_docker(dockerfile_dir, user_id, challenge_id):
        # Convertir le chemin en absolu
    dockerfile_dir = os.path.abspath('app/' + dockerfile_dir)
    
    # Vérifier que le répertoire existe et contient un Dockerfile
    if not os.path.isdir(dockerfile_dir):
        raise FileNotFoundError(f"Répertoire '{dockerfile_dir}' introuvable.")
    if not os.path.isfile(os.path.join(dockerfile_dir, 'Dockerfile')):
        raise FileNotFoundError(f"Dockerfile introuvable dans '{dockerfile_dir}'.")

    # Vérifier qu'un container n'est pas déjà en cours pour cet utilisateur
    existing_port = DockerPort.query.filter_by(user_id=user_id).first()
    if existing_port:
        raise Exception("You already have a container running.")
    
    # Ajouter l'entrée dans la table DockerPort
    new_entry = DockerPort(user_id=user_id, challenge_id=challenge_id, port=port)
    db.session.add(new_entry)
    db.session.commit()

    # Générer un port disponible entre 40000 et 50000
    used_ports = {entry.port for entry in DockerPort.query.all()}
    port = random.choice([p for p in range(40000, 50001) if p not in used_ports])

    # Construire et démarrer le container
    try:
        image, build_logs = client.images.build(path=dockerfile_dir, tag=f"challenge_{challenge_id}")
        container = client.containers.run(
            image=f"challenge_{challenge_id}",
            name=f"challenge_{user_id}_{challenge_id}",
            detach=True,
            ports={"80/tcp": port},
            remove=True,  # Supprime automatiquement le container après l'arrêt
        )
        
        # TODO Timer 30 minutes

        return port
    except Exception as e:
        # Supprimer l'entrée de la base de données
        db.session.delete(new_entry)
        db.session.commit()
        raise Exception(f"Failed to launch Docker container: {str(e)}")

# Arrêt d'un container Docker
def stop_container(user_id, challenge_id):
    # Récupérer le port pour ce challenge
    entry = DockerPort.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
    if not entry:
        raise Exception(f"No container found for this challenge({challenge_id}).")

    try:
        # Trouver le container Docker correspondant
        container = next(
            c for c in client.containers.list(all=True) 
            if f"challenge_{user_id}_{challenge_id}" in c.name
        )
        container.stop()  # Arrêter le container

        # Supprimer l'entrée de la base de données
        db.session.delete(entry)
        db.session.commit()
    except StopIteration:
        raise Exception("Container not found.")
    except Exception as e:
        raise Exception(f"Failed to stop Docker container: {str(e)}")
    
# Routes
@app.before_request
def require_login():
    if not session.get('authenticated') and request.endpoint not in ('login', 'static'):
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        hashed_password = hashlib.sha1(password.encode()).hexdigest()
        setting = Setting.query.filter_by(name='admin_password').first()
        if setting and setting.value == hashed_password:
            session['authenticated'] = True
            session['flag'] = "flag{0d6ab666b57cb29de136d57afcad8758}"
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid password.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    users = User.query.all()
    # if not users:
    #     return "No user"
    return render_template('index.html', users=users)

@app.route('/assets/files/<path:filename>')
def download_file(filename):
    # Envoie le fichier depuis le répertoire assets/files
    return send_from_directory(app.config['FILE_FOLDER'], filename, as_attachment=True)

@app.route('/user/<int:user_id>')
def user_challenges(user_id):
    user = User.query.get_or_404(user_id)
    challenges = Challenge.query.order_by(Challenge.order.asc()).all()
    results = Result.query.filter_by(user_id=user_id).all()
    completed_challenges = {r.challenge_id for r in results}
    # Récupérer les conteneurs Docker actifs pour l'utilisateur
    active_dockers = DockerPort.query.filter_by(user_id=user_id).all()
    active_dockers_dict = {
        docker.challenge_id: docker.port for docker in active_dockers
    }
    return render_template('challenges.html', user=user, challenges=challenges, completed_challenges=completed_challenges, active_dockers=active_dockers_dict, docker_url=DOCKER_URL)

@app.route('/submit_flag/<int:user_id>/<int:challenge_id>', methods=['POST'])
def submit_flag(user_id, challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    user_flag = request.json.get('flag', '').strip()

    # Vérifier le format du flag
    flag_pattern = r'^flag\{[0-9a-fA-F]+\}$'  # Regex pour flag{chaine hexa}
    if not re.match(flag_pattern, user_flag):
        return jsonify({'success': False, 'message': 'Invalid flag format.'})

    if user_flag == challenge.flag:
        # Ajouter un résultat si le flag est correct
        if not Result.query.filter_by(user_id=user_id, challenge_id=challenge_id).first():
            result = Result(user_id=user_id, challenge_id=challenge_id)
            db.session.add(result)
            db.session.commit()
        return jsonify({'success': True})

    return jsonify({'success': False, 'message': 'Incorrect flag.'})

@app.route('/results')
def results():
    # Récupérer tous les utilisateurs
    users = db.session.query(User).all()  # Remplacez 'User' par votre modèle d'utilisateur
    
    # Calculer les résultats pour chaque utilisateur
    results = []
    for user in users:
        # Récupérer tous les challenges
        total_challenges = db.session.query(Challenge).all()  # Remplacez 'Challenge' par votre modèle de challenge
        
        # Récupérer les challenges réussis par l'utilisateur
        completed_challenges = db.session.query(Result).filter(Result.user_id == user.id).all()
        
        completed_challenges_count = len(completed_challenges)  # Nombre de challenges réussis
        total_challenges_count = len(total_challenges)  # Nombre total de challenges
        
        # Ajouter l'utilisateur et ses résultats à la liste des résultats
        results.append({
            'name': user.name,
            'completed_challenges_count': completed_challenges_count,
            'total_challenges_count': total_challenges_count
        })
        
    results = sorted(results, key=lambda x: x['completed_challenges_count'], reverse=True)
    
    # Passer les résultats à la page 'results.html'
    return render_template('results.html', users=results)

@app.route('/start_docker/<int:user_id>/<int:challenge_id>', methods=['POST'])
def start_docker(user_id, challenge_id):
    data = request.json
    docker_dir = data['dockerfile_dir']
    try:
        port = launch_docker(docker_dir, user_id, challenge_id)
        return jsonify({'success': True, 'port': port})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/stop_docker/<int:user_id>/<int:challenge_id>', methods=['POST'])
def stop_docker(user_id, challenge_id):
    try:
        stop_container(user_id, challenge_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
