import datetime
from app.extensions import db, ma
import enum


class RoleEnum(str, enum.Enum):
    UNSUBSCRIBED = "UNSUBSCRIBED"
    PHOTO_SUBSCRIBER = "PHOTO_SUBSCRIBER"
    VIDEO_SUBSCRIBER = "VIDEO_SUBSCRIBER"
    SOCIAL_MEDIA_SUBSCRIBER = "SOCIAL_MEDIA_SUBSCRIBER"
    ADMIN = "ADMIN"
    OWNER = "OWNER"


media = db.Table(
    "users_media",
    db.Column("users_id", db.Integer, db.ForeignKey("users.id"), nullable=False),
    db.Column("media_id", db.Integer, db.ForeignKey("media.id"), nullable=False),
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firebase_id = db.Column(db.String, nullable=False)
    stripe_id = db.Column(db.String, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"))
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.UNSUBSCRIBED)
    media = db.relationship("Media", secondary=media, backref="users")

    def __repr__(self):
        return f"<User {self.email}>"


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
