from flask import Flask
from .extensions import db, cors, ma
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

class DevelopmentConfig(object):
    DEBUG = True
    SECRET_KEY = os.urandom(20)
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRES_CONNECTION_STRING")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config_map = {"development": DevelopmentConfig, "production": ProductionConfig}


def register_extensions(app):
    db.init_app(app)
    cors.init_app(app)
    ma.init_app(app)


def create_app(config="dev"):
    app = Flask(__name__)

    selected_config = config_map[os.environ.get("FLASK_ENV")]

    app.config.from_object(selected_config)

    register_extensions(app)

    from .api import api_bp

    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app
