from flask_restx import Namespace, fields


class AuthDto:
    api = Namespace("auth", description="auth endpoints")
