from flask_restx import Resource, reqparse
from flask import jsonify
from .services import SchoolService
from .dto import SchoolDto
from app.api.utils.events import Events
from app.api.utils.make_response import make_response
from app.models.school import School, SchoolSchema
from app.api.utils.resources import AdminResource

api = SchoolDto.api


@api.route("/")
class SchoolController(Resource):
    def get(self):
        schools = SchoolService.get_schools()
        response = schools
        return response, 200


@api.route("/")
class CreateSchool(AdminResource):
    def post(self, **kwargs):
        school_parser = reqparse.RequestParser()
        school_parser.add_argument("name", required=True)
        school_parser.add_argument("address", required=True)
        school_parser.add_argument("city", required=True)
        school_parser.add_argument("state", required=True)
        school_parser.add_argument("zip_code", required=True)

        request_args = school_parser.parse_args()
        SchoolService.create_school(**request_args)

        return make_response(
            message=request_args, event=Events.SCHOOL_CREATED, response_code=200
        )


@api.route("/<school_id>")
class GranularSchoolController(AdminResource):
    def get(self, school_id, **kwargs):
        school = SchoolService.get_school(school_id)
        if not school:
            return None
        return SchoolSchema().dump(school)

    def put(self, school_id, **kwargs):
        update_school_parser = reqparse.RequestParser()
        update_school_parser.add_argument("name", required=False)
        update_school_parser.add_argument("address", required=False)
        update_school_parser.add_argument("city", required=False)
        update_school_parser.add_argument("state", required=False)
        update_school_parser.add_argument("zip_code", required=False)
        args = update_school_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}

        school = SchoolService.update_school(school_id, **args)
        if not school:
            return None
        return SchoolSchema().dump(school)

    def delete(self, school_id, **kwargs):
        try:
            return SchoolService.delete_school(school_id)
        except Exception as error:
            print(error)
