from . import db


class JsonAble:
    def as_dict(self):
        dict_to_return = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        dict_to_return.pop("password")
        return dict_to_return


class User(db.Model, JsonAble):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    type = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

