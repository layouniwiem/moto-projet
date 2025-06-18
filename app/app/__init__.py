from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

##def create_app():
 #   app = Flask(__name__, template_folder='../templates', static_folder='../static')
#
 #   app.config.from_object(Config)
#
 #   db.init_app(app)
   # login_manager.init_app(app)

   # from .routes import main, auth
  #  app.register_blueprint(main)
   # app.register_blueprint(auth)

   # from monitoring import setup_metrics
   # setup_metrics(app)

  #  os.makedirs(os.path.join(app.static_folder, 'img'), exist_ok=True)

   # return app

#from .models import User
def create_app(test_config=None):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    #from monitoring import monitoring
    #monitoring.register_metrics(app)
    from monitoring import setup_metrics
    setup_metrics(app)
    os.makedirs(os.path.join(app.static_folder, 'img'), exist_ok=True)

    return app
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
