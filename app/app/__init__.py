import os

class Config:
    # Clé secrète pour Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')

    # Infos base de données MySQL / MariaDB
    MYSQL_USER = os.environ.get('MYSQL_USER', 'default_user')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'default_password')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'default_db')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'mariadb')  # service Kubernetes

    # Construction dynamique de l'URI SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Environnement Flask (optionnel)
    FLASK_ENV = os.environ.get('FLASK_ENV', 'production')

    # Autres configs spécifiques si besoin
