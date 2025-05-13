# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
import os

# Initialiser les extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__, template_folder='../templates',static_folder='../static')  # Ajout du chemin des fichiers statiques
    
    app.config.from_object(Config)

    # Initialiser les extensions avec l'app
    db.init_app(app)
    login_manager.init_app(app)

    # Les imports sont placés ici pour éviter les imports circulaires
    from .routes import main, auth
    
    # Enregistrer les blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    
    from .monitoring import monitoring
    monitoring.register_metrics(app)

    # Créer les dossiers nécessaires s'ils n'existent pas
    os.makedirs(os.path.join(app.static_folder, 'img'), exist_ok=True)

    return app

# Importer les modèles ici pour qu'ils soient disponibles
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

