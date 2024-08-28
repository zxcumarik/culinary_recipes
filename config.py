import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456789'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'culinary.db')
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@postgres_recipes:5432/postgres'
