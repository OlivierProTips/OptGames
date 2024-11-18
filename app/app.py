from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import re

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'game.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèles
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

class Challenge(db.Model):
    __tablename__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    flag = db.Column(db.String, nullable=False)
    file_url = db.Column(db.String)
    type = db.Column(db.String, nullable=False)
    order = db.Column(db.Integer, nullable=False)

class Result(db.Model):
    __tablename__ = 'results'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), primary_key=True)
    
# Configurer le dossier où les fichiers sont stockés
FILE_FOLDER = 'assets/files'
app.config['FILE_FOLDER'] = FILE_FOLDER
    
# Routes
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
    return render_template('challenges.html', user=user, challenges=challenges, completed_challenges=completed_challenges)

@app.route('/submit_flag/<int:user_id>/<int:challenge_id>', methods=['POST'])
def submit_flag(user_id, challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    user_flag = request.form.get('flag').strip()
    # Vérifier le format du flag
    flag_pattern = r'^flag\{[0-9a-fA-F]+\}$'  # Regex pour flag{chaine hexa}
    if not re.match(flag_pattern, user_flag):
        return redirect(url_for('user_challenges', user_id=user_id))
    if user_flag == challenge.flag:
        # Ajouter un résultat si le flag est correct
        if not Result.query.filter_by(user_id=user_id, challenge_id=challenge_id).first():
            result = Result(user_id=user_id, challenge_id=challenge_id)
            db.session.add(result)
            db.session.commit()
    return redirect(url_for('user_challenges', user_id=user_id))

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



if __name__ == '__main__':
    app.run(debug=True)
