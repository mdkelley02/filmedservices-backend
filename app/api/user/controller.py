from .dto import UserDto
from .services import UserService
from flask_restx import Resource, reqparse
from app.api.auth.services import AuthService
from app.api.media.services import PhotoMediaService, VideoMediaService
from app.models.user import UserSchema
from app.models.media import MediaSchema
from app.api.utils.resources import (
    AdminResource,
    AuthResource,
    OwnerResource,
    PhotoResource,
)

api = UserDto.api

create_user_parser = reqparse.RequestParser()
create_user_parser.add_argument("email", required=True)
create_user_parser.add_argument("first_name", required=True)
create_user_parser.add_argument("last_name", required=True)
create_user_parser.add_argument("firebase_id", required=True)

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument("email", required=False)
update_user_parser.add_argument("first_name", required=False)
update_user_parser.add_argument("last_name", required=False)
update_user_parser.add_argument("role", required=False)
update_user_parser.add_argument("school_id", required=False)

attach_media_parser = reqparse.RequestParser()
attach_media_parser.add_argument("key", required=True)


@api.route("/")
class GetAllUsers(AdminResource):
    def get(self, **kwargs):
        try:
            return UserService.get_all()
        except Exception as error:
            print(error)
            return None


@api.route("/")
class CreateUser(Resource):
    def post(self):
        args = create_user_parser.parse_args()
        UserService.create(
            firebase_id=args["firebase_id"],
            first_name=args["first_name"],
            last_name=args["last_name"],
            email=args["email"],
        )


@api.route("/my-folder")
class GetMyFolderContent(AuthResource):
    def get(self, **kwargs):
        def make_my_folder_response(photos, videos):
            return {"photos": photos, "videos": videos}

        try:
            user = kwargs["decoded_token"]
            firebase_id = user["user_id"]
            user = UserService().get(firebase_id)
            media = user.media
            photos = []
            videos = []
            if not len(media) == 0:
                if user.role == "PHOTO_SUBSCRIBER":
                    for _media in list(media):
                        if _media.type in ["PHOTO"]:
                            url = PhotoMediaService()._generate_presigned_object_url(
                                key=_media.key
                            )
                            photo = dict(
                                key=_media.key,
                                date_created=str(_media.date_created),
                                type=_media.type,
                                url=url,
                            )
                            photos.append(photo)

                elif user.role in [
                    "PHOTO_SUBSCRIBER",
                    "VIDEO_SUBSCRIBER",
                    "SOCIAL_MEDIA_SUBSCRIBER",
                ]:
                    for _media in media:
                        if _media.type in ["PHOTO"]:
                            url = PhotoMediaService()._generate_presigned_object_url(
                                key=_media.key
                            )
                            photo = dict(
                                key=_media.key,
                                date_created=str(_media.date_created),
                                type=_media.type,
                                url=url,
                            )
                            photos.append(photo)
                        elif _media.type in ["VIDEO"]:
                            url = PhotoMediaService()._generate_presigned_object_url(
                                key=_media.key
                            )
                            video = dict(
                                key=_media.key,
                                date_created=str(_media.date_created),
                                type=_media.type,
                                url=url,
                            )
                            videos.append(video)
            print(photos, videos)
            return make_my_folder_response(photos=photos, videos=videos)
        except Exception as error:
            print(error)


@api.route("/<firebase_id>")
class ParticularUser(AdminResource):
    # get user by firebase_id
    def get(self, firebase_id, **kwargs):
        user = UserService.get(firebase_id)
        if not user:
            return None
        if not user.school:
            user = UserSchema().dump(user)
            user["registration_completed"] = False
        else:
            user = UserSchema().dump(user)
            user["registration_completed"] = True
        return user

    # put user by firebase_id
    def put(self, firebase_id, **kwargs):
        args = update_user_parser.parse_args()
        args = {k: v for k, v in args.items() if v is not None}
        UserService.edit_user(firebase_id, **args)


@api.route("/<firebase_id>/media")
class GetUsersMedia(AdminResource):
    # get all of the media attached to a user
    def get(self, firebase_id, **kwargs):
        user = UserService.get(firebase_id)
        users_media = user.media
        return_list = []
        for media in users_media:
            return_list.append(MediaSchema().dump(media))
        return return_list


@api.route("/<firebase_id>/media/<media_service>/<media_key>")
class UserMedia(AdminResource):
    # attach media to a user
    def post(self, firebase_id, media_service, media_key, **kwargs):
        try:
            if media_service == "photos":
                media_service = "PHOTO"
            elif media_service == "videos":
                media_service = "VIDEO"
            else:
                return "no such endpoint exists"

            UserService.attach_media_to_user(firebase_id, media_service, media_key)
        except Exception as error:
            print(error, "happened in controller")


# Get users by role
@api.route("/role/<role>")
class GetUsersByRole(AdminResource):
    # method_decorators = [AuthService.auth_required]

    def get(self, role):
        return UserService.get_all_users_by_role(role)
