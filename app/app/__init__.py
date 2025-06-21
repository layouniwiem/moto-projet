from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(test_config=None):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    if test_config:
        app.config.from_object(test_config)
    else:
        env = os.getenv('FLASK_ENV', 'development').lower()
        if env == 'production':
            from .config import ProductionConfig
            app.config.from_object(ProductionConfig)
        elif env == 'testing':
            from .config import TestingConfig
            app.config.from_object(TestingConfig)
        else:
            from .config import DevelopmentConfig
            app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    # Création dossier static/img s'il n'existe pas
    import os
    os.makedirs(os.path.join(app.static_folder, 'img'), exist_ok=True)

    return app

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
