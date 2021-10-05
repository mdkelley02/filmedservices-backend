from flask_restx import Resource, reqparse
from .dto import MediaDto
from .services import PhotoMediaService, VideoMediaService, MediaService
from app.api.utils.resources import (
    AuthResource,
    AdminResource,
    VideoResource,
    PhotoResource,
)
from app.models.user import UserSchema
import werkzeug


api = MediaDto.api

media_upload_parser = reqparse.RequestParser()
media_upload_parser.add_argument(
    "file", type=werkzeug.datastructures.FileStorage, location="files"
)

supported_photo_types = ["image/jpeg", "image/png"]

supported_video_types = ["video/mp4", "video/mov"]


@api.route("/<media_key>/associated-users")
class GetAssociatedUser(AdminResource):
    def get(self, media_key, **kwargs):
        users = MediaService.get_medias_associated_users(media_key)
        if not users:
            return []
        users = [UserSchema().dump(user) for user in users]
        return users


@api.route("/photos")
class GetAllPhotos(PhotoResource):
    def get(self, **kwargs):
        response = PhotoMediaService().get_all_objects()
        return response


@api.route("/photos")
class UploadPhoto(AdminResource):
    def post(self, **kwargs):
        args = media_upload_parser.parse_args()
        if not args["file"].mimetype in supported_photo_types:
            return {"message": f"file type is not supported"}
        PhotoMediaService().upload_object(file=args["file"])


@api.route("/photos/<photo_key>")
class GetParticularPhoto(PhotoResource):
    def get(self, photo_key):
        response = PhotoMediaService().get_object(photo_key)
        if not response:
            return None
        return response


@api.route("/photos/<photo_key>")
class DeleteParticularPhoto(AdminResource):
    def delete(self, photo_key, **kwargs):
        response = PhotoMediaService().delete_object(photo_key)
        if not response:
            return {"message": f"{photo_key} does not exist"}
        return {"message": f"{photo_key} succesfully deleted"}


@api.route("/videos")
class GetAllVideos(VideoResource):
    def get(self, **kwargs):
        response = VideoMediaService().get_all_objects()
        if not response:
            return []
        return response


@api.route("/videos")
class VideoUpload(AdminResource):
    def post(self, **kwargs):
        args = media_upload_parser.parse_args()
        print(args)
        print(args["file"].mimetype)
        if not args["file"].mimetype in supported_video_types:
            return {"message": f"file type is not supported"}
        VideoMediaService().upload_object(file=args["file"])


@api.route("/videos/<video_key>")
class GetParticularVideo(VideoResource):
    def get(self, video_key, **kwargs):
        response = VideoMediaService().get_object(video_key)
        if not response:
            return None
        return response


@api.route("/videos/<video_key>")
class DeleteVideo(AdminResource):
    def delete(self, video_key, **kwargs):
        try:
            VideoMediaService().delete_object(video_key)
        except Exception as error:
            print(error)
