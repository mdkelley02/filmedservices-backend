from app.extensions import db
import firebase_admin
from firebase_admin import auth, credentials
from functools import wraps
from flask import request
from app.models.user import User, RoleEnum
from app.api.user.services import UserService
import os
import json


cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
default_app = firebase_admin.initialize_app(cred)


class AuthService:
    @staticmethod
    def auth_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return "Missing authorization header", 400
            try:
                decoded_token = auth.verify_id_token(token)
                kwargs["decoded_token"] = decoded_token
                return f(*args, **kwargs)
            except Exception as e:
                return "Invalid token", 400

        return wrap

    @staticmethod
    def photo_subscription_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return "Missing authorization header", 400
            try:
                decoded_token = auth.verify_id_token(token)
                firebase_id = decoded_token["uid"]
                user = UserService.get(firebase_id)
                if user.role in [RoleEnum.UNSUBSCRIBED]:
                    return "Invalid permission", 400
                kwargs["decoded_token"] = decoded_token
                return f(*args, **kwargs)
            except Exception as e:
                return "Invalid token", 400

        return wrap

    @staticmethod
    def video_subscription_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return "Missing authorization header", 400
            try:
                decoded_token = auth.verify_id_token(token)
                firebase_id = decoded_token["uid"]
                user = UserService.get(firebase_id)
                if user.role is [RoleEnum.UNSUBSCRIBED, RoleEnum.PHOTO_SUBSCRIBER]:
                    return "Invalid permission", 400
                kwargs["decoded_token"] = decoded_token
                return f(*args, **kwargs)
            except Exception as e:
                return "Invalid token", 400

        return wrap

    @staticmethod
    def admin_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return "Missing authorization header", 400
            try:
                decoded_token = auth.verify_id_token(token)
                firebase_id = decoded_token["uid"]
                user = UserService.get(firebase_id)
                if not (user.role in [RoleEnum.ADMIN, RoleEnum.OWNER]):
                    return "Invalid permission", 400
                kwargs["decoded_token"] = decoded_token
                return f(*args, **kwargs)
            except Exception as e:
                print(e)
                return "Invalid token", 400

        return wrap

    @staticmethod
    def owner_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return "Missing authorization header", 400
            try:
                decoded_token = auth.verify_id_token(token)
                firebase_id = decoded_token["uid"]
                user = UserService.get(firebase_id)
                if not (user.role in [RoleEnum.OWNER]):
                    return "Invalid permission", 400
                return f(*args, **kwargs)
            except Exception as e:
                return "Invalid token", 400

        return wrap
