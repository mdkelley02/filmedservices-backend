import datetime
from app.extensions import db, ma
import enum


class RoleEnum(enum.Enum):
    UNSUBSCRIBED = 0
    PHOTO_SUBSCRIBER = 1
    VIDEO_SUBSCRIBER = 2
    SOCIAL_MEDIA_SUBSCRIBER = 3
    ADMIN = 4
    OWNER = 5


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"))
    # school = db.relationship("School", backref=db.backref("User"))
    role = db.Column(db.Enum(RoleEnum))
    # users_media_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    # users_media = db.relationship(
    #     "Media", secondary=users_media, backref="users"
    # )

    # def __init__(
    #     self,
    #     email,
    #     first_name,
    #     last_name,
    #     school,

    # ):
    #     self.email = email
    #     self.first_name = first_name
    #     self.last_name = last_name

    def __repr__(self):
        return f"<User {self.email}>"


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class School(db.Model):
    __tablename__ = 'schools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    state = db.Column(db.String(200))
    city = db.Column(db.String(200))
    zip_code = db.Column(db.Integer)
    users = db.relationship("User", backref=db.backref(
        "school", lazy="joined"), lazy="select")

    def __init__(self, name, address, state, city, zip_code):
        self.name = name
        self.address = address
        self.state = state
        self.city = city
        self.zip_code = zip_code

    def __repr__(self):
        return f"<School {vars(self)}>"


class SchoolSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = School
