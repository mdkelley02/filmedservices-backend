from flask_restx import Namespace, fields


class AdminDto:
    api = Namespace("admin", description="admin endpoints")
