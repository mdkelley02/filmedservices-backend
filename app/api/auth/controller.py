from flask_restx import Resource, reqparse
from app.models.user import User
from .services import AuthService
from app.api.user.services import UserService
from app.api.school.services import SchoolService
from app.extensions import db
from .dto import AuthDto
from app.api.utils.make_response import make_response
from app.api.utils.events import Events
import json


api = AuthDto.api

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument("school_id", required=False)


@api.route("/login")
class Login(Resource):
    method_decorators = [AuthService.auth_required]

    def post(self, **kwargs):
        try:
            user = kwargs["decoded_token"]
            firebase_id = user["uid"]
            user_object = UserService.get(firebase_id)
            if not user_object:
                first_name, last_name = user["name"].split(" ")
                email = user["email"]
                UserService.create(
                    firebase_id=firebase_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )
                return make_response(
                    message="new user created",
                    event=Events.USER_CREATION_INITIATED,
                    response_code=200,
                )
            elif not user_object.school:
                args = create_user_parser.parse_args()
                if not args.get("school_id", None):
                    return make_response(
                        message="school_id is required",
                        event=Events.USER_CREATION_INITIATED,
                        response_code=200,
                    )
                school = SchoolService.get_school(args["school_id"])
                if not school:
                    return None
                user_object.school = school
                db.session.commit()
                return make_response(
                    message="User creation completed",
                    event=Events.USER_CREATED,
                    response_code=200,
                )
            return make_response(
                message="user logged in", event=Events.USER_LOGGED_IN, response_code=200
            )
        except Exception as e:
            print(e, "this is where the error has been thrown")


@api.route("/permission")
class GetPermission(Resource):
    method_decorators = [AuthService.auth_required]

    def get(self, **kwargs):
        user_info = kwargs["decoded_token"]
        firebase_id = user_info["uid"]
        user = UserService.get(firebase_id)
        if user == None:
            return make_response(
                message="user does not exist",
                event=Events.USER_DOES_NOT_EXIST,
                response_code=400,
            )
        return user.role
