from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
# cors = CORS(origins=["http://localhost:3000"])
cors = CORS(resources={r"*": {"origins": "*"}})

ma = Marshmallow()
