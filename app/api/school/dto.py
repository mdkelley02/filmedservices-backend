from flask_restx import Namespace, fields


class SchoolDto:
    api = Namespace("schools", description="school endpoints")
    school = api.model("school object", {"name": fields.String})
    data_resp = api.model("User Data Response", {"message": fields.String})
