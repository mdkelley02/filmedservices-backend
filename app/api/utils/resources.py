from flask_restx import Resource
from app.api.auth.services import AuthService


class AdminResource(Resource):
    method_decorators = [AuthService.admin_required]


class AuthResource(Resource):
    method_decorators = [AuthService.auth_required]


class PhotoResource(Resource):
    method_decorators = [AuthService.photo_subscription_required]


class VideoResource(Resource):
    method_decorators = [AuthService.video_subscription_required]


class OwnerResource(Resource):
    method_decorators = [AuthService.owner_required]
