# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-à-changer-en-prod'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    SQLALCHEMY_DATABASE_URI = os.environ.get('mysql+pymysql://moto_user:moto_password@mariadb:3306/moto_db') or \
        'mysql+pymysql://moto_user:moto_password@mariadb:3306/moto_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False