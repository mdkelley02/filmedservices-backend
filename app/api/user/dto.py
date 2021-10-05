from flask_restx import Namespace, fields


class UserDto:
    api = Namespace("users", description="users endpoints")
