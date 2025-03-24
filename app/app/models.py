# models.py
from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Moto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marque = db.Column(db.String(50), nullable=False)
    modele = db.Column(db.String(50), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    kilometrage = db.Column(db.Integer)
    prix = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(200))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))