import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clinica_secret_key_2026'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "instance", "clinica.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False