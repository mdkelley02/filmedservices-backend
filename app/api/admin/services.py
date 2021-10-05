from app.extensions import db
import firebase_admin
from firebase_admin import auth, credentials
from functools import wraps
from flask import request
from app.models.user import User, RoleEnum
from app.api.user.services import UserService
from app.api.media.services import PhotoMediaService, VideoMediaService
import os
import json


class AdminService:
    @staticmethod
    def add_media_to_users_media(media_key, firebase_id):
        pass

    @staticmethod
    def delete_media(media_key):
        pass

    @staticmethod
    def upload_photo():
        pass

