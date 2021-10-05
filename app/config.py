import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class DevConfig(object):
    DEBUG = True
    SECRET_KEY = os.urandom(20)
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRES_CONNECTION_STRING")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
