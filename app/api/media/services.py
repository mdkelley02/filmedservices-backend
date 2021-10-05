import uuid
import boto3
import os
from app.models.media import Media, MediaSchema
from app.extensions import db

S3_REGION = os.environ.get("BUCKET_REGION")
PHOTO_BUCKET = os.environ.get("PHOTO_BUCKET")
VIDEO_BUCKET = os.environ.get("VIDEO_BUCKET")
# s3 = boto3.client("s3")
s3 = boto3.client(
    "s3",
    region_name=os.environ.get("AWS_DEFAULT_REGION"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)


class MediaService:
    @staticmethod
    def get_medias_associated_users(media_key):
        query = Media.query.filter_by(key=media_key).first()
        if not query:
            return None
        users = query.users
        return users


class S3Service:
    def __init__(self, bucket, client, media_type):
        self.bucket = bucket
        self.client = client
        self.media_type = media_type

    def _generate_presigned_object_url(self, key, ttl=3600):
        url = self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=ttl,
        )
        if not url:
            url = None
        return url

    def _generate_object_key(self):
        return f"{self.media_type}-{str(uuid.uuid1())[0:6]}-{str(uuid.uuid1())[0:6]}"

    def _create_media(self, key):
        media = Media(key=key, type=self.media_type)
        db.session.add(media)
        db.session.commit()

    def upload_object(self, file):
        key = self._generate_object_key()
        try:
            self.client.put_object(
                Body=file,
                Bucket=self.bucket,
                Key=key,
                ContentType="multipart/form-data",
            )
            self._create_media(key)
        except Exception as error:
            return error

    def get_object(self, key):
        media = Media.query.filter_by(key=key).first()
        url = self._generate_presigned_object_url(key, ttl=3600)
        return dict(**MediaSchema().dump(media), url=url)
        # return url

    def get_object_by_id(self, media_id):
        media = Media.query.filter_by(id=media_id)
        if not media:
            return None
        return media

    def get_object_by_key(self, key):
        media = Media.query.filter_by(key=key)
        if not media:
            return None
        return media

    def delete_object(self, key):
        media = Media.query.filter_by(key=key).first()
        if not media:
            return None
        self.client.delete_object(Bucket=self.bucket, Key=key)
        db.session.delete(media)
        db.session.commit()

    def get_all_objects(self):
        response = []
        media_objects = self.client.list_objects(Bucket=self.bucket).get("Contents", [])
        for media in media_objects:
            key = media["Key"]
            last_modified = media["LastModified"]
            media_url = self._generate_presigned_object_url(key)
            media_object = dict(
                key=key,
                url=media_url,
                date_created=str(last_modified),
                type=self.media_type,
            )
            response.append(media_object)
        return response


class PhotoMediaService(S3Service):
    def __init__(self):
        super(PhotoMediaService, self).__init__(PHOTO_BUCKET, s3, "PHOTO")


class VideoMediaService(S3Service):
    def __init__(self):
        super(VideoMediaService, self).__init__(VIDEO_BUCKET, s3, "VIDEO")
