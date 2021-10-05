from app.models.user import User, UserSchema, User, RoleEnum
from app.models.media import Media
from app.models.school import School, SchoolSchema
from app.extensions import db


class UserService:
    @staticmethod
    def update_role(firebase_id, role):
        user = User.query.filter_by(firebase_id=firebase_id).first()
        if not user:
            return None
        if not role in RoleEnum._member_names_:
            return None
        user.role = role
        db.session.commit()

    @staticmethod
    def get(firebase_id):
        user = User.query.filter_by(firebase_id=firebase_id).first()
        if not user:
            return None
        return user

    @staticmethod
    def create(**kwargs):
        try:
            user = User(**kwargs)
            db.session.add(user)
            db.session.commit()
        except Exception as error:
            print("error in create")
            return error

    @staticmethod
    def get_all():
        query = User.query.all()
        user_schema = UserSchema(many=True)
        users = user_schema.dump(query)
        return users

    @staticmethod
    def get_all_users_by_role(role):
        if not role in RoleEnum._member_names_:
            return None
        query = User.query.filter_by(role=role)
        user_schema = UserSchema(many=True)
        users = user_schema.dump(query)
        return users

    @staticmethod
    def promote_user_to_admin(firebase_id):
        user = User.query.filter_by(firebase_id=firebase_id).first()
        if not user:
            return None
        if user.role == RoleEnum.ADMIN:
            return None
        user.role = RoleEnum.ADMIN
        db.session.commit()

    @staticmethod
    def edit_user(firebase_id, **kwargs):
        user = User.query.filter_by(firebase_id=firebase_id)
        if not user:
            return None
        user.update(dict(**kwargs))
        db.session.commit()

    @staticmethod
    def attach_media_to_user(firebase_id, media_type, media_key):
        media = Media.query.filter_by(key=media_key, type=media_type).first()
        if not media:
            return None
        user = User.query.filter_by(firebase_id=firebase_id).first()
        if not user:
            return None
        if not media in user.media:
            user.media.append(media)
            db.session.commit()
