from app.extensions import db
from app.models.school import School, SchoolSchema


class SchoolService:
    @staticmethod
    def get_schools():
        query = School.query.all()
        school_schema = SchoolSchema(many=True)
        schools = school_schema.dump(query)
        return schools

    @staticmethod
    def get_school(school_id):
        school = School.query.filter_by(id=school_id).first()
        if not school:
            return None
        return school

    @staticmethod
    def create_school(**kwargs):
        school = School(**kwargs)
        db.session.add(school)
        db.session.commit()

    @staticmethod
    def update_school(school_id, **kwargs):
        school = School.query.filter_by(id=school_id)
        if not school:
            return None
        school.update(dict(**kwargs))
        db.session.commit()
        return school.first()

    @staticmethod
    def delete_school(school_id):
        school = School.query.filter_by(id=school_id).first()
        if not school:
            return "School does not exist"
        db.session.delete(school)
        db.session.commit()
        return "School succesfully deleted"
