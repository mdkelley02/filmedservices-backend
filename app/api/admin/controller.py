from flask_restx import Resource, reqparse
from app.models.user import User
from .services import AdminService
from app.api.user.services import UserService
from app.extensions import db
from .dto import AdminDto
from app.api.utils.make_response import make_response
from app.api.utils.events import Events
import json


api = AdminDto.api


@api.route("/users/role/<role>")
class Admin(Resource):
    def get(self, role):
        users = AdminService.list_all_users_by_role(role)
        return users
