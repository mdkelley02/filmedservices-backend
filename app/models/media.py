from app.extensions import db, ma
import enum
import datetime


class MediaTypeEnum(str, enum.Enum):
    PHOTO = "PHOTO"
    VIDEO = "VIDEO"


class Media(db.Model):
    __tablename__ = "media"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    key = db.Column(db.String, nullable=False)
    type = db.Column(db.Enum(MediaTypeEnum), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, key, type):
        self.key = key
        self.type = type


class MediaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Media
