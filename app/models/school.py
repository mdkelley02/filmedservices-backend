from app.extensions import db, ma


class School(db.Model):
    __tablename__ = "schools"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    state = db.Column(db.String(200))
    city = db.Column(db.String(200))
    zip_code = db.Column(db.Integer())
    users = db.relationship(
        "User", backref=db.backref("school", lazy="joined"), lazy="select"
    )

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

    id = ma.auto_field()
