from flask import Flask
from .config import DevConfig, ProdConfig
from .extensions import db, cors, ma
from dotenv import load_dotenv, find_dotenv
import os


config_map = {"development": DevConfig, "production": ProdConfig}


def register_extensions(app):
    db.init_app(app)
    cors.init_app(app)
    ma.init_app(app)


def create_app(config="dev"):
    app = Flask(__name__)
    load_dotenv(find_dotenv())

    selected_config = config_map[os.environ.get("FLASK_ENV")]
    selected_config.SQLALCHEMY_DATABASE_URI = os.environ.get(
        "POSTGRES_CONNECTION_STRING"
    )
    app.config.from_object(selected_config)

    register_extensions(app)

    from .api import api_bp

    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app
