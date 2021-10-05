from flask_restx import Api
from flask import Blueprint
from flask import json

from .media.controller import api as media_ns
from .school.controller import api as school_ns
from .payments.controller import api as payments_ns
from .auth.controller import api as auth_ns
from .user.controller import api as user_ns
from .admin.controller import api as admin_ns

api_bp = Blueprint(
    "api",
    __name__,
)

api = Api(api_bp, title="API", description="core routes")

# API namespaces
api.add_namespace(media_ns)
api.add_namespace(school_ns)
api.add_namespace(payments_ns)
api.add_namespace(auth_ns)
api.add_namespace(user_ns)
api.add_namespace(admin_ns)
